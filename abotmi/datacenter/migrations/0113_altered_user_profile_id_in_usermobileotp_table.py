# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0112_added_email_to_usermobileotp_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermobileotp',
            name='user_profile_id',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
