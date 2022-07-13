# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0034_external_user_rera_details_and_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlogrecord',
            name='sessionId',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
    ]
