# -*- coding: utf-8 -*-
from django import template
from mhackspace.feeds.models import Feed
from scaffold.readers.rss_reader import feed_reader
from django.conf import settings

register = template.Library()

@register.inclusion_tag('partials/recapture.html')
def google_capture():
   return settings.CAPTCHA
