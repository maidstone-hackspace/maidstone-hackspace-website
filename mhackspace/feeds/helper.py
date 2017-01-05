# -*- coding: utf-8 -*-
from django import template
from mhackspace.feeds.models import Feed
from scaffold.readers.rss_reader import feed_reader

register = template.Library()

@register.inclusion_tag('feed_tiles.html')
def fetch_feeds():
    for feed
    rss_feeds = []
    for feed in Feed.objects.all():
        rss_feeds.append({
            'author':'Simon Ridley',
            'url': 'http://waistcoatforensicator.blogspot.com/feeds/posts/default?alt=rss'
        })

    return feed_reader(rss_feeds)
