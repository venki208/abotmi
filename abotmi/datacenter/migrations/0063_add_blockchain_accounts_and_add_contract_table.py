# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0062_added_last_login_to_user_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlockchainAccounts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accounts', models.CharField(max_length=50, null=True, blank=True)),
                ('accounts_password', models.CharField(max_length=50, null=True, blank=True)),
                ('accounts_creation_transaction_id', models.CharField(max_length=100, null=True, blank=True)),
                ('is_account_created', models.BooleanField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='BlockchainContracts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20, blank=True)),
                ('source_code', models.TextField(blank=True)),
                ('binary_format', models.TextField(blank=True)),
                ('contract_transaction_id', models.CharField(max_length=100, blank=True)),
                ('contract_address', models.CharField(max_length=50, blank=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='blockchainaccounts',
            name='contract_address',
            field=models.ForeignKey(to='datacenter.BlockchainContracts'),
        ),
        migrations.AddField(
            model_name='blockchainaccounts',
            name='user_profile',
            field=models.OneToOneField(to='datacenter.UserProfile'),
        ),
    ]
