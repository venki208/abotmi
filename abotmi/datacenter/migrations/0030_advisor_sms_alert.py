# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0029_socialmedialikessharecount'),
    ]

    operations = [
        migrations.AddField(
            model_name='advisor',
            name='sms_alert',
            field=models.BooleanField(default=1),
        ),
    ]
