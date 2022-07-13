# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0015_auto_20160718_0508'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionsdetails',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
