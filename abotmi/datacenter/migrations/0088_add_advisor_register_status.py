# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0087_added_expertise_field_in_advisor_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='userstatus',
            name='amfi_status',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='userstatus',
            name='irda_status',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='userstatus',
            name='sebi_status',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
