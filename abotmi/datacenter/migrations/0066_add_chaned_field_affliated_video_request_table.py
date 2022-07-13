# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0065_affiliated_company_added_fields'),
    ]

    operations = [
        migrations.RenameField(
            model_name='affiliatedcompany',
            old_name='contact',
            new_name='domain_name',
        ),
        migrations.AddField(
            model_name='advisorvideorequest',
            name='location',
            field=models.CharField(max_length=25, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='advisorvideorequest',
            name='video_description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='advisorvideorequest',
            name='video_title',
            field=models.CharField(max_length=150, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='affiliatedcompany',
            name='contact_number',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='affiliatedcompany',
            name='authorized_capital',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='affiliatedcompany',
            name='board_of_directors',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='affiliatedcompany',
            name='paid_up_capital',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
