# -*- coding: utf-8 -*-
from django import template
from mhackspace.feeds.models import Feed
from scaffold.readers.rss_reader import feed_reader

register = template.Library()

@register.inclusion_tag('feeds/list.html')
def show_feeds():
    rss_feeds = []
    for feed in Feed.objects.all():
        if feed.enabled is False:
            continue
        rss_feeds.append({
            'author': feed.author,
            'url': feed.url
        })

    result = feed_reader(rss_feeds)
    return {'feeds': [item for item in result]}
