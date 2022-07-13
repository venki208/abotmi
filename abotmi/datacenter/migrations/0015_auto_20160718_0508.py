# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0014_auto_20160715_1310'),
    ]

    operations = [
        migrations.CreateModel(
            name='CrisilCertifications',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('crisil_registration_number', models.CharField(max_length=30, null=True, blank=True)),
                ('crisil_expiry_date', models.DateField(null=True, blank=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TransactionsDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('invoice_number', models.CharField(unique=True, max_length=25, blank=True)),
                ('bank_name', models.CharField(max_length=50, null=True, blank=True)),
                ('cheque_dd_no', models.CharField(max_length=50, null=True, blank=True)),
                ('cheque_dd_date', models.DateField(null=True, blank=True)),
                ('amount', models.FloatField(default=0)),
                ('promo_code', models.CharField(max_length=20, null=True, blank=True)),
                ('discounted_amount', models.FloatField(default=0)),
                ('credited_date', models.DateField(null=True, blank=True)),
                ('status', models.CharField(blank=True, max_length=50, null=True, choices=[(b'reconciled', b'Reconciled'), (b'bounced', b'Bounced')])),
                ('transaction_type', models.CharField(blank=True, max_length=10, null=True, choices=[(b'offline', b'Offline'), (b'online', b'Online')])),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('upload_cheque_dd_id', models.ForeignKey(blank=True, to='datacenter.UploadDocuments', null=True)),
                ('user_profile', models.ForeignKey(to='datacenter.UserProfile')),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='advisor',
            name='crisi_application_status',
            field=models.CharField(default=0, max_length=50),
        ),
        migrations.AddField(
            model_name='advisor',
            name='crisil_expiry_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='crisilcertifications',
            name='advisor_id',
            field=models.ForeignKey(to='datacenter.Advisor'),
        ),
        migrations.AddField(
            model_name='crisilcertifications',
            name='transcation_id',
            field=models.ForeignKey(to='datacenter.TransactionsDetails'),
        ),
    ]
