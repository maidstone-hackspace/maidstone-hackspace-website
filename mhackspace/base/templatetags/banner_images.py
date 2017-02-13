# -*- coding: utf-8 -*-
from django import template
from mhackspace.base.models import BannerImages

register = template.Library()

@register.inclusion_tag('partials/banner_list.html')
def show_banner_images():
    return {'banner_list': BannerImages.objects.filter(displayed=True)}

