# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0021_auto_20160729_0723'),
    ]

    operations = [
        migrations.AddField(
            model_name='promocodes',
            name='code_percent',
            field=models.FloatField(default=0),
        ),
    ]
