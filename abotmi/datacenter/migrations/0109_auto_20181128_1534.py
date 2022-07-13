# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0108_mlegion_registered_user_count_category_is_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='advisor',
            name='govt_no',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicaladvisor',
            name='govt_no',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
