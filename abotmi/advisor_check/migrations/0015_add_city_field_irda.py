# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advisor_check', '0014_auto_20171114_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='irdadata',
            name='city',
            field=models.CharField(max_length=25, null=True, blank=True),
        ),
    ]
