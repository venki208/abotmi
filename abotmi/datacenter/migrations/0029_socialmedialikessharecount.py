# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0028_auto_20160819_0645'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialMediaLikesShareCount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(unique=True)),
                ('facebook_likes', models.IntegerField(default=0, blank=True)),
                ('facebook_shares', models.IntegerField(default=0, blank=True)),
                ('google_plus_shares', models.IntegerField(default=0, blank=True)),
                ('linkedin_shares', models.IntegerField(default=0, blank=True)),
                ('total_count', models.IntegerField(default=0, blank=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'managed': True,
            },
        ),
    ]
