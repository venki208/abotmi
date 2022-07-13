# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0051_crisil_isssued_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaltransactionsdetails',
            name='serial_no',
            field=models.IntegerField(default=b'0'),
        ),
        migrations.AddField(
            model_name='transactionsdetails',
            name='serial_no',
            field=models.IntegerField(default=b'0'),
        ),
    ]
