# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0111_refer_friend_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermobileotp',
            name='email',
            field=models.EmailField(max_length=250, blank=True),
        ),
    ]
