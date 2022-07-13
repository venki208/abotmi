# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0003_userprofile_login_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='communication_email_id',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
    ]
