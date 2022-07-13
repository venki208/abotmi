# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0083_subsription_pack_tables_creations'),
    ]

    operations = [
        migrations.AddField(
            model_name='advisor',
            name='amfi_start_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='advisor',
            name='irda_start_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='advisor',
            name='sebi_start_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicaladvisor',
            name='amfi_start_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicaladvisor',
            name='irda_start_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicaladvisor',
            name='sebi_start_date',
            field=models.DateField(null=True, blank=True),
        ),
    ]
