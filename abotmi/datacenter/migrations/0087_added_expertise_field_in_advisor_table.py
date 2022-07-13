# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0086_feature_data_field_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='advisor',
            name='expertise',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicaladvisor',
            name='expertise',
            field=models.TextField(null=True, blank=True),
        ),
    ]
