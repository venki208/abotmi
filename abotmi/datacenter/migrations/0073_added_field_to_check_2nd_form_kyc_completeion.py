# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0072_update_sessionId_char_to_text_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='advisor',
            name='is_advisor_details_submitted',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='historicaladvisor',
            name='is_advisor_details_submitted',
            field=models.BooleanField(default=0),
        ),
    ]
