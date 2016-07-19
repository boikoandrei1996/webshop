# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-09 15:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webshop_web', '0006_remove_ordermodel_order_datetime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imagemodel',
            name='path',
        ),
        migrations.AddField(
            model_name='imagemodel',
            name='img',
            field=models.ImageField(default=0, upload_to='images/'),
            preserve_default=False,
        ),
    ]
