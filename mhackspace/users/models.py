# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class User(AbstractUser):
    name = models.CharField(_('Name of User'), blank=True, max_length=255)
    image = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})


class UserBlurb(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='users') 
    skills = models.CharField(max_length=255)
    description = models.TextField()


class UserMembership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL) 
    payment = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateTimeField() 
    reference = models.CharField(max_length=255)
