# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('datacenter', '0082_replace_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeatureListMaster',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('feature_name', models.CharField(max_length=250)),
                ('feature_description', models.TextField(null=True, blank=True)),
                ('feature_short_name', models.CharField(max_length=250, null=True, blank=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='FeatureSubscriptionPkgMapping',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('feature_data', models.TextField(null=True, blank=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('feature_list', models.ForeignKey(to='datacenter.FeatureListMaster')),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='HistoricalFeatureListMaster',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('feature_name', models.CharField(max_length=250)),
                ('feature_description', models.TextField(null=True, blank=True)),
                ('feature_short_name', models.CharField(max_length=250, null=True, blank=True)),
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
                'verbose_name': 'historical feature list master',
            },
        ),
        migrations.CreateModel(
            name='HistoricalFeatureSubscriptionPkgMapping',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('feature_data', models.TextField(null=True, blank=True)),
                ('created_date', models.DateTimeField(null=True, editable=False, blank=True)),
                ('modified_date', models.DateTimeField(null=True, editable=False, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('feature_list', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='datacenter.FeatureListMaster', null=True)),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical feature subscription pkg mapping',
            },
        ),
        migrations.CreateModel(
            name='HistoricalMicroLearningVideoPkg',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('video_count', models.IntegerField(default=0, null=True, blank=True)),
                ('created_date', models.DateTimeField(null=True, editable=False, blank=True)),
                ('modified_date', models.DateTimeField(null=True, editable=False, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('advisor_subscription_pkg', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='datacenter.AdvisorSubscriptionPackageOrder', null=True)),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical micro learning video pkg',
            },
        ),
        migrations.CreateModel(
            name='HistoricalSubscriptionCategoryMaster',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('category_name', models.CharField(max_length=250, db_index=True)),
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
                'verbose_name': 'historical subscription category master',
            },
        ),
        migrations.CreateModel(
            name='MicroLearningVideoPkg',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('video_count', models.IntegerField(default=0, null=True, blank=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('advisor_subscription_pkg', models.ForeignKey(to='datacenter.AdvisorSubscriptionPackageOrder')),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SubscriptionCategoryMaster',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category_name', models.CharField(unique=True, max_length=250)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='historicalsubscriptionpackagemaster',
            name='package_description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalsubscriptionpackagemaster',
            name='package_type',
            field=models.CharField(default=b'STANDARD', max_length=50, choices=[(b'STANDARD', b'STANDARD'), (b'DELUXE', b'DELUXE'), (b'PREMIUM', b'PREMIUM'), (b'EXECUTIVE', b'EXECUTIVE'), (b'PLATINUM', b'PLATINUM')]),
        ),
        migrations.AddField(
            model_name='subscriptionpackagemaster',
            name='package_description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='subscriptionpackagemaster',
            name='package_type',
            field=models.CharField(default=b'STANDARD', max_length=50, choices=[(b'STANDARD', b'STANDARD'), (b'DELUXE', b'DELUXE'), (b'PREMIUM', b'PREMIUM'), (b'EXECUTIVE', b'EXECUTIVE'), (b'PLATINUM', b'PLATINUM')]),
        ),
        migrations.AlterField(
            model_name='historicalsubscriptionpackagemaster',
            name='package_code',
            field=models.CharField(max_length=50, db_index=True),
        ),
        migrations.AlterField(
            model_name='subscriptionpackagemaster',
            name='package_code',
            field=models.CharField(unique=True, max_length=50),
        ),
        migrations.AddField(
            model_name='historicalfeaturesubscriptionpkgmapping',
            name='subscription_pkg',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='datacenter.SubscriptionPackageMaster', null=True),
        ),
        migrations.AddField(
            model_name='historicalfeaturelistmaster',
            name='subscription_category',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='datacenter.SubscriptionCategoryMaster', null=True),
        ),
        migrations.AddField(
            model_name='featuresubscriptionpkgmapping',
            name='subscription_pkg',
            field=models.ForeignKey(to='datacenter.SubscriptionPackageMaster'),
        ),
        migrations.AddField(
            model_name='featurelistmaster',
            name='subscription_category',
            field=models.ForeignKey(to='datacenter.SubscriptionCategoryMaster'),
        ),
        migrations.AddField(
            model_name='historicalsubscriptionpackagemaster',
            name='subscription_category',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='datacenter.SubscriptionCategoryMaster', null=True),
        ),
        migrations.AddField(
            model_name='subscriptionpackagemaster',
            name='subscription_category',
            field=models.ForeignKey(blank=True, to='datacenter.SubscriptionCategoryMaster', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='featuresubscriptionpkgmapping',
            unique_together=set([('subscription_pkg', 'feature_list')]),
        ),
        migrations.AlterUniqueTogether(
            name='featurelistmaster',
            unique_together=set([('feature_name', 'feature_short_name', 'subscription_category')]),
        ),
    ]
