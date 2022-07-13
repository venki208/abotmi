# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0101_Advisor_reputation_index_one_to_one_field_with_up'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityFollowers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('following_status', models.CharField(max_length=20, null=True, blank=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('followers', models.ForeignKey(related_name='follow_advisor_activity', blank=True, to='datacenter.UserProfile', null=True)),
                ('user_profile', models.ForeignKey(related_name='advior', blank=True, to='datacenter.UserProfile', null=True)),
            ],
            options={
                'managed': True,
            },
        ),
    ]
