# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site
from django.utils import timezone
from stdimage.models import StdImageField
from dynamic_filenames import FilePattern
from stdimage.validators import MinSizeValidator

from spirit.comment.models import Comment
from spirit.topic.models import Topic
from wiki.models.article import ArticleRevision

from django.core.mail import EmailMessage
from django.db.models.signals import post_save
from mhackspace.base.tasks import matrix_message


upload_to_pattern = FilePattern(
    filename_pattern="{model_name}/{instance.title:slug}{ext}"
)


class BannerImage(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=255)
    displayed = models.BooleanField(default=True)
    image = StdImageField(
        upload_to=upload_to_pattern,
        variations={
            "small": {"width": 400, "height": 300, "crop": True},
            "small2x": {"width": 800, "height": 600, "crop": True},
            "medium": {"width": 800, "height": 300, "crop": True},
            "medium2x": {"width": 1600, "height": 600, "crop": True},
            "large": {"width": 1200, "height": 300, "crop": True},
            "large2x": {"width": 2400, "height": 600, "crop": True},
        },
        validators=[MinSizeValidator(2400, 600)],
    )

    caption = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


# should be done inside spirit
def send_topic_update_email(sender, instance, **kwargs):
    comments = Comment.objects.filter(topic=instance.topic)
    addresses = {comment.user.email for comment in comments}
    for user_email in addresses:
        email = EmailMessage(
            "[%s] - %s" % (settings.MSG_PREFIX, instance.topic.title),
            "A topic you have interacted with has been updated click link to see new comments %s"
            % instance.get_absolute_url(),
            "no-reply@maidstone-hackspace.org.uk",
            to=[user_email],
            headers={"Reply-To": "no-reply@maidstone-hackspace.org.uk"},
        )
        email.send()
    matrix_message.delay(
        "https://%s%s"
        % (
            Site.objects.get_current().domain,
            instance.topic.get_absolute_url(),
        )
    )


def wiki_article_updated(sender, instance, **kwargs):
    matrix_message.delay(
        "https://%s%s"
        % (
            Site.objects.get_current().domain,
            instance.article.get_absolute_url(),
        )
    )


def send_new_topic_notification(sender, instance, **kwargs):
    matrix_message.delay(
        "https://%s%s"
        % (Site.objects.get_current().domain, instance.get_absolute_url())
    )
    email = EmailMessage(
        "[%s - TOPIC] - %s" % (settings.MSG_PREFIX, instance),
        "A new topic has been created, click link to view %s"
        % instance.get_absolute_url(),
        settings.EMAIL_MAILING_LIST,
        to=[settings.EMAIL_MAILING_LIST],
        headers={"Reply-To": settings.EMAIL_MAILING_LIST},
    )
    email.send()


post_save.connect(wiki_article_updated, sender=ArticleRevision)
post_save.connect(send_topic_update_email, sender=Comment)
post_save.connect(send_new_topic_notification, sender=Topic)
