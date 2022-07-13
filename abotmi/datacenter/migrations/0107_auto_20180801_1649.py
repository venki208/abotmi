# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0106_giveadvice_activation_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalmeetupevent',
            name='meetup_landmark',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meetupevent',
            name='meetup_landmark',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalmeetupevent',
            name='meetup_event_id',
            field=models.CharField(max_length=25, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='meetupevent',
            name='meetup_event_id',
            field=models.CharField(max_length=25, null=True, blank=True),
        ),
    ]
