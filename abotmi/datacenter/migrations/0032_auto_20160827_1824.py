# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0031_auto_20160826_0700'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='is_filled_address',
        ),
        migrations.RemoveField(
            model_name='member',
            name='is_filled_identity',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='is_filled_address',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='is_filled_identity',
            field=models.BooleanField(default=0),
        ),
    ]
