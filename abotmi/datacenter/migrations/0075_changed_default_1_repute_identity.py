# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0074_added_user_status_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstatus',
            name='my_identity_status',
            field=models.BooleanField(default=1),
        ),
        migrations.AlterField(
            model_name='userstatus',
            name='my_repute_status',
            field=models.BooleanField(default=1),
        ),
    ]
