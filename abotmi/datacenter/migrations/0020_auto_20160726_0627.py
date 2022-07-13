# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0019_userprofile_my_belief'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='my_belief',
            field=models.CharField(default=b'Service is my Motto', max_length=300, null=True, blank=True),
        ),
    ]
