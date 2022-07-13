# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0067_changes_on_affliated_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='india_pincode',
            name='pin_code',
            field=models.BigIntegerField(db_index=True),
        ),
    ]
