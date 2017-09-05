from celery import shared_task
from mhackspace.feeds.helper import import_feeds


@shared_task
def update_homepage_feeds():
    return import_feeds()
