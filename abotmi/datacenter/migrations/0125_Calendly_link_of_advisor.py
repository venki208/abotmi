# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0124_moved_batch_to_user_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='advisor',
            name='calendly_link',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicaladvisor',
            name='calendly_link',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
    ]
