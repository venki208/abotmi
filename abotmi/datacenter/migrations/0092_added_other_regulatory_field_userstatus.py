# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0091_add_field_advisor_package_susbscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='userstatus',
            name='regulatory_other_status',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
