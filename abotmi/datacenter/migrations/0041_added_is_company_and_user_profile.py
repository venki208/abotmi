# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0040_affiliatedcompany'),
    ]

    operations = [
        migrations.AddField(
            model_name='affiliatedcompany',
            name='user_profile',
            field=models.OneToOneField(null=True, blank=True, to='datacenter.UserProfile'),
        ),
        migrations.AddField(
            model_name='historicaluserprofile',
            name='is_company',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='is_company',
            field=models.BooleanField(default=0),
        ),
    ]
