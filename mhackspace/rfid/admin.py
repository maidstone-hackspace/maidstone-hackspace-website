# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.forms.models import ModelChoiceField

from mhackspace.rfid.models import Device, DeviceAuth


@admin.register(Device)
class DeviceAdmin(ModelAdmin):
    list_display = ('name', 'identifier')


@admin.register(DeviceAuth)
class DeviceAuthAdmin(ModelAdmin):
    list_display = ('device', 'rfid_code', 'rfid_user', 'device_id')

    def rfid_code(self, x):
        return x.rfid.code

    def rfid_user(self, x):
        return x.rfid.user
