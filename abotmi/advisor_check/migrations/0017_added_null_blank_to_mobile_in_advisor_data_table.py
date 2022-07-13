# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advisor_check', '0016_create_finra_firms_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advisordata',
            name='mobile',
            field=models.CharField(db_index=True, max_length=20, null=True, blank=True),
        ),
    ]
