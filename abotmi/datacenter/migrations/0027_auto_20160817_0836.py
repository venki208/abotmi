# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('datacenter', '0026_auto_20160816_1423'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLogRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('sessionId', models.CharField(max_length=256)),
                ('requestPath', models.TextField()),
                ('requestQueryString', models.TextField()),
                ('requestVars', models.TextField()),
                ('requestMethod', models.CharField(max_length=4)),
                ('requestSecure', models.BooleanField(default=False)),
                ('requestAjax', models.BooleanField(default=False)),
                ('requestMETA', models.TextField(null=True, blank=True)),
                ('requestAddress', models.GenericIPAddressField()),
                ('viewFunction', models.CharField(max_length=256)),
                ('viewDocString', models.TextField(null=True, blank=True)),
                ('viewArgs', models.TextField()),
                ('responseCode', models.CharField(max_length=3)),
                ('responseContent', models.TextField()),
                ('requestUser', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='is_alternate_address',
            field=models.BooleanField(default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='landline',
            field=models.CharField(max_length=15, blank=True),
        ),
    ]
