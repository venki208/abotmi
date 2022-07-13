# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advisor_check', '0008_corprate_email_chaned_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bsedata',
            old_name='contact_no',
            new_name='mobile',
        ),
        migrations.RenameField(
            model_name='bsedata',
            old_name='member_name',
            new_name='name',
        ),
    ]
