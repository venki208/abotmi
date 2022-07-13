# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0052_added_serial_no_transcation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaltrackwebinar',
            name='starts_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='trackwebinar',
            name='starts_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
