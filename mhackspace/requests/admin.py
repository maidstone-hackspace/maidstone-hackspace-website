# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models
from django.contrib.admin import ModelAdmin
from draceditor.widgets import AdminDraceditorWidget
from draceditor.models import DraceditorField

from mhackspace.requests.models import UserRequests


@admin.register(UserRequests)
class RequestsAdmin(ModelAdmin):
    list_display = ('title', 'description', 'created_date')
    # list_filter = ('author', 'categories', 'members_only')


