# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-09 14:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webshop_web', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientmodel',
            name='comment',
            field=models.TextField(default=0, max_length=255),
            preserve_default=False,
        ),
    ]
