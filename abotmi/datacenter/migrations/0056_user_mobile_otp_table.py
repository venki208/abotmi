# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0055_Aadhaartranactiontable'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMobileOtp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_profile_id', models.IntegerField(blank=True)),
                ('otp', models.CharField(max_length=10, blank=True)),
                ('mobile', models.CharField(max_length=20, null=True, blank=True)),
                ('otp_source', models.CharField(max_length=50, null=True, blank=True)),
                ('verified', models.BooleanField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'managed': True,
            },
        ),
    ]
