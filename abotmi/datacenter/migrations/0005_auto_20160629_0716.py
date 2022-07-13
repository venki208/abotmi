# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0004_userprofile_communication_email_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialMedia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sm_source', models.CharField(max_length=50, choices=[(b'google', b'Google'), (b'facebook', b'Facebook'), (b'linkedin', b'Linkedin'), (b'twitter', b'twitter')])),
                ('social_media_id', models.CharField(max_length=50, blank=True)),
                ('title', models.CharField(max_length=50, null=True, blank=True)),
                ('first_name', models.CharField(max_length=50, null=True, blank=True)),
                ('middle_name', models.CharField(max_length=50, null=True, blank=True)),
                ('last_name', models.CharField(max_length=50, null=True, blank=True)),
                ('gender', models.CharField(max_length=50, null=True, blank=True)),
                ('email_id', models.CharField(max_length=50, null=True, blank=True)),
                ('mobile', models.CharField(max_length=20, null=True, blank=True)),
                ('sm_community_details', models.TextField(null=True, blank=True)),
                ('sm_post_details', models.TextField(null=True, blank=True)),
                ('sm_profile_picture', models.URLField(null=True, blank=True)),
                ('sm_other_details', models.TextField(null=True, blank=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='member',
            name='accepted_declaration',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='member',
            name='net_worth',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='member',
            name='net_worth_as_on',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='alternate_address_line_1',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='alternate_address_line_2',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='alternate_city',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='alternate_country',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='alternate_location',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='alternate_phone_no',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='alternate_pincode',
            field=models.CharField(max_length=15, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='alternate_state',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='politically_exposed_person',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='proof_of_identity',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='related_to_pep',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='socialmedia',
            name='user_profile',
            field=models.ForeignKey(blank=True, to='datacenter.UserProfile', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='socialmedia',
            unique_together=set([('user_profile', 'sm_source')]),
        ),
    ]
