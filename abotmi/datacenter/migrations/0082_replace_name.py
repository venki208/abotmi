# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0081_remove_auto_now_from_viewed_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='groupmembers',
            old_name='user_profile',
            new_name='group_profile_id',
        ),
        migrations.RenameField(
            model_name='historicalgroupmembers',
            old_name='user_profile',
            new_name='group_profile_id',
        ),
        migrations.AlterUniqueTogether(
            name='groupmembers',
            unique_together=set([('group', 'group_profile_id')]),
        ),
    ]
