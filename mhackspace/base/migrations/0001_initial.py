# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-14 08:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import stdimage.models
import stdimage.utils
import dynamic_filenames


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BannerImages",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("url", models.URLField()),
                ("title", models.CharField(max_length=255)),
                ("displayed", models.BooleanField(default=True)),
                (
                    "original_image",
                    models.URLField(blank=True, max_length=255, null=True),
                ),
                (
                    "scaled_image",
                    stdimage.models.StdImageField(
                        blank=True,
                        null=True,
                        upload_to=dynamic_filenames.FilePattern(
                            filename_pattern="{model_name}/{instance.title:slug}{ext}"
                        ),
                    ),
                ),
                ("caption", models.TextField()),
                (
                    "date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
            ],
        )
    ]
