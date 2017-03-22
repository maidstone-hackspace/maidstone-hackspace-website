# -*- coding: utf-8 -*-
from django import template

from mhackspace.blog.models import Category

register = template.Library()


@register.inclusion_tag('blog/sidebar.html')
def sidebar():
    return {'categories': Category.objects.all()}
