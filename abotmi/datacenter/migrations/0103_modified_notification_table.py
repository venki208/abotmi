# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0102_activity_followers_table'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='name',
            new_name='message',
        ),
        migrations.AddField(
            model_name='notification',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='viewed_status',
            field=models.BooleanField(default=False),
        ),
    ]
