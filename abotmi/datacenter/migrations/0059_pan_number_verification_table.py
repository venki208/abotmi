# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0058_aadhaartransactions_ekyc_details'),
    ]

    operations = [
        migrations.CreateModel(
            name='PanNumberVerfication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_email', models.CharField(max_length=250, db_index=True)),
                ('user_first_name', models.CharField(max_length=50)),
                ('user_last_name', models.CharField(max_length=50)),
                ('pan_number', models.CharField(max_length=20)),
                ('nsdl_pan_details', models.CharField(max_length=300)),
                ('pan_verified_status', models.BooleanField(default=0)),
                ('remark', models.TextField(blank=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('user_profile', models.ForeignKey(blank=True, to='datacenter.UserProfile', null=True)),
            ],
            options={
                'managed': True,
            },
        ),
    ]
