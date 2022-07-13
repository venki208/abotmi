# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0005_auto_20160629_0716'),
    ]

    operations = [
        migrations.AddField(
            model_name='advisor',
            name='is_rera',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='advisor',
            name='rera_details',
            field=models.TextField(blank=True),
        ),
    ]
