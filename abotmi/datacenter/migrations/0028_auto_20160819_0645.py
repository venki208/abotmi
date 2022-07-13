# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0027_auto_20160817_0836'),
    ]

    operations = [
        migrations.AddField(
            model_name='advisorrating',
            name='feedback',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='is_alternate_address',
            field=models.CharField(max_length=10, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='landline',
            field=models.CharField(max_length=20, blank=True),
        ),
    ]
