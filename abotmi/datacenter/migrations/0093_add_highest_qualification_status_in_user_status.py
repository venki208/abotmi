# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0092_added_other_regulatory_field_userstatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='userstatus',
            name='highest_qualification_status',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
