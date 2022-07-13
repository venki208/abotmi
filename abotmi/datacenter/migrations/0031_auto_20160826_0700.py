# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0030_advisor_sms_alert'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='is_filled_address',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='member',
            name='is_filled_identity',
            field=models.BooleanField(default=0),
        ),
    ]
