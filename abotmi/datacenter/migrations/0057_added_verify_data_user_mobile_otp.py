# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0056_user_mobile_otp_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermobileotp',
            name='verify_data',
            field=models.TextField(null=True, blank=True),
        ),
    ]
