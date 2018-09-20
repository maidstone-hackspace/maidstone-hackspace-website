# -*- coding: utf-8 -*-
import os
import requests
import logging
from io import BytesIO
from time import mktime
from datetime import datetime

from django.core.files import File

from mhackspace.feeds.reader import fetch_feeds
from mhackspace.feeds.models import Feed, Article

logger = logging.getLogger(__name__)


def import_feeds(feed=False):
    remove_old_articles()
    articles = fetch_feeds(get_active_feeds(feed))
    article_objects = []
    # for author in articles:
    for article in articles:
        date = datetime.fromtimestamp(mktime(article["date"]))
        article_objects.append(
            Article(
                url=article["url"],
                feed=Feed.objects.get(pk=article["feed"]),
                title=article["title"],
                original_image=article["image"],
                description=article["description"],
                date=date,
            )
        )
    articles = Article.objects.bulk_create(article_objects)
    download_remote_images()
    return articles


def remove_old_articles():
    for article in Article.objects.all():
        article.image.delete(save=False)
    Article.objects.all().delete()


def download_remote_images():
    for article in Article.objects.all():
        if not article.original_image:
            continue
        try:
            result = requests.get(article.original_image, timeout=5)
        except Exception as e:
            logger.exception(result.status_code)
            logger.exception(
                "Unable to download remote image for %s"
                % article.original_image
            )
            return

        try:
            article.image.save(
                os.path.basename(article.original_image),
                File(BytesIO(result.content)),
            )
            article.save()
        except Exception as e:
            logger.exception(result)


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
