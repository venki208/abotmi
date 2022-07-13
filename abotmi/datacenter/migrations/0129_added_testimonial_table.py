# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datacenter.models.testimonial


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0128_altered_fields_follow_advisor_activity_advior_in_ActivityFollowers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('headline', models.CharField(max_length=200, blank=True)),
                ('description', models.TextField(blank=True)),
                ('picture', models.ImageField(upload_to=datacenter.models.testimonial.profile_picture_name, blank=True)),
                ('endorser', models.CharField(max_length=100, blank=True)),
                ('endorser_designation', models.CharField(max_length=100, blank=True)),
                ('endorser_company', models.CharField(max_length=100, blank=True)),
                ('status', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
