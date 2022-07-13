# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0054_meetup_and_webniar_added_uplyf_project_and_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='AadhaarTransactions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.CharField(max_length=250)),
                ('aadhaar_number', models.CharField(max_length=25, blank=True)),
                ('aadhaar_status_code', models.CharField(max_length=150, blank=True)),
                ('success_status', models.BooleanField(default=0)),
                ('aadhaar_reference_code', models.CharField(max_length=100, blank=True)),
                ('api_type', models.CharField(max_length=10, blank=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('user_profile', models.ForeignKey(to='datacenter.UserProfile')),
            ],
            options={
                'managed': True,
            },
        ),
    ]
