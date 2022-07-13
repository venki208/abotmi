# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0100_added_pincodes_field_reputation_index'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advisorreputationindex',
            name='user_profile',
            field=models.OneToOneField(to='datacenter.UserProfile'),
        ),
    ]
