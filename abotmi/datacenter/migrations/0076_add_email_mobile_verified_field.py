# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0075_changed_default_1_repute_identity'),
    ]

    operations = [
        migrations.AddField(
            model_name='userstatus',
            name='email_verified',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='userstatus',
            name='mobile_verified',
            field=models.BooleanField(default=0),
        ),
    ]
