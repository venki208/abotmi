'''
author: Kantanand US
created date: 12-05-2016
'''

import datetime
from django.db import models
from simple_history.models import HistoricalRecords

from datacenter.models import UserProfile

class TrackWebinar(models.Model):
	room_id = models.CharField(max_length=10, null=True, blank=True, default="0")
	room_name = models.CharField(max_length=250, null=True, blank=True, default="None")
	room_url = models.CharField(max_length=250, null=True, blank=True)
	room_pin = models.CharField(max_length=10, null=True, blank=True)
	room_type = models.CharField(max_length=10,blank=True,default='webinar')
	starts_at = models.DateTimeField(blank=True, null=True)
	duration = models.DurationField(default=datetime.timedelta(0))
	session_id = models.CharField(max_length=10, blank=True, null=True)
	session_data = models.TextField(blank=True)
	session_ended = models.BooleanField(default=0)
	password = models.CharField(max_length=50, null=True, blank=True)
	user_profile = models.ForeignKey(UserProfile, blank=True, null=True)
	auto_login_host_url = models.TextField(null=True, blank=True)
	# uplyf project 
	uplyf_project = models.TextField(null=True, blank=True)
	created_date = models.DateTimeField(auto_now_add = True, blank=True, null=True)
	modified_date = models.DateTimeField(auto_now = True, blank=True, null=True)
	# Historical data ===========
	history = HistoricalRecords()

	class Meta:
			app_label = 'datacenter'
			managed = True

	def __unicode__(self):
		return 'Room id: '+self.room_id +' Name: '+ self.room_name
