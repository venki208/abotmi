'''
Author: Kantanand US
Created: 29-06-2016
'''

from django.db import models
from simple_history.models import HistoricalRecords

from datacenter.models import UserProfile

SM_SOURCE = (
	('google','Google'),
	('facebook','Facebook'),
	('linkedin','Linkedin'),
	('twitter','twitter'),
)

class SocialMedia(models.Model):
	""" This model is used to capture all the social media information the user """
	user_profile = models.ForeignKey(UserProfile, null=True, blank=True)
	sm_source = models.CharField(max_length=50, choices=SM_SOURCE)
	social_media_id = models.CharField(max_length=50, blank=True)
	title = models.CharField(max_length=50, null=True, blank=True)
	first_name = models.CharField(max_length=50, null=True, blank=True)
	middle_name = models.CharField(max_length=50, null=True, blank=True)
	last_name = models.CharField(max_length=50, null=True, blank=True)
	gender = models.CharField(max_length=50, null=True, blank=True)
	email_id = models.CharField(max_length=50, null=True, blank=True)
	mobile = models.CharField(max_length=20, null=True, blank=True)
	sm_community_details = models.TextField(null=True, blank=True)
	sm_post_details = models.TextField(null=True, blank=True)
	sm_profile_picture = models.URLField(null=True, blank=True)
	sm_other_details = models.TextField(null=True, blank=True)
	created_date = models.DateTimeField(auto_now_add = True, blank=True)
	modified_date = models.DateTimeField(auto_now = True, blank=True)
	# Historical data ===========
	history = HistoricalRecords()

	class Meta:
		app_label = 'datacenter'
		managed = True
		unique_together = (("user_profile", "sm_source"),)

	def __unicode__(self):
		return str(self.user_profile)

UserProfile.sm = property(lambda u: SocialMedia.objects.get_or_create(user_profile=u)[0])


class SocialMediaLikesShareCount(models.Model):
	""" This model is used to capture all the post url likes and shares 
		count by social media 
	"""
	user_profile = models.ForeignKey(UserProfile, null=True, blank=True)
	url = models.URLField(null=False, unique=True)
	facebook_likes = models.IntegerField(default=0, blank=True)
	facebook_shares = models.IntegerField(default=0, blank=True)
	google_plus_shares = models.IntegerField(default=0, blank=True)
	linkedin_shares = models.IntegerField(default=0, blank=True)
	total_count = models.IntegerField(default=0, blank=True)
	created_date = models.DateTimeField(auto_now_add = True, blank=True)
	modified_date = models.DateTimeField(auto_now = True, blank=True)
	# Historical data ===========
	history = HistoricalRecords()

	class Meta:
		app_label = 'datacenter'
		managed = True

	def __unicode__(self):
		return str(self.url)