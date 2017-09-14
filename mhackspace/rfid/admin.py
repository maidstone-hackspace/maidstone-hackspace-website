# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.forms.models import ModelChoiceField

from mhackspace.rfid.models import Device, DeviceAuth


@admin.register(Device)
class DeviceAdmin(ModelAdmin):
    list_display = ('name', 'identifier')


# Probably need to look at this again
@admin.register(DeviceAuth)
class DeviceAuthAdmin(ModelAdmin):
    list_display = ('rfid', 'device')

    class CustomModelChoiceField(ModelChoiceField):
        def label_from_instance(self, obj):
            return obj.description + ' - ' + str(obj.user)

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "rfid":
    #         return self.CustomModelChoiceField(
    #             Rfid.objects.all(),
    #             initial=request.user)

    #     return super(DeviceAuthAdmin, self).formfield_for_foreignkey(
    #         db_field, request, **kwargs)
