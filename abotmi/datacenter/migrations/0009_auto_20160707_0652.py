# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0008_auto_20160706_0539'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='politically_exposed_person',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='related_to_pep',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='politically_status',
            field=models.CharField(blank=True, max_length=50, choices=[(b'PEP', b'Politically Exposed Person'), (b'RELATED_PEP', b'Related to PEP'), (b'NONE', b'None')]),
        ),
    ]
