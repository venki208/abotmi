# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datacenter.models.clients


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0070_create_digital_foot_print'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientdetails',
            name='adhaar_card',
            field=models.CharField(max_length=15, blank=True),
        ),
        migrations.AddField(
            model_name='clientdetails',
            name='birthdate',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='clientdetails',
            name='city',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='clientdetails',
            name='father_name',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='clientdetails',
            name='first_name',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='clientdetails',
            name='gender',
            field=models.CharField(blank=True, max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female'), (b'O', b'Other')]),
        ),
        migrations.AddField(
            model_name='clientdetails',
            name='last_name',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='clientdetails',
            name='location',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='clientdetails',
            name='picture',
            field=models.ImageField(null=True, upload_to=datacenter.models.clients.client_profile_picture_name, blank=True),
        ),
        migrations.AddField(
            model_name='historicalclientdetails',
            name='adhaar_card',
            field=models.CharField(max_length=15, blank=True),
        ),
        migrations.AddField(
            model_name='historicalclientdetails',
            name='birthdate',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalclientdetails',
            name='city',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='historicalclientdetails',
            name='father_name',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalclientdetails',
            name='first_name',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalclientdetails',
            name='gender',
            field=models.CharField(blank=True, max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female'), (b'O', b'Other')]),
        ),
        migrations.AddField(
            model_name='historicalclientdetails',
            name='last_name',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalclientdetails',
            name='location',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='historicalclientdetails',
            name='picture',
            field=models.TextField(max_length=100, null=True, blank=True),
        ),
    ]
