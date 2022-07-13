# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0002_auto_20160614_1209'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='login_count',
            field=models.IntegerField(default=0),
        ),
    ]
