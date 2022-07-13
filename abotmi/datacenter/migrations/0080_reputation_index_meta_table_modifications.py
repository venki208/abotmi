# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0079_profile_link_wallet_package_tables'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReputationIndexMetaData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=255)),
                ('dob', models.CharField(max_length=15, null=True, blank=True)),
                ('total_languages', models.IntegerField(default=0, null=True, blank=True)),
                ('facebook_signup', models.BooleanField(default=False)),
                ('google_signup', models.BooleanField(default=False)),
                ('linkedin_signup', models.BooleanField(default=False)),
                ('direct_signup', models.BooleanField(default=False)),
                ('edu', models.TextField(null=True, blank=True)),
                ('ekyc', models.BooleanField(default=False)),
                ('pan', models.BooleanField(default=False)),
                ('no_sm_connected', models.TextField(null=True, blank=True)),
                ('years_exp', models.FloatField(default=0.0, null=True, blank=True)),
                ('clients_served', models.IntegerField(default=0, null=True, blank=True)),
                ('advisors_connected', models.IntegerField(default=0, null=True, blank=True)),
                ('eipv_verified', models.BooleanField(default=False)),
                ('crisil_verified', models.BooleanField(default=False)),
                ('irda_reg', models.BooleanField(default=False)),
                ('is_sebi', models.BooleanField(default=False)),
                ('is_rera', models.BooleanField(default=False)),
                ('no_reg_regs', models.IntegerField(default=0, null=True, blank=True)),
                ('no_reg_regs_validate', models.TextField(null=True, blank=True)),
                ('peer_rating', models.FloatField(default=0.0, null=True, blank=True)),
                ('avg_client_rating', models.FloatField(default=0.0, null=True, blank=True)),
                ('meetups_hosted', models.IntegerField(default=0, null=True, blank=True)),
                ('webinars_hosted', models.IntegerField(default=0, null=True, blank=True)),
                ('disciplinary_action', models.BooleanField(default=False)),
                ('associated_organization', models.IntegerField(default=0, null=True, blank=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('user_profile', models.ForeignKey(to='datacenter.UserProfile')),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.RemoveField(
            model_name='insurancemetadata',
            name='user_profile',
        ),
        migrations.DeleteModel(
            name='InsuranceMetaData',
        ),
    ]
