# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models
from django.utils import timezone


REQUEST_TYPES = (
    (1, 'Equipment request'),
    (2, 'Educational request'),
    (3, 'Training request'))


class UserRequests(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='+')
    request_type = models.IntegerField(choices=REQUEST_TYPES)
    description = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('pk',)
