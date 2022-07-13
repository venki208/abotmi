# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0066_add_chaned_field_affliated_video_request_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='advisorvideorequest',
            name='shoot_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='affiliatedcompany',
            name='company_sub_category',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='affiliatedcompany',
            name='segment',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
