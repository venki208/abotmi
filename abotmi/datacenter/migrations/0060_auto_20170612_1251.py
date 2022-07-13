# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0059_pan_number_verification_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalmeetupevent',
            name='hashed_key',
            field=models.CharField(db_index=True, max_length=50, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meetupevent',
            name='hashed_key',
            field=models.CharField(max_length=50, unique=True, null=True, blank=True),
        ),
    ]
