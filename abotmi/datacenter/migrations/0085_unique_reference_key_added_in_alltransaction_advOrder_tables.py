# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0084_add_start_date_for_sebi_irda_amfi'),
    ]

    operations = [
        migrations.AddField(
            model_name='advisorsubscriptionpackageorder',
            name='unique_reference_key',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='alltransactionsdetails',
            name='service_type',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='alltransactionsdetails',
            name='unique_reference_key',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicaladvisorsubscriptionpackageorder',
            name='unique_reference_key',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalalltransactionsdetails',
            name='service_type',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalalltransactionsdetails',
            name='unique_reference_key',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='alltransactionsdetails',
            name='order_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='historicalalltransactionsdetails',
            name='order_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterUniqueTogether(
            name='alltransactionsdetails',
            unique_together=set([('order_id', 'service_type')]),
        ),
    ]
