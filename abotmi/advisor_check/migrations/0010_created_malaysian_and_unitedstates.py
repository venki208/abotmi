# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advisor_check', '0009_rename_field_contact_no_to_mobile_and_member_name_to_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='MalaysianAdvisors',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('licensed_holder', models.CharField(max_length=100, null=True, blank=True)),
                ('regulated_activity', models.TextField(null=True, blank=True)),
                ('principal_company', models.CharField(max_length=100, null=True, blank=True)),
                ('licence_number', models.CharField(max_length=30, db_index=True)),
                ('licensed_since', models.CharField(max_length=20, null=True, blank=True)),
                ('status', models.CharField(max_length=15, null=True, blank=True)),
                ('remarks', models.TextField(null=True, blank=True)),
                ('source', models.CharField(max_length=150, null=True)),
                ('name', models.CharField(max_length=250, null=True, blank=True)),
                ('email', models.CharField(max_length=250, null=True, blank=True)),
                ('mobile', models.CharField(max_length=250, null=True, blank=True)),
                ('city', models.CharField(max_length=250, null=True, blank=True)),
                ('advisor_id', models.IntegerField(null=True, blank=True)),
                ('claimed_status', models.CharField(max_length=50, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='UnitedStatesAdvisors',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lic_id', models.CharField(unique=True, max_length=50)),
                ('lic_type', models.CharField(max_length=15, null=True, blank=True)),
                ('lic_issue_date', models.CharField(max_length=25, null=True, blank=True)),
                ('lic_expiry_date', models.CharField(max_length=25, null=True, blank=True)),
                ('last_name', models.CharField(max_length=50, null=True, blank=True)),
                ('middle_name', models.CharField(max_length=25, null=True, blank=True)),
                ('address', models.TextField(null=True, blank=True)),
                ('city', models.CharField(max_length=50, null=True, blank=True)),
                ('st', models.CharField(max_length=50, null=True, blank=True)),
                ('pincode', models.CharField(max_length=15, null=True, blank=True)),
                ('telephone', models.CharField(max_length=15, null=True, blank=True)),
                ('orig_st_cd', models.CharField(max_length=50, null=True, blank=True)),
                ('qual_type', models.CharField(max_length=15, null=True, blank=True)),
                ('report_date', models.CharField(max_length=25, null=True, blank=True)),
                ('source', models.CharField(max_length=150, null=True)),
                ('name', models.CharField(max_length=250, null=True, blank=True)),
                ('email', models.CharField(max_length=250, null=True, blank=True)),
                ('mobile', models.CharField(max_length=250, null=True, blank=True)),
                ('advisor_id', models.IntegerField(null=True, blank=True)),
                ('claimed_status', models.CharField(max_length=50, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'managed': True,
            },
        ),
    ]
