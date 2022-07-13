# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0018_auto_20160718_0937'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='my_belief',
            field=models.CharField(default=b'Service is my motto', max_length=300, null=True, blank=True),
        ),
    ]
