# -*- coding: utf-8 -*-
from django import template
from mhackspace.feeds.models import Article
from django.db.models import Avg, F, Window
from django.db.models.functions import RowNumber

register = template.Library()


@register.inclusion_tag("feeds/list.html")
def show_feeds():
    w = Window(RowNumber(),partition_by=F("feed"), order_by=F("date").desc())

    return {
        "articles": Article.objects.select_related("feed").filter(
            displayed=True, feed__enabled=True
        ).annotate(t=w).order_by('t', 'date')
    }
