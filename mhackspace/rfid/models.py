# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import uuid

from django.utils import timezone
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from mhackspace.users.models import Rfid
# just brainstorming so we can start playing with this,
# be nice to make this a 3rd party django installable app ?

# description of a device like door, print, laser cutter
class Device(models.Model):
    # user = models.ManyToMany(settings.AUTH_USER_MODEL)
    name = models.CharField(_('Device name'), max_length=255)
    identifier = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.CharField(_('Short description of what the device does'), blank=True, max_length=255)
    added_date = models.DateTimeField(default=timezone.now, editable=False)
    members = models.ManyToManyField(Rfid, through='DeviceAuth')

    def __str__(self):
        return self.name


# http://stackoverflow.com/questions/4443190/djangos-manytomany-relationship-with-additional-fields
# many to many, lookup user from rfid model then get there user_id and the device to check if auth allowed
class DeviceAuth(models.Model):
    rfid = models.ForeignKey(
        Rfid,
    )

    device = models.ForeignKey(
        Device,
    )
