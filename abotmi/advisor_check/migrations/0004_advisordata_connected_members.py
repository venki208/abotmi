# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advisor_check', '0003_added_advisor_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='advisordata',
            name='connected_members',
            field=models.CommaSeparatedIntegerField(max_length=200, null=True, blank=True),
        ),
    ]
