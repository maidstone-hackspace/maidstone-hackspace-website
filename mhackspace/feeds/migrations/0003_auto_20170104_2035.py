# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-04 20:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0002_auto_20170104_2033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
