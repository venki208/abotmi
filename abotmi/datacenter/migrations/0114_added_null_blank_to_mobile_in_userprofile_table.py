# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0113_altered_user_profile_id_in_usermobileotp_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaluserprofile',
            name='mobile',
            field=models.CharField(db_index=True, max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='mobile',
            field=models.CharField(db_index=True, max_length=20, null=True, blank=True),
        ),
    ]
