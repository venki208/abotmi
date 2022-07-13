# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0033_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='externaluser',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='externaluser',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='externaluser',
            name='rera_details',
            field=models.TextField(blank=True),
        ),
    ]
