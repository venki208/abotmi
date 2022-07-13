# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0129_added_testimonial_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaluserprofile',
            name='my_belief',
            field=models.CharField(max_length=300, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='my_belief',
            field=models.CharField(max_length=300, null=True, blank=True),
        ),
    ]
