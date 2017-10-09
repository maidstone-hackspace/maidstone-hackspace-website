from django.db import models
from django.conf import settings
from django.utils import timezone
from mhackspace.register.managers import RegisteredUserManager


class RegisteredUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+', null=True, blank=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(default=timezone.now)

    objects = RegisteredUserManager()

    class Meta:
        ordering = ('-created_at',)
