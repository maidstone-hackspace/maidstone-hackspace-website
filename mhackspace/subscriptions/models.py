# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from stdimage.models import StdImageField


PAYMENT_TYPES = {
    'unknown': 0,
    'subscription': 1,
    'payment': 2
}

@python_2_unicode_compatible
class Payments(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        default=None,
        related_name='from_user'
    )
    user_reference = models.CharField(max_length=255)
    user_email = models.CharField(max_length=255)

    reference = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    type = models.PositiveSmallIntegerField(default=0)
    date = models.DateTimeField() 

    def lookup_payment_type(name):
        return PAYMENT_TYPES.get(name, 0)

    def get_payment_type(self):
        return self.type

    def __str__(self):
        return self.reference
