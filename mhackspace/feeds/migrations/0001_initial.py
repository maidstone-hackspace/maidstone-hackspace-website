# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-28 18:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import stdimage.models
import stdimage.utils
import dynamic_filenames


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Article",
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
                (
                    "original_image",
                    models.URLField(blank=True, max_length=255, null=True),
                ),
                (
                    "image",
                    stdimage.models.StdImageField(
                        blank=True,
                        null=True,
                        upload_to=dynamic_filenames.FilePattern(
                            filename_pattern="{model_name}/{instance.title:slug}{ext}"
                        ),
                    ),
                ),
                ("description", models.TextField()),
                ("displayed", models.BooleanField(default=True)),
                (
                    "date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Feed",
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
                ("home_url", models.URLField(verbose_name="Site Home Page")),
                ("feed_url", models.URLField(verbose_name="RSS Feed URL")),
                ("title", models.CharField(max_length=255)),
                ("author", models.CharField(max_length=255)),
                ("tags", models.CharField(blank=True, max_length=255)),
                (
                    "image",
                    stdimage.models.StdImageField(
                        blank=True,
                        null=True,
                        upload_to=dynamic_filenames.FilePattern(
                            filename_pattern="{model_name}/{instance.title:slug}{ext}"
                        ),
                    ),
                ),
                ("enabled", models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name="article",
            name="feed",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="feeds.Feed"
            ),
        ),
    ]
