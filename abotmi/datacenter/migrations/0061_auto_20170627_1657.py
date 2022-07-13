# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0060_auto_20170612_1251'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(blank=True)),
                ('user_profile', models.ForeignKey(to='datacenter.UserProfile')),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ReputationIndex',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='RewardPoints',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('points', models.IntegerField(default=0)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='reputationindex',
            name='reward_type',
            field=models.ForeignKey(to='datacenter.RewardPoints'),
        ),
        migrations.AddField(
            model_name='reputationindex',
            name='user_profile',
            field=models.ForeignKey(to='datacenter.UserProfile'),
        ),
    ]
