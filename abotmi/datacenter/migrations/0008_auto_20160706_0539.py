# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0007_loginattempts'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='resedential_status',
            field=models.CharField(blank=True, max_length=50, choices=[(b'INDIAN', b'Indian'), (b'NRI', b'NRI (Non Resident Indian)'), (b'FOREIGNER', b'Foreigner')]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='proof_of_identity',
            field=models.CharField(blank=True, max_length=50, choices=[(b'pan', b'PAN'), (b'aadhaar', b'Aadhaar'), (b'passport', b'Passport'), (b'voter_id', b'Voter-ID')]),
        ),
    ]
