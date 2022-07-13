# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0097_reputation_index_edu_fields_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalrevenuetype',
            name='is_wallet',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='revenuetype',
            name='is_wallet',
            field=models.BooleanField(default=0),
        ),
    ]
