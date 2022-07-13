# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0042_alter_phon_no_trackreferrals'),
    ]

    operations = [
        migrations.AddField(
            model_name='affiliatedcompany',
            name='users_count',
            field=models.IntegerField(default=0),
        ),
    ]
