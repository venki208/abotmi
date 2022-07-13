# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0105_Get_advice_and_give_advice'),
    ]

    operations = [
        migrations.AddField(
            model_name='giveadvice',
            name='activation_key',
            field=models.TextField(null=True, blank=True),
        ),
    ]
