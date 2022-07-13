# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0057_added_verify_data_user_mobile_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='aadhaartransactions',
            name='ekyc_details',
            field=models.TextField(blank=True),
        ),
    ]
