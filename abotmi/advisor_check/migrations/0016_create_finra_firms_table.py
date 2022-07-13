# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advisor_check', '0015_add_city_field_irda'),
    ]

    operations = [
        migrations.CreateModel(
            name='FinraFirms',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('crd_no', models.CharField(unique=True, max_length=20)),
                ('sec_no', models.CharField(max_length=20, null=True, blank=True)),
                ('other_names', models.TextField(null=True, blank=True)),
                ('finra_json', models.TextField(null=True, blank=True)),
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
