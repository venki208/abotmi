# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0041_added_is_company_and_user_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trackreferrals',
            name='phone',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
    ]
