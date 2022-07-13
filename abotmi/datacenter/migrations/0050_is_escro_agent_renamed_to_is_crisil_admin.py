# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0049_dsa_details'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicaluserprofile',
            old_name='is_escrow_agent',
            new_name='is_crisil_admin',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='is_escrow_agent',
            new_name='is_crisil_admin',
        ),
    ]
