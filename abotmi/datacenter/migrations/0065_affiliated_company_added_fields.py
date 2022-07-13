# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0064_upwrds_migrations_for_production_2'),
    ]

    operations = [
        migrations.AddField(
            model_name='affiliatedcompany',
            name='activity',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='affiliatedcompany',
            name='authorized_capital',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='affiliatedcompany',
            name='board_of_directors',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='affiliatedcompany',
            name='branches_office_establishment',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='affiliatedcompany',
            name='class_of_company',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='affiliatedcompany',
            name='company_category',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='affiliatedcompany',
            name='company_sub_category',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='affiliatedcompany',
            name='corprate_identity_no',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='affiliatedcompany',
            name='date_of_incorporation',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='affiliatedcompany',
            name='franchisee_office_establishment',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='affiliatedcompany',
            name='membership_type',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='affiliatedcompany',
            name='number_client',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='affiliatedcompany',
            name='number_of_employee',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='affiliatedcompany',
            name='paid_up_capital',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='affiliatedcompany',
            name='registered_location',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='affiliatedcompany',
            name='registered_under_and_no',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='affiliatedcompany',
            name='registration_no',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='affiliatedcompany',
            name='segment',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
