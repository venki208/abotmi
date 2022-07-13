# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0006_auto_20160630_1006'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginAttempts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('access_attempts', models.IntegerField(default=0, blank=True)),
                ('user', models.ForeignKey(to='datacenter.UserProfile')),
            ],
            options={
                'managed': True,
            },
        ),
    ]
