# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.db import models
from django.utils import timezone
from six import python_2_unicode_compatible
from stdimage.models import StdImageField
from dynamic_filenames import FilePattern


image_variations = {"home": {"width": 530, "height": 220, "crop": True}}
upload_to_pattern = FilePattern(
    filename_pattern="{model_name}/{instance.title:slug}{ext}"
)


@python_2_unicode_compatible
class Feed(models.Model):
    home_url = models.URLField(verbose_name="Site Home Page")
    feed_url = models.URLField(verbose_name="RSS Feed URL")
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    tags = models.CharField(max_length=255, blank=True)
    image = StdImageField(
        upload_to=upload_to_pattern,
        blank=True,
        null=True,
        variations=image_variations,
    )
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Article(models.Model):
    url = models.URLField()
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    original_image = models.URLField(max_length=255, blank=True, null=True)
    image = StdImageField(
        upload_to=upload_to_pattern,
        blank=True,
        null=True,
        variations=image_variations,
    )

    description = models.TextField()
    displayed = models.BooleanField(default=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("pk",)
