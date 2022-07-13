# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0127_changed_default_val_to_0_for_total_experience_in_user_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activityfollowers',
            name='followers',
            field=models.ForeignKey(related_name='follower_user_profile', blank=True, to='datacenter.UserProfile', null=True),
        ),
        migrations.AlterField(
            model_name='activityfollowers',
            name='user_profile',
            field=models.ForeignKey(related_name='followee_user_profile', blank=True, to='datacenter.UserProfile', null=True),
        ),
    ]
