# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('datacenter', '0078_changed_names_client_details'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdvisorProfileShare',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, null=True, blank=True)),
                ('email', models.CharField(max_length=250, db_index=True)),
                ('viewed_date', models.DateTimeField(auto_now=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('advisor', models.ForeignKey(to='datacenter.Advisor')),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='AdvisorSubscriptionPackageOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subsciption_value', models.FloatField(default=0, null=True, blank=True)),
                ('subscription_status', models.CharField(max_length=20, null=True, blank=True)),
                ('expire_date', models.DateField(null=True, blank=True)),
                ('payment_status', models.CharField(max_length=20, null=True, blank=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='AllTransactionsDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('transaction_type', models.CharField(blank=True, max_length=10, null=True, choices=[(b'mywallet', b'mywallet'), (b'online', b'Online')])),
                ('transaction_value', models.FloatField(default=0)),
                ('credited_date', models.DateField(null=True, blank=True)),
                ('status', models.CharField(max_length=50, null=True, blank=True)),
                ('payment_response', models.TextField(null=True, blank=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('order_id', models.ForeignKey(to='datacenter.AdvisorSubscriptionPackageOrder')),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='HistoricalAdvisorSubscriptionPackageOrder',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('subsciption_value', models.FloatField(default=0, null=True, blank=True)),
                ('subscription_status', models.CharField(max_length=20, null=True, blank=True)),
                ('expire_date', models.DateField(null=True, blank=True)),
                ('payment_status', models.CharField(max_length=20, null=True, blank=True)),
                ('created_date', models.DateTimeField(null=True, editable=False, blank=True)),
                ('modified_date', models.DateTimeField(null=True, editable=False, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical advisor subscription package order',
            },
        ),
        migrations.CreateModel(
            name='HistoricalAllTransactionsDetails',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('transaction_type', models.CharField(blank=True, max_length=10, null=True, choices=[(b'mywallet', b'mywallet'), (b'online', b'Online')])),
                ('transaction_value', models.FloatField(default=0)),
                ('credited_date', models.DateField(null=True, blank=True)),
                ('status', models.CharField(max_length=50, null=True, blank=True)),
                ('payment_response', models.TextField(null=True, blank=True)),
                ('created_date', models.DateTimeField(null=True, editable=False, blank=True)),
                ('modified_date', models.DateTimeField(null=True, editable=False, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('order_id', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='datacenter.AdvisorSubscriptionPackageOrder', null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical all transactions details',
            },
        ),
        migrations.CreateModel(
            name='HistoricalMyWallet',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('wallet_name', models.CharField(max_length=20)),
                ('total_wallet', models.FloatField(default=0, null=True, blank=True)),
                ('created_date', models.DateTimeField(null=True, editable=False, blank=True)),
                ('modified_date', models.DateTimeField(null=True, editable=False, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_profile', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='datacenter.UserProfile', null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical my wallet',
            },
        ),
        migrations.CreateModel(
            name='HistoricalMywalletTransaction',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('wallet_name', models.CharField(max_length=20, null=True, blank=True)),
                ('source_wallet_type', models.CharField(max_length=20, null=True, blank=True)),
                ('credited_amount', models.FloatField(default=0, null=True, blank=True)),
                ('debited_amount', models.FloatField(default=0, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('created_date', models.DateTimeField(null=True, editable=False, blank=True)),
                ('modified_date', models.DateTimeField(null=True, editable=False, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('source_transaction', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='datacenter.AllTransactionsDetails', null=True)),
                ('user_profile', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='datacenter.UserProfile', null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical mywallet transaction',
            },
        ),
        migrations.CreateModel(
            name='HistoricalSubscriptionPackageMaster',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('package_code', models.CharField(max_length=50)),
                ('package_name', models.CharField(max_length=50)),
                ('package_amount', models.FloatField(default=0, null=True, blank=True)),
                ('package_duration', models.IntegerField(default=0, null=True, blank=True)),
                ('published', models.BooleanField(default=1)),
                ('created_date', models.DateTimeField(null=True, editable=False, blank=True)),
                ('modified_date', models.DateTimeField(null=True, editable=False, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical subscription package master',
            },
        ),
        migrations.CreateModel(
            name='MyWallet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('wallet_name', models.CharField(max_length=20)),
                ('total_wallet', models.FloatField(default=0, null=True, blank=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('user_profile', models.ForeignKey(to='datacenter.UserProfile')),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='MywalletTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('wallet_name', models.CharField(max_length=20, null=True, blank=True)),
                ('source_wallet_type', models.CharField(max_length=20, null=True, blank=True)),
                ('credited_amount', models.FloatField(default=0, null=True, blank=True)),
                ('debited_amount', models.FloatField(default=0, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('source_transaction', models.ForeignKey(blank=True, to='datacenter.AllTransactionsDetails', null=True)),
                ('user_profile', models.ForeignKey(to='datacenter.UserProfile')),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ProfileShareMapping',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('viewed_page', models.TextField(null=True, blank=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('advisor', models.ForeignKey(to='datacenter.Advisor')),
                ('viewed_user_profile', models.ForeignKey(to='datacenter.UserProfile')),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SubscriptionPackageMaster',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('package_code', models.CharField(max_length=50)),
                ('package_name', models.CharField(max_length=50)),
                ('package_amount', models.FloatField(default=0, null=True, blank=True)),
                ('package_duration', models.IntegerField(default=0, null=True, blank=True)),
                ('published', models.BooleanField(default=1)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='historicaladvisorsubscriptionpackageorder',
            name='subsciption_type',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='datacenter.SubscriptionPackageMaster', null=True),
        ),
        migrations.AddField(
            model_name='historicaladvisorsubscriptionpackageorder',
            name='user_profile',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='datacenter.UserProfile', null=True),
        ),
        migrations.AddField(
            model_name='advisorsubscriptionpackageorder',
            name='subsciption_type',
            field=models.ForeignKey(to='datacenter.SubscriptionPackageMaster'),
        ),
        migrations.AddField(
            model_name='advisorsubscriptionpackageorder',
            name='user_profile',
            field=models.ForeignKey(to='datacenter.UserProfile'),
        ),
        migrations.AlterUniqueTogether(
            name='mywallet',
            unique_together=set([('user_profile', 'wallet_name')]),
        ),
    ]
