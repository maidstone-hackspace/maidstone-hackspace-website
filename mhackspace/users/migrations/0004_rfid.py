# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-27 18:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_merge_20170226_0844'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rfid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.PositiveIntegerField()),
                ('description', models.CharField(blank=True, max_length=255, verbose_name='Short rfid description')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
