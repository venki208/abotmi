# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0119_removed_developer_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advisor',
            name='govt_no',
        ),
        migrations.RemoveField(
            model_name='advisor',
            name='ipv_type',
        ),
        migrations.RemoveField(
            model_name='advisor',
            name='is_corporate_advisor',
        ),
        migrations.RemoveField(
            model_name='advisor',
            name='profile_confirmation_mail',
        ),
        migrations.RemoveField(
            model_name='advisor',
            name='reia_level',
        ),
        migrations.RemoveField(
            model_name='historicaladvisor',
            name='govt_no',
        ),
        migrations.RemoveField(
            model_name='historicaladvisor',
            name='ipv_type',
        ),
        migrations.RemoveField(
            model_name='historicaladvisor',
            name='is_corporate_advisor',
        ),
        migrations.RemoveField(
            model_name='historicaladvisor',
            name='profile_confirmation_mail',
        ),
        migrations.RemoveField(
            model_name='historicaladvisor',
            name='reia_level',
        ),
    ]
