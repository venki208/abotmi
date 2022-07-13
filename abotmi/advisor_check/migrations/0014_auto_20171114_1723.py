# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advisor_check', '0013_created_singapore_advisor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='finraadvisors',
            name='years_of_experience',
        ),
        migrations.AddField(
            model_name='finraadvisors',
            name='alternate_name',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='finraadvisors',
            name='bc_scope',
            field=models.CharField(max_length=15, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='finraadvisors',
            name='company_crd_number',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='finraadvisors',
            name='company_state_code',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='finraadvisors',
            name='company_zip_code',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='finraadvisors',
            name='exam_details',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='finraadvisors',
            name='ia_scope',
            field=models.CharField(max_length=15, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='finraadvisors',
            name='industry_start_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='finraadvisors',
            name='last_name',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='finraadvisors',
            name='middle_name',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='finraadvisors',
            name='previous_employments',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='finraadvisors',
            name='registered_states',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='finraadvisors',
            name='registered_with_company_since',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='finraadvisors',
            name='sro_registrations',
            field=models.TextField(null=True, blank=True),
        ),
    ]
