# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0009_auto_20160707_0652'),
    ]

    operations = [
        migrations.AddField(
            model_name='loginattempts',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='loginattempts',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
