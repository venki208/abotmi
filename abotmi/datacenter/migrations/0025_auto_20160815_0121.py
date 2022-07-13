# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0024_auto_20160804_0939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='landline',
            field=models.CharField(max_length=20, blank=True),
        ),
    ]
