# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0069_added_practice_details_in_advisor'),
    ]

    operations = [
        migrations.CreateModel(
            name='DigitalFootPrint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('digital_links', models.TextField(null=True, blank=True)),
                ('footprint_type', models.CharField(default=b'blog', max_length=150)),
                ('source_media', models.CharField(default=b'self', max_length=150)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('user_profile', models.ForeignKey(blank=True, to='datacenter.UserProfile', null=True)),
            ],
            options={
                'managed': True,
            },
        ),
    ]
