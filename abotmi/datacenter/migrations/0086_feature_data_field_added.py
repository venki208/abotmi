# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0085_unique_reference_key_added_in_alltransaction_advOrder_tables'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalsubscriptionpackagemaster',
            name='feature_data',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='subscriptionpackagemaster',
            name='feature_data',
            field=models.TextField(null=True, blank=True),
        ),
    ]
