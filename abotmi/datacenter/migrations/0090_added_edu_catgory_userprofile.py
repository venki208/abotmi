# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0089_advisor_subscription_packcage_modify'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaluserprofile',
            name='education_category',
            field=models.CharField(max_length=30, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='education_category',
            field=models.CharField(max_length=30, blank=True),
        ),
    ]
