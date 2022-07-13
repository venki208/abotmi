# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0044_added_company_advisor_mapping'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyadvisormapping',
            name='status',
            field=models.CharField(max_length=24, null=True, blank=True),
        ),
    ]
