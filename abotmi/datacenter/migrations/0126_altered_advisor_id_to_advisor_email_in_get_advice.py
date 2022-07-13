# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0125_Calendly_link_of_advisor'),
    ]

    operations = [
        migrations.RenameField(
            model_name='getadvice',
            old_name='advisor_id',
            new_name='advisor_email',
        ),
    ]
