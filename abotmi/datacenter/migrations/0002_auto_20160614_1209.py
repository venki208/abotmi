# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='languages_known_read_write',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='mother_tongue',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='primary_communication',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
    ]
