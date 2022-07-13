# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0104_alter_activity_follower_added_activation_key'),
    ]

    operations = [
        migrations.CreateModel(
            name='GetAdvice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question_title', models.TextField(null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('document_ids', models.TextField(null=True, blank=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('user_profile', models.ForeignKey(blank=True, to='datacenter.UserProfile', null=True)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='GiveAdvice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.TextField(null=True, blank=True)),
                ('document_ids', models.TextField(null=True, blank=True)),
                ('status', models.CharField(max_length=20, null=True, blank=True)),
                ('remarks', models.CharField(max_length=250, null=True, blank=True)),
                ('rating', models.FloatField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('question', models.ForeignKey(blank=True, to='datacenter.GetAdvice', null=True)),
                ('user_profile', models.ForeignKey(blank=True, to='datacenter.UserProfile', null=True)),
            ],
            options={
                'managed': True,
            },
        ),
    ]
