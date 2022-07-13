# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0068_added_db_index_to_indian_pincode'),
    ]

    operations = [
        migrations.AddField(
            model_name='advisor',
            name='practice_details',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicaladvisor',
            name='practice_details',
            field=models.TextField(null=True, blank=True),
        ),
    ]
