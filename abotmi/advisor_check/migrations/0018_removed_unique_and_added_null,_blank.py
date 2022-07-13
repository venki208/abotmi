# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advisor_check', '0017_added_null_blank_to_mobile_in_advisor_data_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finraadvisors',
            name='crd_no',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='finrafirms',
            name='crd_no',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='malaysianadvisors',
            name='licence_number',
            field=models.CharField(db_index=True, max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='singaporeadvisors',
            name='member_number',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='unitedstatesadvisors',
            name='lic_id',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
