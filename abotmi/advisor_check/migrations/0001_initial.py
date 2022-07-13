# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdvisorData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=5, blank=True)),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(max_length=50, blank=True)),
                ('last_name', models.CharField(max_length=50, blank=True)),
                ('gender', models.CharField(max_length=10, blank=True)),
                ('birthdate', models.DateField(null=True, blank=True)),
                ('blood_group', models.CharField(max_length=10, blank=True)),
                ('email', models.CharField(max_length=250, db_index=True)),
                ('secondary_email', models.CharField(max_length=250, blank=True)),
                ('mobile', models.CharField(max_length=20, db_index=True)),
                ('mobile2', models.CharField(max_length=20, blank=True)),
                ('landline', models.CharField(max_length=20, blank=True)),
                ('address', models.TextField(blank=True)),
                ('city', models.CharField(max_length=50, blank=True)),
                ('state', models.CharField(max_length=50, blank=True)),
                ('country', models.CharField(default=b'India', max_length=50)),
                ('pincode', models.CharField(max_length=15, blank=True)),
                ('extra_fields', models.TextField(null=True, blank=True)),
                ('registrations', models.TextField(null=True, blank=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'managed': True,
            },
        ),
    ]
