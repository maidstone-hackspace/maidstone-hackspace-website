# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-14 17:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requests', '0008_auto_20180114_1730'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrequest',
            name='acquired',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
