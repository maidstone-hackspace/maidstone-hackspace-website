# -*- coding: utf-8 -*-
from django import template
from mhackspace.feeds.models import Article

register = template.Library()

@register.inclusion_tag('feeds/list.html')
def show_feeds():
    return {'articles': Article.objects.select_related('feed').filter(displayed=True, feed__enabled=True)}
