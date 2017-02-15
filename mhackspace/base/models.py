# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.db import models
from django.utils import timezone
from stdimage.models import StdImageField
from stdimage.utils import UploadToAutoSlugClassNameDir
from stdimage.validators import MinSizeValidator


class BannerImages(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=255)
    displayed = models.BooleanField(default=True)
    original_image = models.URLField(max_length=255, blank=True, null=True)
    scaled_image = StdImageField(
        upload_to=UploadToAutoSlugClassNameDir(populate_from='title'),
        blank=True,
        null=True,
        variations={
            'small': {
                "width": 600,
                "height": 300,
                "crop": True},
            'large': {
                "width": 1024,
                "height": 300,
                "crop": True}},
        validators=[
            MinSizeValidator(1200, 300)])

    caption = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
