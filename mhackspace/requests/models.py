# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from mhackspace.base.tasks import matrix_message


REQUEST_TYPES = (
    (0, 'Equipment request'),
    (1, 'Educational request'),
    (2, 'Training request'))


class UserRequests(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='+'
    )
    title = models.CharField(max_length=255, help_text='Whats being requested ?')
    request_type = models.IntegerField(choices=REQUEST_TYPES, null=False)
    cost = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        help_text='Leave blank, if no associated cost, or add estimated cost if not sure.'
    )
    description = models.TextField(help_text="detail of what's being requested and where it can be purchased")
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('cost',)

    def request_type_string(self):
        return REQUEST_TYPES[self.request_type][1]

# class UserRequestComments(models.Model):
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL, related_name='+')
#     comment = models.TextField()
#     created_date = models.DateTimeField(default=timezone.now)

#     class Meta:
#         ordering = ('created_date',)


def send_topic_update_email(sender, instance, **kwargs):
    matrix_message.delay('New Request - %s' % instance.title)


post_save.connect(send_topic_update_email, sender=UserRequests)
