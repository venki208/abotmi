# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0077_added_user_status_table'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clientdetails',
            old_name='client_address',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='clientdetails',
            old_name='client_email',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='clientdetails',
            old_name='client_mobile',
            new_name='mobile',
        ),
        migrations.RenameField(
            model_name='historicalclientdetails',
            old_name='client_address',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='historicalclientdetails',
            old_name='client_email',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='historicalclientdetails',
            old_name='client_mobile',
            new_name='mobile',
        ),
        migrations.RemoveField(
            model_name='historicalclientdetails',
            name='client_name',
        ),
        migrations.AlterField(
            model_name='clientdetails',
            name='gender',
            field=models.CharField(blank=True, max_length=10, choices=[(b'M', b'Male'), (b'F', b'Female'), (b'O', b'Other')]),
        ),
        migrations.AlterField(
            model_name='historicalclientdetails',
            name='gender',
            field=models.CharField(blank=True, max_length=10, choices=[(b'M', b'Male'), (b'F', b'Female'), (b'O', b'Other')]),
        ),
        migrations.AlterUniqueTogether(
            name='clientdetails',
            unique_together=set([('email', 'client_platform')]),
        ),
        migrations.RemoveField(
            model_name='clientdetails',
            name='client_name',
        ),
    ]
