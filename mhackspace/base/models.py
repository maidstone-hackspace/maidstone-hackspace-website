# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.db import models
from django.utils import timezone
from stdimage.models import StdImageField
from stdimage.utils import UploadToAutoSlugClassNameDir
from stdimage.validators import MinSizeValidator


class BannerImage(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=255)
    displayed = models.BooleanField(default=True)
    image = StdImageField(
        upload_to=UploadToAutoSlugClassNameDir(populate_from='title'),
        variations={
            'small': {
                "width": 400,
                "height": 300,
                "crop": True},
            'small2x': {
                "width": 800,
                "height": 600,
                "crop": True},
            'medium': {
                "width": 800,
                "height": 300,
                "crop": True},
            'medium2x': {
                "width": 1600,
                "height": 600,
                "crop": True},
            'large': {
                "width": 1200,
                "height": 300,
                "crop": True},
            'large2x': {
                "width": 2400,
                "height": 600,
                "crop": True}},
        validators=[
            MinSizeValidator(2400, 600)])

    caption = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
