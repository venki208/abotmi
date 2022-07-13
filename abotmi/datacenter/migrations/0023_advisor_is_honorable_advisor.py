# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0022_promocodes_code_percent'),
    ]

    operations = [
        migrations.AddField(
            model_name='advisor',
            name='is_honorable_advisor',
            field=models.BooleanField(default=0),
        ),
    ]
