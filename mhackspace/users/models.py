# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from stdimage.models import StdImageField


class User(AbstractUser):
    name = models.CharField(_('Name of User'), blank=True, max_length=255)
    public = models.BooleanField(default=False, help_text='If the users email is public on post feeds')
    image = StdImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        variations={
            'profile': {
                "width": 256,
                "height": 256,
                "crop": True}})

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})


class Blurb(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='+')
    skills = models.CharField(max_length=255)
    description = models.TextField()

MEMBERSHIP_CANCELLED = 0

MEMBERSHIP_STATUS_CHOICES = (
    (0, 'Guest user'),
    (1, 'Active membership'),
    (3, 'Membership Expired'),
    (4, 'Membership Cancelled')
)

MEMBERSHIP_STRING = {
    0: 'Guest user',
    1: 'Active membership',
    3: 'Membership Expired'
}

MEMBERSHIP_STATUS = {
    'active': 1,
    'cancelled': 2
}

class Membership(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        default=None,
        related_name='user'
    )
    payment = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    date = models.DateTimeField() 
    reference = models.CharField(max_length=255)
    status = models.PositiveSmallIntegerField(default=0, choices=MEMBERSHIP_STATUS_CHOICES)
    email = models.CharField(max_length=255)

    @property
    def get_status(self):
        return MEMBERSHIP_STRING[self.status]

    def lookup_status(name):
        if not name:
            return 0
        return MEMBERSHIP_STATUS.get(name.lower(), 0)

    def __str__(self):
        return self.reference
