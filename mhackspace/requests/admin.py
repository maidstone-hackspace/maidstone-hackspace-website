# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models
from django.contrib.admin import ModelAdmin
from martor.widgets import AdminMartorWidget
from martor.models import MartorField

from mhackspace.requests.models import UserRequest


@admin.register(UserRequest)
class RequestsAdmin(ModelAdmin):
    list_display = ('title', 'acquired', 'description', 'created_date')


