# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0120_removed_unwanted_from_advisor_table'),
    ]

    operations = [
        migrations.RenameField(
            model_name='advisor',
            old_name='is_stream_user',
            new_name='is_wpb_user',
        ),
        migrations.RenameField(
            model_name='historicaladvisor',
            old_name='is_stream_user',
            new_name='is_wpb_user',
        ),
    ]
