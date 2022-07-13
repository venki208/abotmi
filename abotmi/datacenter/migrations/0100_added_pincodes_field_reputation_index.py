# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0099_ReputationIndex_one_to_one_field_with_up'),
    ]

    operations = [
        migrations.AddField(
            model_name='reputationindexmetadata',
            name='pincodes',
            field=models.TextField(null=True, blank=True),
        ),
    ]
