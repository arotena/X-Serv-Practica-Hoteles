# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-14 17:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hoteles', '0004_auto_20160614_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentarios',
            name='hotel',
            field=models.CharField(max_length=32),
        ),
    ]
