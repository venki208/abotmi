# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0016_transactionsdetails_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='advisor',
            old_name='crisi_application_status',
            new_name='crisil_application_status',
        ),
    ]
