# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0095_added_batch_code_in_advisor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reputationindexmetadata',
            name='advisors_connected',
        ),
        migrations.RemoveField(
            model_name='reputationindexmetadata',
            name='associated_organization',
        ),
        migrations.RemoveField(
            model_name='reputationindexmetadata',
            name='avg_client_rating',
        ),
        migrations.RemoveField(
            model_name='reputationindexmetadata',
            name='clients_served',
        ),
        migrations.RemoveField(
            model_name='reputationindexmetadata',
            name='crisil_verified',
        ),
        migrations.RemoveField(
            model_name='reputationindexmetadata',
            name='direct_signup',
        ),
        migrations.RemoveField(
            model_name='reputationindexmetadata',
            name='disciplinary_action',
        ),
        migrations.RemoveField(
            model_name='reputationindexmetadata',
            name='dob',
        ),
        migrations.RemoveField(
            model_name='reputationindexmetadata',
            name='edu',
        ),
        migrations.RemoveField(
            model_name='reputationindexmetadata',
            name='facebook_signup',
        ),
        migrations.RemoveField(
            model_name='reputationindexmetadata',
            name='google_signup',
        ),
        migrations.RemoveField(
            model_name='reputationindexmetadata',
            name='irda_reg',
        ),
        migrations.RemoveField(
            model_name='reputationindexmetadata',
            name='is_rera',
        ),
        migrations.RemoveField(
            model_name='reputationindexmetadata',
            name='linkedin_signup',
        ),
        migrations.RemoveField(
            model_name='reputationindexmetadata',
            name='meetups_hosted',
        ),
        migrations.RemoveField(
            model_name='reputationindexmetadata',
            name='no_reg_regs',
        ),
        migrations.RemoveField(
            model_name='reputationindexmetadata',
            name='no_reg_regs_validate',
        ),
        migrations.RemoveField(
            model_name='reputationindexmetadata',
            name='no_sm_connected',
        ),
        migrations.RemoveField(
            model_name='reputationindexmetadata',
            name='peer_rating',
        ),
        migrations.RemoveField(
            model_name='reputationindexmetadata',
            name='total_languages',
        ),
        migrations.RemoveField(
            model_name='reputationindexmetadata',
            name='webinars_hosted',
        ),
        migrations.RemoveField(
            model_name='reputationindexmetadata',
            name='years_exp',
        ),
        migrations.AddField(
            model_name='reputationindexmetadata',
            name='client_rate_count',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='reputationindexmetadata',
            name='is_amfi',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reputationindexmetadata',
            name='is_amfi_validate',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reputationindexmetadata',
            name='is_irda',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reputationindexmetadata',
            name='is_irda_validate',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reputationindexmetadata',
            name='is_name_match',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='reputationindexmetadata',
            name='is_reg_id_match',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='reputationindexmetadata',
            name='is_rera_reg_in_practice_state',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='reputationindexmetadata',
            name='is_sebi_validate',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reputationindexmetadata',
            name='peer_rate_count',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='reputationindexmetadata',
            name='percent_client_rating',
            field=models.FloatField(default=0.0, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='reputationindexmetadata',
            name='percent_peer_rating',
            field=models.FloatField(default=0.0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='reputationindexmetadata',
            name='eipv_verified',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='reputationindexmetadata',
            name='pan',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
    ]
