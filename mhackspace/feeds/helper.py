# -*- coding: utf-8 -*-
import os
import logging

from time import mktime
from datetime import datetime
from urllib.request import urlretrieve
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
        if not article.original_image:
            continue
        try:
            result = urlretrieve(article.original_image.__str__())
            article.image.save(
                os.path.basename(article.original_image.__str__()),
                File(open(result[0], "rb")),
            )
            render_variations(result[0], image_variations, replace=True)
            article.save()
        except Exception as e:
            logger.exception(result)
            logger.exception(result[0])
            logger.exception(
                "Unable to download remote image for %s"
                % article.original_image
            )


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
