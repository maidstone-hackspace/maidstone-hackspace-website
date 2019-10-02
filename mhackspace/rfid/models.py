# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import uuid

from django.utils import timezone
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from mhackspace.users.models import Rfid


class Device(models.Model):
    identifier = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    name = models.CharField(_("Device name"), max_length=255)
    description = models.CharField(
        _("Short description of what the device does"),
        blank=True,
        max_length=255,
    )
    added_date = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.name


class AccessLog(models.Model):
    rfid = models.ForeignKey(Rfid, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    success = models.BooleanField()
    access_date = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return f"{self.rfid.user} {self.device}"
