# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0090_added_edu_catgory_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='advisorsubscriptionpackageorder',
            name='current_package_criteria',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicaladvisorsubscriptionpackageorder',
            name='current_package_criteria',
            field=models.TextField(null=True, blank=True),
        ),
    ]
