# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0071_add_fields_clients_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlogrecord',
            name='sessionId',
            field=models.TextField(null=True, blank=True),
        ),
    ]
