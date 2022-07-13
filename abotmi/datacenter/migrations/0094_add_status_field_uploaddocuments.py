# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0093_add_highest_qualification_status_in_user_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaluploaddocuments',
            name='status',
            field=models.CharField(max_length=40, blank=True),
        ),
        migrations.AddField(
            model_name='uploaddocuments',
            name='status',
            field=models.CharField(max_length=40, blank=True),
        ),
    ]
