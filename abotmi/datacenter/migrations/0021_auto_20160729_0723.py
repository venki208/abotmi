# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0020_auto_20160726_0627'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromoCodes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('promo_code', models.CharField(db_index=True, max_length=10, blank=True)),
                ('expiry_date', models.DateField(null=True, blank=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='country',
            name='code',
            field=models.CharField(db_index=True, max_length=4, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='country',
            name='dial_code',
            field=models.CharField(db_index=True, max_length=10, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='is_alternate_address',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='proof_of_address',
            field=models.CharField(blank=True, max_length=50, choices=[(b'aadhaar', b'Aadhaar'), (b'passport', b'Passport'), (b'voter_id', b'Voter-ID')]),
        ),
        migrations.AddField(
            model_name='promocodes',
            name='user_profile',
            field=models.ForeignKey(to='datacenter.UserProfile'),
        ),
    ]
