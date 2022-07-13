# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0080_reputation_index_meta_table_modifications'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advisorprofileshare',
            name='viewed_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
