# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0094_add_status_field_uploaddocuments'),
    ]

    operations = [
        migrations.AddField(
            model_name='advisor',
            name='batch_code',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicaladvisor',
            name='batch_code',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
