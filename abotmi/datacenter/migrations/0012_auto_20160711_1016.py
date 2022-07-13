# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0011_signzy'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='signzy',
            options={'managed': True},
        ),
    ]
