# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0115_ Education and certification details'),
    ]

    operations = [
        migrations.AddField(
            model_name='getadvice',
            name='advisor_id',
            field=models.TextField(null=True, blank=True),
        ),
    ]
