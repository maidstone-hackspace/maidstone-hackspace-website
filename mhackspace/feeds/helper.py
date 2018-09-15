# -*- coding: utf-8 -*-
import os
import logging
import feedparser

from time import mktime
from datetime import datetime
from urllib.request import urlretrieve
from django.core.files import File
from django.utils.timezone import make_aware
from django.utils import timezone
from stdimage.utils import render_variations
from mhackspace.feeds.reader import fetch_feeds

# from scaffold.readers.rss_reader import feed_reader

from mhackspace.feeds.models import Feed, Article, image_variations

logger = logging.getLogger(__name__)


def feed_reader(feeds):
    for feed in feeds:
        print(feed)
        yield feedparser.parse(feed["url"])


def import_feeds(feed=False):
    remove_old_articles()

    print([f.get("url") for f in get_active_feeds(feed)])
    rss_articles = fetch_feeds(get_active_feeds(feed))

    articles = []
    for article in rss_articles:
        date = datetime.fromtimestamp(mktime(article["date"]))
        print(article["title"])
        print(article["image"])
        print('#############')
        articles.append(
            Article(
                url=article["url"],
                feed=Feed.objects.get(pk=article["feed"]),
                title=article["title"][0:100],
                original_image=article["image"][0:100],
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
