# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-02 06:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20160502_0640'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='Speciality',
            new_name='speciality',
        ),
    ]