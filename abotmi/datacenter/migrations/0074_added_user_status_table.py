# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0073_added_field_to_check_2nd_form_kyc_completeion'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('my_identity_status', models.BooleanField(default=0)),
                ('my_repute_status', models.BooleanField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('user_profile', models.ForeignKey(blank=True, to='datacenter.UserProfile', null=True)),
            ],
            options={
                'managed': True,
            },
        ),
    ]
