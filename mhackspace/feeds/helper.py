# -*- coding: utf-8 -*-
import os
import tempfile
import requests
import logging
from time import mktime
from datetime import datetime
from django.conf import settings
from django.core.files import File
from stdimage.utils import render_variations
from mhackspace.feeds.reader import fetch_feeds

from mhackspace.feeds.models import Feed, Article, image_variations

logger = logging.getLogger(__name__)


def import_feeds(feed=False):
    remove_old_articles()
    articles = []
    for article in fetch_feeds(get_active_feeds(feed)):
        date = datetime.fromtimestamp(mktime(article["date"]))
        articles.append(
            Article(
                url=article["url"],
                feed=Feed.objects.get(pk=article["feed"]),
                title=article["title"],
                original_image=article["image"],
                description=article["description"],
                date=date,
            )
        )
    articles = Article.objects.bulk_create(articles)
    download_remote_images()
    return articles


def remove_old_articles():
    for article in Article.objects.all():
        article.image.delete(save=False)
    Article.objects.all().delete()


def download_remote_images():
    for article in Article.objects.all():
        print(article.original_image)
        if not article.original_image:
            continue
        try:
            result = requests.get(article.original_image)
        except Exception as e:
            logger.exception(result.status_code)
            logger.exception(
                "Unable to download remote image for %s"
                % article.original_image
            )
            return

        try:
            tmpfile = tempfile.TemporaryFile(mode='w+b')
            tmpfile.write(result.content)

            article.image.save(
                os.path.basename(article.original_image),
                File(tmpfile),
            )

            file_path = f'{settings.MEDIA_ROOT}/{article.image.file}'
            render_variations(file_path, image_variations, replace=True)
            article.save()
        except Exception as e:
            logger.exception(result)
        finally:
            tmpfile.close()


def get_active_feeds(feed=False):
    if feed is not False:
        feeds = Feed.objects.filter(pk__in=feed)
    else:
        feeds = Feed.objects.all()

    rss_feeds = []
    for feed in feeds:
        if feed.enabled is False:
            continue
        rss_feeds.append(
            {"id": feed.id, "author": feed.author, "url": feed.feed_url}
        )
    return rss_feeds
