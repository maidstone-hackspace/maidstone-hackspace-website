# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.conf.urls import url
from django.http import HttpResponseRedirect
from django.urls import reverse

from mhackspace.base.models import BannerImage


@admin.register(BannerImage)
class BannerImageAdmin(ModelAdmin):
    list_display = ('title', 'url', 'displayed', 'date')
