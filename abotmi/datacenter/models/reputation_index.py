from django.db import models
from datacenter.models import UserProfile
from datacenter.fields import JSONField


class RewardPoints(models.Model):
    '''
    Description: Saving Reward type constants with points
    name --> Reward Type
    points --> respective points for particular Reward
    ex: name --> signup_with_google : points --> 10
    '''
    name = models.CharField(max_length = 250)
    points = models.IntegerField(default=0)

    class Meta:
        app_label = 'datacenter'
        managed = True

    def __unicode__(self):
        return self.name


class ReputationIndex(models.Model):
    '''
    Description: Storing RewardPoints got by advisor
    '''
    user_profile = models.ForeignKey(UserProfile)
    reward_type = models.ForeignKey(RewardPoints)

    class Meta:
        app_label = 'datacenter'
        managed = True

    def __unicode__(self):
        return self.reward_type.name


class ReputationIndexMetaData(models.Model):
    """
    Used to Hold the Insurance Metadata
    """
    # UserProfile table related fields
    user_profile = models.OneToOneField(UserProfile)
    username = models.CharField(max_length=255)
    ekyc = models.BooleanField(default=False)
    pan = models.IntegerField(default=0, blank=True, null=True)
    # educational details json formar not json dump
    # {"deg_type":"post_doct", "year_passout":"2010", "premium_inst":false}
    education_details = models.TextField(blank=True, null=True)
    pincodes = models.TextField(blank=True,null=True)
    #Advisor table related fields
    eipv_verified = models.IntegerField(default=0, blank=True, null=True)
    is_sebi = models.BooleanField(default=False)
    is_irda = models.BooleanField(default=False)
    is_amfi = models.BooleanField(default=False)
    is_rera_reg_in_practice_state = models.IntegerField(default=0, blank=True, null=True)
    is_irda_validate = models.BooleanField(default=False)
    is_amfi_validate = models.BooleanField(default=False)
    is_sebi_validate = models.BooleanField(default=False)
    is_name_match = models.IntegerField(default=0, blank=True, null=True)
    is_reg_id_match = models.IntegerField(default=0, blank=True, null=True)
    #AdvisorRating table related fields
    client_rate_count = models.IntegerField(default=0, blank=True, null=True)
    peer_rate_count = models.IntegerField(default=0, blank=True, null=True)
    percent_peer_rating = models.FloatField(default=0.0, blank=True, null=True)
    percent_client_rating = models.FloatField(default=0.0, blank=True, null=True)
    # system related information
    created_date = models.DateTimeField(auto_now_add = True,blank=True, null=True)
    modified_date = models.DateTimeField(auto_now = True, blank=True, null=True)

    class Meta:
        app_label = 'datacenter'
        managed = True

    def __unicode__(self):
        return str(self.user_profile)

class AdvisorReputationIndex(models.Model):
    user_profile = models.OneToOneField(UserProfile)
    insurance = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add = True,blank=True, null=True)
    modified_date = models.DateTimeField(auto_now = True, blank=True, null=True)

    class Meta:
        app_label = 'datacenter'
        managed = True

    def __unicode__(self):
        return str(self.user_profile)
