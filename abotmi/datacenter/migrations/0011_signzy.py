# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0010_auto_20160708_0529'),
    ]

    operations = [
        migrations.CreateModel(
            name='Signzy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('urls', models.TextField(blank=True)),
                ('extracted_data', models.TextField(blank=True)),
                ('verification_data', models.TextField(blank=True)),
                ('documents_type', models.CharField(max_length=30)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('user_profile', models.ForeignKey(to='datacenter.UserProfile')),
            ],
        ),
    ]
