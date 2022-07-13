# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0107_auto_20180801_1649'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalmeetupevent',
            name='category',
            field=models.CharField(default=b'Investment', max_length=150),
        ),
        migrations.AddField(
            model_name='historicalmeetupevent',
            name='is_deleted',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='historicalmeetupevent',
            name='registered_user_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='meetupevent',
            name='category',
            field=models.CharField(default=b'Investment', max_length=150),
        ),
        migrations.AddField(
            model_name='meetupevent',
            name='is_deleted',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='meetupevent',
            name='registered_user_count',
            field=models.IntegerField(default=0),
        ),
    ]
