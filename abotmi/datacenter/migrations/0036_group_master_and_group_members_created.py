# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0035_auto_20160831_0512'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupMaster',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group_name', models.CharField(max_length=250, db_index=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('group_owner', models.ForeignKey(to='datacenter.UserProfile')),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='GroupMembers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('group', models.ForeignKey(to='datacenter.GroupMaster')),
                ('user_profile', models.ForeignKey(to='datacenter.UserProfile')),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.AlterUniqueTogether(
            name='groupmembers',
            unique_together=set([('group', 'user_profile')]),
        ),
    ]
