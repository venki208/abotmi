# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0126_altered_advisor_id_to_advisor_email_in_get_advice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaluserprofile',
            name='total_experience',
            field=models.IntegerField(default=0, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='total_experience',
            field=models.IntegerField(default=0, blank=True),
        ),
    ]
