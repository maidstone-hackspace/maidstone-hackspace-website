# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin import ModelAdmin

from mhackspace.rfid.models import Device, AccessLog


@admin.register(Device)
class DeviceAdmin(ModelAdmin):
    filter_vertical = ('users',)
    list_display = ('name', 'identifier')


@admin.register(AccessLog)
class AccessLogAdmin(ModelAdmin):
    list_display = ('rfid', 'device', 'success')
    list_filter = ('success',)
