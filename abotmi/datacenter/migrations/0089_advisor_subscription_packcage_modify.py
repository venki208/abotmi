# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0088_add_advisor_register_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='advisorsubscriptionpackageorder',
            old_name='subsciption_type',
            new_name='subscription_type',
        ),
        migrations.RenameField(
            model_name='advisorsubscriptionpackageorder',
            old_name='subsciption_value',
            new_name='subscription_value',
        ),
        migrations.RenameField(
            model_name='historicaladvisorsubscriptionpackageorder',
            old_name='subsciption_type',
            new_name='subscription_type',
        ),
        migrations.RenameField(
            model_name='historicaladvisorsubscriptionpackageorder',
            old_name='subsciption_value',
            new_name='subscription_value',
        ),
        migrations.AlterField(
            model_name='advisorsubscriptionpackageorder',
            name='payment_status',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='advisorsubscriptionpackageorder',
            name='subscription_status',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicaladvisorsubscriptionpackageorder',
            name='payment_status',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicaladvisorsubscriptionpackageorder',
            name='subscription_status',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
    ]
