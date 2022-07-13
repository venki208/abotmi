# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0043_added_users_count_in_company'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyAdvisorMapping',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('advisor_user_profile', models.ForeignKey(related_name='user_profile', to='datacenter.UserProfile')),
                ('company_user_profile', models.ForeignKey(related_name='company_profile', to='datacenter.UserProfile')),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.AlterUniqueTogether(
            name='companyadvisormapping',
            unique_together=set([('company_user_profile', 'advisor_user_profile')]),
        ),
    ]
