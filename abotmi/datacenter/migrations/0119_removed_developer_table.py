# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0118_removed_investor_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='developer',
            name='user_profile',
        ),
        migrations.RemoveField(
            model_name='historicaldeveloper',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicaldeveloper',
            name='user_profile',
        ),
        migrations.DeleteModel(
            name='Developer',
        ),
        migrations.DeleteModel(
            name='HistoricalDeveloper',
        ),
    ]
