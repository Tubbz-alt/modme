# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-07 17:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ModME', '0038_session_uniqueness'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='metadata',
            unique_together=set([('condition', 'participant', 'session')]),
        ),
    ]
