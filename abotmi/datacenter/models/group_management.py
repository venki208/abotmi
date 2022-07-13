'''
Author: Kantanand US
Created: 01-09-2016
'''

from django.db import models
from simple_history.models import HistoricalRecords
from datacenter.models import UserProfile

class GroupMaster(models.Model):
    '''
    This GroupMaster used to Create Groups and
    Track who is creating the group
    '''
    group_name = models.CharField(db_index=True, max_length=250)
    group_owner = models.ForeignKey(UserProfile)
    created_date = models.DateTimeField(auto_now_add = True)
    modified_date = models.DateTimeField(auto_now = True)
    # Historical data ===========
    history = HistoricalRecords()

    class Meta:
        app_label = 'datacenter'
        managed = True

    def __unicode__(self):
        return self.group_name


class GroupMembers(models.Model):
    '''
    This GroupMembers is a mapping table used to map
    group and members ( advisor, member )
    '''
    group = models.ForeignKey(GroupMaster)
    group_profile_id = models.IntegerField(blank=True, null=True)
    member_type = models.CharField(max_length=150, default='advisor')
    extra_fields = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add = True)
    modified_date = models.DateTimeField(auto_now = True)
    # Historical data ===========
    history = HistoricalRecords()

    class Meta:
        app_label = 'datacenter'
        managed = True
        unique_together = (("group", "group_profile_id"),)

    def __unicode__(self):
        return str(self.group.group_name +' - '+ self.group_profile_id)