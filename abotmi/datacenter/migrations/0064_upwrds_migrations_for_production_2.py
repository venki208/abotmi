# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('datacenter', '0063_add_blockchain_accounts_and_add_contract_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdvisorPublishedVideo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('video_title', models.CharField(max_length=150, null=True, blank=True)),
                ('video_link', models.TextField(null=True, blank=True)),
                ('video_description', models.TextField(null=True, blank=True)),
                ('status', models.CharField(max_length=20, null=True, blank=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='AdvisorReputationIndex',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('insurance', models.TextField(null=True, blank=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='AdvisorVideoRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(max_length=20, null=True, blank=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ClientDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('client_name', models.CharField(max_length=50, null=True, blank=True)),
                ('client_email', models.CharField(max_length=250, db_index=True)),
                ('client_mobile', models.CharField(max_length=20, null=True, blank=True)),
                ('client_address', models.TextField(null=True, blank=True)),
                ('is_active', models.BooleanField(default=1)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ClientPlatform',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('platform_name', models.CharField(max_length=40, unique=True, null=True, blank=True)),
                ('platform_code', models.CharField(max_length=10, unique=True, null=True, blank=True)),
                ('platform_email', models.CharField(max_length=250, db_index=True)),
                ('is_active', models.BooleanField(default=1)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='GuestUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_profile', models.IntegerField(null=True, blank=True)),
                ('name', models.CharField(max_length=100, null=True, blank=True)),
                ('mobile', models.CharField(max_length=20, null=True, blank=True)),
                ('email', models.EmailField(db_index=True, max_length=250, null=True, blank=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='HistoricalClientDetails',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('client_name', models.CharField(max_length=50, null=True, blank=True)),
                ('client_email', models.CharField(max_length=250, db_index=True)),
                ('client_mobile', models.CharField(max_length=20, null=True, blank=True)),
                ('client_address', models.TextField(null=True, blank=True)),
                ('is_active', models.BooleanField(default=1)),
                ('created_date', models.DateTimeField(null=True, editable=False, blank=True)),
                ('modified_date', models.DateTimeField(null=True, editable=False, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('client_platform', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='datacenter.ClientPlatform', null=True)),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical client details',
            },
        ),
        migrations.CreateModel(
            name='HistoricalClientPlatform',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('platform_name', models.CharField(db_index=True, max_length=40, null=True, blank=True)),
                ('platform_code', models.CharField(db_index=True, max_length=10, null=True, blank=True)),
                ('platform_email', models.CharField(max_length=250, db_index=True)),
                ('is_active', models.BooleanField(default=1)),
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
                'verbose_name': 'historical client platform',
            },
        ),
        migrations.CreateModel(
            name='HistoricalRevenueTransactions',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('product_id', models.CharField(max_length=20, null=True, blank=True)),
                ('transaction_value', models.FloatField(default=0, null=True, blank=True)),
                ('pay_from', models.CharField(db_index=True, max_length=250, null=True, blank=True)),
                ('pay_to', models.CharField(db_index=True, max_length=250, null=True, blank=True)),
                ('source_revenue', models.FloatField(max_length=30, null=True, blank=True)),
                ('revenue_in_percentage', models.FloatField(default=0, null=True, blank=True)),
                ('revenue', models.FloatField(default=0, null=True, blank=True)),
                ('is_paid', models.BooleanField(default=0)),
                ('payment_received_date', models.DateField(null=True, blank=True)),
                ('parent_transaction_id', models.IntegerField(default=0, null=True, blank=True)),
                ('created_date', models.DateTimeField(null=True, editable=False, blank=True)),
                ('modified_date', models.DateTimeField(null=True, editable=False, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('client', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='datacenter.ClientDetails', null=True)),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical revenue transactions',
            },
        ),
        migrations.CreateModel(
            name='HistoricalRevenueType',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('revenue_name', models.CharField(db_index=True, max_length=40, blank=True)),
                ('revenue_code', models.CharField(db_index=True, max_length=10, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('is_active', models.BooleanField(default=1)),
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
                'verbose_name': 'historical revenue type',
            },
        ),
        migrations.CreateModel(
            name='HistoricalSequence',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('last_sequence', models.IntegerField(default=0, null=True, blank=True)),
                ('sequence_type', models.CharField(max_length=20, null=True, blank=True)),
                ('prefix', models.CharField(max_length=5, null=True, blank=True)),
                ('digit_len', models.CharField(max_length=5, null=True, blank=True)),
                ('remark', models.TextField(null=True, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical sequence',
            },
        ),
        migrations.CreateModel(
            name='HistoricalTypeRevenuePlatformMapping',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('revenue_percentage', models.FloatField(default=0, null=True, blank=True)),
                ('is_active', models.BooleanField(default=1)),
                ('created_date', models.DateTimeField(null=True, editable=False, blank=True)),
                ('modified_date', models.DateTimeField(null=True, editable=False, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('platform', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='datacenter.ClientPlatform', null=True)),
                ('receiver', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='datacenter.ClientPlatform', null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical type revenue platform mapping',
            },
        ),
        migrations.CreateModel(
            name='InsuranceMetaData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=255)),
                ('dob', models.CharField(max_length=15, null=True, blank=True)),
                ('years_exp', models.FloatField(default=0.0, null=True, blank=True)),
                ('total_languages', models.IntegerField(default=0, null=True, blank=True)),
                ('clients_served', models.IntegerField(default=0, null=True, blank=True)),
                ('advisors_connected', models.IntegerField(default=0, null=True, blank=True)),
                ('peer_rating', models.FloatField(default=0.0, null=True, blank=True)),
                ('meetups_hosted', models.IntegerField(default=0, null=True, blank=True)),
                ('webinars_hosted', models.IntegerField(default=0, null=True, blank=True)),
                ('eipv_verified', models.BooleanField(default=False)),
                ('facebook_signup', models.BooleanField(default=False)),
                ('google_signup', models.BooleanField(default=False)),
                ('linkedin_signup', models.BooleanField(default=False)),
                ('direct_signup', models.BooleanField(default=False)),
                ('crisil_verified', models.BooleanField(default=False)),
                ('irda_reg', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='RevenueTransactions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product_id', models.CharField(max_length=20, null=True, blank=True)),
                ('transaction_value', models.FloatField(default=0, null=True, blank=True)),
                ('pay_from', models.CharField(db_index=True, max_length=250, null=True, blank=True)),
                ('pay_to', models.CharField(db_index=True, max_length=250, null=True, blank=True)),
                ('source_revenue', models.FloatField(max_length=30, null=True, blank=True)),
                ('revenue_in_percentage', models.FloatField(default=0, null=True, blank=True)),
                ('revenue', models.FloatField(default=0, null=True, blank=True)),
                ('is_paid', models.BooleanField(default=0)),
                ('payment_received_date', models.DateField(null=True, blank=True)),
                ('parent_transaction_id', models.IntegerField(default=0, null=True, blank=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('client', models.ForeignKey(blank=True, to='datacenter.ClientDetails', null=True)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='RevenueType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('revenue_name', models.CharField(unique=True, max_length=40, blank=True)),
                ('revenue_code', models.CharField(unique=True, max_length=10, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('is_active', models.BooleanField(default=1)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Sequence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_sequence', models.IntegerField(default=0, null=True, blank=True)),
                ('sequence_type', models.CharField(max_length=20, null=True, blank=True)),
                ('prefix', models.CharField(max_length=5, null=True, blank=True)),
                ('digit_len', models.CharField(max_length=5, null=True, blank=True)),
                ('remark', models.TextField(null=True, blank=True)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TypeRevenuePlatformMapping',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('revenue_percentage', models.FloatField(default=0, null=True, blank=True)),
                ('is_active', models.BooleanField(default=1)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('platform', models.ForeignKey(related_name='payer', to='datacenter.ClientPlatform')),
                ('receiver', models.ForeignKey(related_name='receiver', blank=True, to='datacenter.ClientPlatform', null=True)),
                ('revenue_type', models.ForeignKey(to='datacenter.RevenueType')),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.RemoveField(
            model_name='advisorranking',
            name='advisor',
        ),
        migrations.RemoveField(
            model_name='advisorranking',
            name='member',
        ),
        migrations.RemoveField(
            model_name='advisorranking',
            name='transaction',
        ),
        migrations.RemoveField(
            model_name='allocation',
            name='investor',
        ),
        migrations.RemoveField(
            model_name='allocation',
            name='reingo',
        ),
        migrations.RemoveField(
            model_name='block',
            name='project',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='investor',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='reingo',
        ),
        migrations.RemoveField(
            model_name='bookinginvestment',
            name='advisor',
        ),
        migrations.RemoveField(
            model_name='bookinginvestment',
            name='member',
        ),
        migrations.RemoveField(
            model_name='bookinginvestment',
            name='opportunity',
        ),
        migrations.RemoveField(
            model_name='document',
            name='document_category',
        ),
        migrations.RemoveField(
            model_name='document',
            name='opportunity',
        ),
        migrations.RemoveField(
            model_name='fundsubcategory',
            name='category',
        ),
        migrations.RemoveField(
            model_name='historicaladvisorranking',
            name='advisor',
        ),
        migrations.RemoveField(
            model_name='historicaladvisorranking',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicaladvisorranking',
            name='member',
        ),
        migrations.RemoveField(
            model_name='historicaladvisorranking',
            name='transaction',
        ),
        migrations.RemoveField(
            model_name='historicalallocation',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalallocation',
            name='investor',
        ),
        migrations.RemoveField(
            model_name='historicalallocation',
            name='reingo',
        ),
        migrations.RemoveField(
            model_name='historicalblock',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalblock',
            name='project',
        ),
        migrations.RemoveField(
            model_name='historicalbooking',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalbooking',
            name='investor',
        ),
        migrations.RemoveField(
            model_name='historicalbooking',
            name='reingo',
        ),
        migrations.RemoveField(
            model_name='historicalbookinginvestment',
            name='advisor',
        ),
        migrations.RemoveField(
            model_name='historicalbookinginvestment',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalbookinginvestment',
            name='member',
        ),
        migrations.RemoveField(
            model_name='historicalbookinginvestment',
            name='opportunity',
        ),
        migrations.RemoveField(
            model_name='historicaldocument',
            name='document_category',
        ),
        migrations.RemoveField(
            model_name='historicaldocument',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicaldocument',
            name='opportunity',
        ),
        migrations.RemoveField(
            model_name='historicaldocumentcategories',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalissuer',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicallevel',
            name='block',
        ),
        migrations.RemoveField(
            model_name='historicallevel',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalopportunity',
            name='fund_sub_category',
        ),
        migrations.RemoveField(
            model_name='historicalopportunity',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalopportunity',
            name='issuer',
        ),
        migrations.RemoveField(
            model_name='historicalproject',
            name='developer',
        ),
        migrations.RemoveField(
            model_name='historicalproject',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalrating',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalrating',
            name='member',
        ),
        migrations.RemoveField(
            model_name='historicalrating',
            name='opportunity',
        ),
        migrations.RemoveField(
            model_name='historicalrating',
            name='rating_agency',
        ),
        migrations.RemoveField(
            model_name='historicalratingagency',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalreingo',
            name='floor',
        ),
        migrations.RemoveField(
            model_name='historicalreingo',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalresearchreports',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalresearchreports',
            name='opportunity',
        ),
        migrations.RemoveField(
            model_name='historicaluploadfile',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicaluploadfile',
            name='project',
        ),
        migrations.RemoveField(
            model_name='historicaluploadimage',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicaluploadimage',
            name='project',
        ),
        migrations.RemoveField(
            model_name='historicalwishlist',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalwishlist',
            name='investor',
        ),
        migrations.RemoveField(
            model_name='historicalwishlist',
            name='reingo',
        ),
        migrations.RemoveField(
            model_name='level',
            name='block',
        ),
        migrations.RemoveField(
            model_name='opportunity',
            name='fund_sub_category',
        ),
        migrations.RemoveField(
            model_name='opportunity',
            name='issuer',
        ),
        migrations.RemoveField(
            model_name='project',
            name='developer',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='member',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='opportunity',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='rating_agency',
        ),
        migrations.RemoveField(
            model_name='reingo',
            name='floor',
        ),
        migrations.RemoveField(
            model_name='researchreports',
            name='opportunity',
        ),
        migrations.RemoveField(
            model_name='uploadfile',
            name='project',
        ),
        migrations.RemoveField(
            model_name='uploadimage',
            name='project',
        ),
        migrations.RemoveField(
            model_name='wishlist',
            name='investor',
        ),
        migrations.RemoveField(
            model_name='wishlist',
            name='reingo',
        ),
        migrations.AddField(
            model_name='advisor',
            name='skills',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='groupmembers',
            name='extra_fields',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='groupmembers',
            name='member_type',
            field=models.CharField(default=b'advisor', max_length=150),
        ),
        migrations.AddField(
            model_name='historicaladvisor',
            name='skills',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalgroupmembers',
            name='extra_fields',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalgroupmembers',
            name='member_type',
            field=models.CharField(default=b'advisor', max_length=150),
        ),
        migrations.AddField(
            model_name='historicalsocialmedialikessharecount',
            name='user_profile',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='datacenter.UserProfile', null=True),
        ),
        migrations.AddField(
            model_name='historicaluserprofile',
            name='notification_service',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='historicaluserprofile',
            name='reputation_index_points',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicaluserprofile',
            name='self_description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='socialmedialikessharecount',
            name='user_profile',
            field=models.ForeignKey(blank=True, to='datacenter.UserProfile', null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='notification_service',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='reputation_index_points',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='self_description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='groupmembers',
            name='user_profile',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalgroupmembers',
            name='user_profile',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.DeleteModel(
            name='AdvisorRanking',
        ),
        migrations.DeleteModel(
            name='Allocation',
        ),
        migrations.DeleteModel(
            name='Block',
        ),
        migrations.DeleteModel(
            name='Booking',
        ),
        migrations.DeleteModel(
            name='BookingInvestment',
        ),
        migrations.DeleteModel(
            name='Document',
        ),
        migrations.DeleteModel(
            name='DocumentCategories',
        ),
        migrations.DeleteModel(
            name='FundCategory',
        ),
        migrations.DeleteModel(
            name='FundSubCategory',
        ),
        migrations.DeleteModel(
            name='HistoricalAdvisorRanking',
        ),
        migrations.DeleteModel(
            name='HistoricalAllocation',
        ),
        migrations.DeleteModel(
            name='HistoricalBlock',
        ),
        migrations.DeleteModel(
            name='HistoricalBooking',
        ),
        migrations.DeleteModel(
            name='HistoricalBookingInvestment',
        ),
        migrations.DeleteModel(
            name='HistoricalDocument',
        ),
        migrations.DeleteModel(
            name='HistoricalDocumentCategories',
        ),
        migrations.DeleteModel(
            name='HistoricalIssuer',
        ),
        migrations.DeleteModel(
            name='HistoricalLevel',
        ),
        migrations.DeleteModel(
            name='HistoricalOpportunity',
        ),
        migrations.DeleteModel(
            name='HistoricalProject',
        ),
        migrations.DeleteModel(
            name='HistoricalRating',
        ),
        migrations.DeleteModel(
            name='HistoricalRatingAgency',
        ),
        migrations.DeleteModel(
            name='HistoricalReingo',
        ),
        migrations.DeleteModel(
            name='HistoricalResearchReports',
        ),
        migrations.DeleteModel(
            name='HistoricalUploadFile',
        ),
        migrations.DeleteModel(
            name='HistoricalUploadImage',
        ),
        migrations.DeleteModel(
            name='HistoricalWishList',
        ),
        migrations.DeleteModel(
            name='Issuer',
        ),
        migrations.DeleteModel(
            name='Level',
        ),
        migrations.DeleteModel(
            name='Opportunity',
        ),
        migrations.DeleteModel(
            name='Project',
        ),
        migrations.DeleteModel(
            name='Rating',
        ),
        migrations.DeleteModel(
            name='RatingAgency',
        ),
        migrations.DeleteModel(
            name='Reingo',
        ),
        migrations.DeleteModel(
            name='ResearchReports',
        ),
        migrations.DeleteModel(
            name='UploadFile',
        ),
        migrations.DeleteModel(
            name='UploadImage',
        ),
        migrations.DeleteModel(
            name='WishList',
        ),
        migrations.AddField(
            model_name='revenuetransactions',
            name='revenue_platform',
            field=models.ForeignKey(blank=True, to='datacenter.TypeRevenuePlatformMapping', null=True),
        ),
        migrations.AddField(
            model_name='revenuetransactions',
            name='service_advisor',
            field=models.ForeignKey(blank=True, to='datacenter.Advisor', null=True),
        ),
        migrations.AddField(
            model_name='insurancemetadata',
            name='user_profile',
            field=models.ForeignKey(to='datacenter.UserProfile'),
        ),
        migrations.AddField(
            model_name='historicaltyperevenueplatformmapping',
            name='revenue_type',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='datacenter.RevenueType', null=True),
        ),
        migrations.AddField(
            model_name='historicalrevenuetransactions',
            name='revenue_platform',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='datacenter.TypeRevenuePlatformMapping', null=True),
        ),
        migrations.AddField(
            model_name='historicalrevenuetransactions',
            name='service_advisor',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='datacenter.Advisor', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='guestuser',
            unique_together=set([('user_profile', 'email')]),
        ),
        migrations.AddField(
            model_name='clientdetails',
            name='client_platform',
            field=models.ForeignKey(to='datacenter.ClientPlatform'),
        ),
        migrations.AddField(
            model_name='advisorvideorequest',
            name='user_profile',
            field=models.ForeignKey(blank=True, to='datacenter.UserProfile', null=True),
        ),
        migrations.AddField(
            model_name='advisorreputationindex',
            name='user_profile',
            field=models.ForeignKey(to='datacenter.UserProfile'),
        ),
        migrations.AddField(
            model_name='advisorpublishedvideo',
            name='user_profile',
            field=models.ForeignKey(blank=True, to='datacenter.UserProfile', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='typerevenueplatformmapping',
            unique_together=set([('platform', 'revenue_type')]),
        ),
        migrations.AlterUniqueTogether(
            name='clientdetails',
            unique_together=set([('client_email', 'client_platform')]),
        ),
    ]
