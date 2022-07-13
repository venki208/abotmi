# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advisor_check', '0012_remove_malaysianadvisors_licensed_holder'),
    ]

    operations = [
        migrations.CreateModel(
            name='SingaporeAdvisors',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('english_name', models.CharField(max_length=50, null=True, blank=True)),
                ('surname', models.CharField(max_length=50, null=True, blank=True)),
                ('fpas_certification', models.CharField(max_length=50, null=True, blank=True)),
                ('industry', models.CharField(max_length=50, null=True, blank=True)),
                ('experience', models.CharField(max_length=20, null=True, blank=True)),
                ('specialization', models.TextField(null=True, blank=True)),
                ('company', models.CharField(max_length=250, null=True, blank=True)),
                ('job_title', models.CharField(max_length=250, null=True, blank=True)),
                ('office_address', models.TextField(null=True, blank=True)),
                ('member_since', models.CharField(max_length=50, null=True, blank=True)),
                ('member_number', models.CharField(unique=True, max_length=20)),
                ('practitioner', models.CharField(max_length=50, null=True, blank=True)),
                ('regulatory_no', models.CharField(max_length=20, null=True, blank=True)),
                ('cfp_certified_from', models.CharField(max_length=50, null=True, blank=True)),
                ('awp_certified_from', models.CharField(max_length=50, null=True, blank=True)),
                ('afp_certified_from', models.CharField(max_length=50, null=True, blank=True)),
                ('cfp_license_number', models.CharField(max_length=50, null=True, blank=True)),
                ('member_ship_expiry_date', models.CharField(max_length=50, null=True, blank=True)),
                ('name', models.CharField(max_length=250, null=True, blank=True)),
                ('email', models.CharField(max_length=250, null=True, blank=True)),
                ('mobile', models.CharField(max_length=250, null=True, blank=True)),
                ('city', models.CharField(max_length=50, null=True, blank=True)),
                ('source', models.CharField(max_length=150, null=True)),
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
