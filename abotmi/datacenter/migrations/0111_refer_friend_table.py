# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0110_AdvChkProfileConnectMap_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReferFriend',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150, blank=True)),
                ('email', models.EmailField(max_length=250)),
                ('friend_name', models.CharField(max_length=150, blank=True)),
                ('friend_email', models.EmailField(max_length=250, blank=True)),
            ],
        ),
    ]
