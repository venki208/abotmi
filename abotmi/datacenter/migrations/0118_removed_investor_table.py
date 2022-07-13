# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0117_removed_unwanted_fields_in_UserProfile_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalinvestor',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalinvestor',
            name='user_profile',
        ),
        migrations.RemoveField(
            model_name='investor',
            name='user_profile',
        ),
        migrations.DeleteModel(
            name='HistoricalInvestor',
        ),
        migrations.DeleteModel(
            name='Investor',
        ),
    ]
