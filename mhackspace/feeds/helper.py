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
from huey.contrib.djhuey import task


logger = logging.getLogger(__name__)


def import_feeds(feed=False):
    feeds = Feed.objects.filter(enabled=True)
    count = 0
    for feed in feeds.all():
        try:
            import_feed(feed.pk)
            count += 1
        except Exception as e:
            raise Exception(f"Failed to parse feed {feed.id}")
    return count


@task()
def import_feed(feed=False):
    remove_old_articles(feed)
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


def remove_old_articles(feed=None):
    if feed:
        articles = Article.objects.filter(feed_id=feed)
    else:
        articles = Article.objects.all()
    for article in articles:
        article.image.delete(save=False)
    articles.delete()


def download_remote_images():
    for article in Article.objects.all():
        if not article.original_image:
            continue
        try:
            result = requests.get(article.original_image, timeout=5)
        except requests.exceptions.ConnectionError as e:
            logger.exception(
                "Unable to download remote image for %s"
                % article.original_image
            )
            continue
        except Exception as e:
            logger.exception(
                "Unable to download remote image for %s"
                % article.original_image
            )
            continue

        try:
            article.image.save(
                os.path.basename(article.original_image),
                File(BytesIO(result.content)),
            )
            article.save()
        except OSError as e:
            continue

        except Exception as e:
            logger.exception(result)
            continue


def get_active_feeds(feed=False):
    if feed is not False:
        feeds = Feed.objects.filter(pk=feed)
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
