# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0038_historicaladvisor_historicaladvisorranking_historicaladvisorrating_historicalallocation_historicalbl'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaluserprofile',
            name='voter_id',
            field=models.CharField(max_length=25, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='voter_id',
            field=models.CharField(max_length=25, blank=True),
        ),
    ]
