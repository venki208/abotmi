# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datacenter.models.advisor


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0039_added_voter_id_in_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='AffiliatedCompany',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company_name', models.CharField(max_length=255, blank=True)),
                ('tagline', models.CharField(max_length=90, blank=True)),
                ('website_url', models.URLField(blank=True)),
                ('objective', models.CharField(max_length=255, blank=True)),
                ('description', models.TextField(blank=True)),
                ('address', models.TextField(blank=True)),
                ('contact', models.TextField(blank=True)),
                ('social_media', models.TextField(blank=True)),
                ('logo', models.ImageField(upload_to=datacenter.models.advisor.company_logo, blank=True)),
                ('awards_or_rewards', models.TextField(blank=True)),
                ('terms_and_conditions', models.BooleanField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'managed': True,
            },
        ),
    ]
