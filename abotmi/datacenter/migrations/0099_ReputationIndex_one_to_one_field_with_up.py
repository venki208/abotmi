# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0098_add_wallet_field_revenue_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reputationindexmetadata',
            name='user_profile',
            field=models.OneToOneField(to='datacenter.UserProfile'),
        ),
    ]
