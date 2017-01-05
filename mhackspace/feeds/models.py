# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Feed(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    tags = models.CharField(max_length=255, blank=True)
    image = models.ImageField(blank=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.url

