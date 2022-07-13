'''
author: araskumar
created date: 20-05-2016
'''
import random
import hashlib
from django.db import models
from simple_history.models import HistoricalRecords
from datacenter.models import UserProfile


class MeetUpEvent(models.Model):
    user_profile = models.ForeignKey(UserProfile, null=True, blank=True)
    scheduled = models.DateTimeField(null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    meetup_event_id = models.CharField(max_length=25, null=True, blank=True)
    hashed_key = models.CharField(max_length=50, unique=True, blank=True, null=True)
    description = models.CharField(max_length=800, null=True, blank=True)
    duration = models.CharField(max_length=30, null=True, blank=True)
    is_deleted = models.BooleanField(default=0)
    category = models.CharField(max_length=150, default="Investment")
    registered_user_count = models.IntegerField(default=0)
    created_date = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    # uplyf
    uplyf_project = models.TextField(blank=True, null=True)
    meetup_location = models.CharField(max_length=200, blank=True, null=True)
    meetup_landmark = models.CharField(max_length=200, blank=True, null=True)
    # Historical data ===========
    history = HistoricalRecords()

    class Meta:
        app_label = 'datacenter'
        managed = True

    def __unicode__(self):
        return self.name

    def save(
        self, force_insert=False,
        force_update=False, using=None,
        update_fields=None
    ):
        super(MeetUpEvent, self).save()

        self.save()

    def save(self, *args, **kwargs):
        if not self.hashed_key:
            salt = str(random.random())
            encypted_id = hashlib.sha1(
                self.meetup_event_id + salt
            ).hexdigest()
            self.hashed_key = encypted_id
        return super(MeetUpEvent, self).save(*args, **kwargs)
