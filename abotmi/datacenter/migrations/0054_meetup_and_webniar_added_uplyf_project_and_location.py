# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0053_auto_20170321_0508'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalmeetupevent',
            name='meetup_location',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalmeetupevent',
            name='uplyf_project',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicaltrackwebinar',
            name='uplyf_project',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meetupevent',
            name='meetup_location',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meetupevent',
            name='uplyf_project',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='trackwebinar',
            name='uplyf_project',
            field=models.TextField(null=True, blank=True),
        ),
    ]
