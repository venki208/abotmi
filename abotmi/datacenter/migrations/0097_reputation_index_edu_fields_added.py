# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0096_Reputation_index_meta_data_table_modifications'),
    ]

    operations = [
        migrations.AddField(
            model_name='reputationindexmetadata',
            name='education_details',
            field=models.TextField(null=True, blank=True),
        ),
    ]
