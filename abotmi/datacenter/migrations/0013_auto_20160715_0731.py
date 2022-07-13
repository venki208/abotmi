# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0012_auto_20160711_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(db_index=True, max_length=250, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.CharField(max_length=250, db_index=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='mobile',
            field=models.CharField(max_length=20, db_index=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='secondary_email',
            field=models.CharField(db_index=True, max_length=250, blank=True),
        ),
    ]
