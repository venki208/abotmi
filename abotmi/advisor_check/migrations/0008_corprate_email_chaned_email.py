# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advisor_check', '0007_advisor_check_added_bse_table'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bsedata',
            old_name='corporate_email',
            new_name='email',
        ),
    ]
