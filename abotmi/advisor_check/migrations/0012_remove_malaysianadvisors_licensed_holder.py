# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advisor_check', '0011_create_finra_advisor_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='malaysianadvisors',
            name='licensed_holder',
        ),
    ]
