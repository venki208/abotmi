# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0121_changed_is_stream_user_to_is_wpb_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='user_profile',
        ),
        migrations.DeleteModel(
            name='Notification',
        ),
    ]
