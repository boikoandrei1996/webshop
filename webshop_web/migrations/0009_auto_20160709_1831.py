# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-09 18:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webshop_web', '0008_auto_20160709_1550'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imagemodel',
            name='img',
        ),
        migrations.AddField(
            model_name='imagemodel',
            name='path',
            field=models.CharField(default=0, max_length=255, unique=True),
            preserve_default=False,
        ),
    ]