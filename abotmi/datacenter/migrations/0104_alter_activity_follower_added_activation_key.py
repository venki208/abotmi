# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0103_modified_notification_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='activityfollowers',
            name='activation_key',
            field=models.TextField(null=True, blank=True),
        ),
    ]
