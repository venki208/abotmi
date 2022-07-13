# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advisor_check', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='advisordata',
            name='advisor_id',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='advisordata',
            name='company',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='advisordata',
            name='name',
            field=models.CharField(db_index=True, max_length=255, blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='advisordata',
            unique_together=set([('name', 'mobile')]),
        ),
        migrations.RemoveField(
            model_name='advisordata',
            name='birthdate',
        ),
        migrations.RemoveField(
            model_name='advisordata',
            name='blood_group',
        ),
        migrations.RemoveField(
            model_name='advisordata',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='advisordata',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='advisordata',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='advisordata',
            name='middle_name',
        ),
    ]
