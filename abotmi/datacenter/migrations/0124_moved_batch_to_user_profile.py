# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0123_removed_sms_alert_from_advisor_removed_notification_service_from_user_profile_added_notification_service_to_userstatus_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advisor',
            name='batch_code',
        ),
        migrations.RemoveField(
            model_name='historicaladvisor',
            name='batch_code',
        ),
        migrations.AddField(
            model_name='historicaluserprofile',
            name='batch_code',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='batch_code',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
