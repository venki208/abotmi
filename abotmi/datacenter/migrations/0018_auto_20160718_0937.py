# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0017_auto_20160718_0721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advisor',
            name='crisil_application_status',
            field=models.CharField(default=b'not_applied', max_length=50),
        ),
    ]
