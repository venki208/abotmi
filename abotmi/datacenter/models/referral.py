'''
author: aras
created date: 21-04-2016
'''

from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

from datacenter.models import UserProfile


class UserReferral(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=10, unique=True)
    referred_by = models.ForeignKey(User)
    created_date = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(
        auto_now=True, blank=True, null=True)
    # Historical data ===========
    history = HistoricalRecords()

    class Meta:
        app_label = 'datacenter'
        managed = True

    def __unicode__(self):
        return "%s referred by %s" % (self.name, self.referred_by)


class ReferralPointsType(models.Model):
    name_type = (
        ('signup_advisor','singup_advisor'),
        ('registered_advisor','registered_advisor'),
        ('certified_advisor','certified_advisor'),
        ('crisil_advisor','crisil_advisor'),
        ('first_transcation_advisor','first_transcation_advisor'),
        ('more_than_one_transcation_advisor','more_than_one_transcation_advisor'),
        ('bonus_for_crossing_100s_advisor','bonus_for_crossing_100s_advisor'),
        ('surprise_bonus_advisor','surprise_bonus_advisor'),
    )

    level_type = (
        (1,'Parent'),
        (2,'Grand-Parent'),
    )

    name = models.CharField(max_length=250, choices=name_type, null=True, blank=True)
    points = models.IntegerField(default=0)
    level = models.IntegerField(default=0, choices=level_type, blank=True, null=True)
    created_date    = models.DateTimeField(auto_now_add = True, blank=True, null=True)
    modified_date   = models.DateTimeField(auto_now = True, blank=True, null=True)
    # Historical data ===========
    history = HistoricalRecords()

    class Meta:
        app_label = 'datacenter'
        managed = True

    def __unicode__(self):
        return str(self.id) +'-'+self.name+'- Point:'+str(self.points)

class ReferralPoints(models.Model):
    referralpointstype = models.ForeignKey(ReferralPointsType, blank=True, null=True)
    beneficiary = models.ForeignKey(UserProfile, null=True, blank=True, related_name='beneficiary')
    referred = models.ForeignKey(UserProfile, null=True, blank=True, related_name='referred')
    points = models.IntegerField(null=True, blank=True)
    created_date    = models.DateTimeField(auto_now_add = True, blank=True, null=True)
    modified_date   = models.DateTimeField(auto_now = True, blank=True, null=True)
    # Historical data ===========
    history = HistoricalRecords()

    class Meta:
        app_label = 'datacenter'
        managed = True

    def __unicode__(self):
        return str(self.id) +'- beneficiary: '+ self.beneficiary.email \
        +' - points type :'+ self.referralpointstype.name


class ReferFriend(models.Model):
    '''
    Outside(not abotmi) User can refer friend to invite into Abotmi
    name --> referrer name
    email* --> referrer email (mandatory)
    friend_name --> friends name
    friend_email --> friends email
    '''
    name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(max_length=250)
    friend_name = models.CharField(max_length=150, blank=True)
    friend_email = models.EmailField(max_length=250, blank=True)

    def __unicode__(self):
        return str(self.email)
