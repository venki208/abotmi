# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0109_auto_20181128_1534'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdvChkProfileConnectMap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('advisor_chk_id', models.IntegerField(blank=True)),
                ('registration_type', models.CharField(max_length=50, blank=True)),
                ('action_type', models.CharField(max_length=30, blank=True)),
                ('email', models.EmailField(max_length=250, blank=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('user_profile', models.ForeignKey(related_name='member_profile_id', blank=True, to='datacenter.UserProfile')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='advchkprofileconnectmap',
            unique_together=set([('user_profile', 'advisor_chk_id', 'registration_type', 'action_type')]),
        ),
    ]
