# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advisor_check', '0002_auto_20170508_1116'),
    ]

    operations = [
        migrations.AddField(
            model_name='advisordata',
            name='advisor_type',
            field=models.TextField(default=b'other', null=True, blank=True),
        ),
    ]
