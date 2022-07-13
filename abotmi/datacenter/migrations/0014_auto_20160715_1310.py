# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0013_auto_20160715_0731'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='country_of_birth',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='member',
            name='place_of_birth',
            field=models.CharField(max_length=50, blank=True),
        ),
    ]
