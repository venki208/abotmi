# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0048_add_ipv_field_advisor_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='advisor',
            name='dsa_details',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicaladvisor',
            name='dsa_details',
            field=models.TextField(null=True, blank=True),
        ),
    ]
