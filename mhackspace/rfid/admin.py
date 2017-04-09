# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin import ModelAdmin

from mhackspace.rfid.models import Device, Rfid


@admin.register(Device)
class DeviceAdmin(ModelAdmin):
    list_display = ('name',)

@admin.register(Rfid)
class RfidAdmin(ModelAdmin):
    list_display = ('code',)
