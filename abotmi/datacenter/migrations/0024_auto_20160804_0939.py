# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0023_advisor_is_honorable_advisor'),
    ]

    operations = [
        migrations.AddField(
            model_name='advisor',
            name='total_advisors_connected',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='advisor',
            name='total_clients_served',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
    ]
