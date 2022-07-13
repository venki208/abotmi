# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advisor_check', '0004_advisordata_connected_members'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='advisordata',
            unique_together=set([]),
        ),
    ]
