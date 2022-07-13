# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0030_advisor_sms_alert'),
    ]

    operations = [
        migrations.AddField(
            model_name='advisor',
            name='my_sales',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
    ]
