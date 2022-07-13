# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0036_group_master_and_group_members_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='driving_license',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='driving_license_expire_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='proof_of_address',
            field=models.CharField(blank=True, max_length=50, choices=[(b'aadhaar', b'Aadhaar'), (b'passport', b'Passport'), (b'voter_id', b'Voter-ID'), (b'driving_license', b'Driving-License')]),
        ),
    ]
