from django.contrib.auth.models import User
from django.db import models
from simple_history.models import HistoricalRecords

from datacenter.models import UserProfile

class Member(models.Model):
    user_profile = models.OneToOneField(UserProfile, null=True, blank=True)
    occupation = models.CharField(max_length=80, blank=True)
    office_location = models.CharField(max_length=50, blank=True)
    office_city = models.CharField(max_length=50, blank=True)
    office_website = models.CharField(max_length=100, blank=True)
    designation = models.CharField(max_length=50, blank=True)
    year_income = models.CharField(max_length=20, blank=True)
    member_questions = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add = True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now = True, blank=True, null=True)
    # member status ==================================
    is_submitted_all = models.BooleanField(default=0)
    is_register_member = models.BooleanField(default=0)
    # New Fields Added ===============================
    net_worth = models.CharField(max_length=100,blank=True,null=True)
    net_worth_as_on = models.DateField(blank=True, null=True)
    accepted_declaration = models.BooleanField(default=0)
    # according to new kyc
    place_of_birth = models.CharField(max_length=50, blank=True)
    country_of_birth = models.CharField(max_length=50, blank=True)
    # Historical data ===========
    history = HistoricalRecords()

    class Meta:
        app_label = 'datacenter'
        managed = True

    def __unicode__(self):
        return str(self.id)

UserProfile.members = property(lambda u: Member.objects.get_or_create(user_profile=u)[0])


class MemberQuestion(models.Model):
    member = models.ForeignKey(Member, null=True, blank=True)
    questions = models.TextField(blank=True)
    date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add = True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now = True, blank=True, null=True)
    # Historical data ===========
    history = HistoricalRecords()

    class Meta:
        app_label = 'datacenter'
        managed = True

    def __unicode__(self):
        return self.member.user_profile.user.username

class TrackReferrals(models.Model):
    name = models.CharField(max_length=50,blank = True,null = True)
    email = models.EmailField(max_length=70,blank=True,null=True)
    phone = models.CharField(max_length=20,blank=True,null=True)
    location = models.CharField(max_length=100,blank = True, null = True)
    products_serviced = models.CharField(max_length=30,blank=True,null=True)
    registered_financial_advisor = models.BooleanField(default=0)
    sebi_reg_no = models.CharField(max_length=30,blank=True,null=True)
    amfi_reg_no = models.CharField(max_length=30,blank=True,null=True)
    irda_reg_no = models.CharField(max_length=30,blank=True,null=True)
    crisil_verified_no = models.CharField(max_length=30,blank=True,null=True)
    know_duration = models.IntegerField(null=True,blank=True)
    believe_become_advisor = models.CharField(max_length=300,null=True,blank=True)
    referred_by = models.ForeignKey(UserProfile)
    referral_user_type = models.CharField( max_length=20, null=True)
    created_date = models.DateTimeField(auto_now_add = True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now = True, blank=True, null=True)
    # Historical data =========== un comment if you need it
    # history = HistoricalRecords()

    class Meta:
        app_label = 'datacenter'
        managed = True

    def __unicode__(self):
        return str(self.name)
