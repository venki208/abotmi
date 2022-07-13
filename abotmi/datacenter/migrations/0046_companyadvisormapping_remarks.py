# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0045_auto_20161024_0649'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyadvisormapping',
            name='remarks',
            field=models.TextField(null=True, blank=True),
        ),
    ]
