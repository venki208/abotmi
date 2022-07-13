# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0050_is_escro_agent_renamed_to_is_crisil_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='crisilcertifications',
            name='crisil_issued_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalcrisilcertifications',
            name='crisil_issued_date',
            field=models.DateField(null=True, blank=True),
        ),
    ]
