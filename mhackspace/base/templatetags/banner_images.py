# -*- coding: utf-8 -*-
from django import template
from mhackspace.base.models import BannerImage

register = template.Library()

@register.inclusion_tag('partials/banner_list.html')
def show_banner_images():
    return {'bannerlist': BannerImage.objects.all(), 'test': 'abc'}

