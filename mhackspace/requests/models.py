# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.sites.models import Site
from django.db.models.signals import post_save
from martor.models import MartorField
from mhackspace.base.tasks import matrix_message


REQUEST_TYPES = (
    (0, 'Equipment request'),
    (1, 'Educational request'),
    (2, 'Training request'))


class UserRequest(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='+'
    )
    title = models.CharField(max_length=255, help_text='Whats being requested ?')
    request_type = models.IntegerField(choices=REQUEST_TYPES, null=False)
    acquired = models.BooleanField(default=False)
    cost = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text='Leave blank, if no associated cost, or add estimated cost if not sure.'
    )
    description = MartorField(help_text="detail of what's being requested and where it can be purchased")
    created_date = models.DateTimeField(default=timezone.now)

    def request_type_string(self):
        return REQUEST_TYPES[self.request_type][1]

    def get_absolute_url(self):
        return reverse(
            'requests_detail',
            kwargs={'pk': self.pk})

    class Meta:
        ordering = ('acquired', 'created_date',)


class UserRequestsComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    request = models.ForeignKey(UserRequest, on_delete=models.CASCADE)
    comment = MartorField(help_text='Your comments')
    created_date = models.DateTimeField(default=timezone.now)


def send_topic_update_email(sender, instance, **kwargs):
    matrix_message.delay(
        prefix=' - REQUEST',
        message='%s - https://%s%s' % (
            Site.objects.get_current().domain,
            instance.title,
            instance.get_absolute_url()))


post_save.connect(send_topic_update_email, sender=UserRequest)
