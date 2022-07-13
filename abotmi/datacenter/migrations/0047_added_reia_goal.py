# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0046_companyadvisormapping_remarks'),
    ]

    operations = [
        migrations.AddField(
            model_name='advisor',
            name='reia_goals',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicaladvisor',
            name='reia_goals',
            field=models.TextField(null=True, blank=True),
        ),
    ]
