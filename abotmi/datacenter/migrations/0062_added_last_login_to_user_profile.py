# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0061_auto_20170627_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaluserprofile',
            name='last_login',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='last_login',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
