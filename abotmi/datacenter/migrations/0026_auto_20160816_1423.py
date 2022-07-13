# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0025_auto_20160815_0121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='is_alternate_address',
            field=models.CharField(max_length=10, blank=True),
        ),
    ]
