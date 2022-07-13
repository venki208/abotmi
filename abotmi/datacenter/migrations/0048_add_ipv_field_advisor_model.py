# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0047_added_reia_goal'),
    ]

    operations = [
        migrations.AddField(
            model_name='advisor',
            name='ipv_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='advisor',
            name='ipv_type',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicaladvisor',
            name='ipv_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicaladvisor',
            name='ipv_type',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
