# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0076_add_email_mobile_verified_field'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientAdvisorMapping',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('client', models.ForeignKey(to='datacenter.ClientDetails')),
                ('user_profile', models.ForeignKey(to='datacenter.UserProfile')),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.AlterUniqueTogether(
            name='clientadvisormapping',
            unique_together=set([('client', 'user_profile')]),
        ),
    ]
