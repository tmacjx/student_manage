# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-11 01:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_academy_short_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academy',
            name='short_name',
            field=models.CharField(max_length=20, unique=True, verbose_name='\u5b66\u9662\u7b80\u79f0'),
        ),
    ]