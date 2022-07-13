'''
author: aras
created date : 12-01-2016
updated by: Kantanand US
updated date : 11-02-2016
'''

import os
import hashlib
import datetime
import random
import json

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from datacenter.storage import OverwriteStorage
from simple_history.models import HistoricalRecords

from datacenter.constants import DEFAULT_NOTIFICATION_SETTINGS

GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
MARITAL_CHOICES = (
    ('Y', 'Yes'),
    ('N', 'No'),
    )

POI_CHOICES = (
    ('pan', 'PAN'),
    ('aadhaar', 'Aadhaar'),
    ('passport', 'Passport'),
    ('voter_id', 'Voter-ID'),
)

POA_CHOICES = (
    ('aadhaar', 'Aadhaar'),
    ('passport', 'Passport'),
    ('voter_id', 'Voter-ID'),
    ('driving_license', 'Driving-License'),
)

RESEDENTIAL_STATUS_CHOICES = (
    ('INDIAN', 'Indian'),
    ('NRI', 'NRI (Non Resident Indian)'),
    ('FOREIGNER', 'Foreigner'),
)

PEP_STATUS = (
    ('PEP', 'Politically Exposed Person'),
    ('RELATED_PEP', 'Related to PEP'),
    ('NONE', 'None'),
)


def is_regulatory_document(instance, file_type):
    if (file_type == 'sebi_certificate' or file_type == 'sebi_renewal_certificate' or
            file_type == 'amfi_certificate' or file_type == 'amfi_renewal_certificate' or
            file_type == 'irda_certificate' or file_type == 'irda_renewal_certificate' or
            file_type == 'rera_certificate' or file_type == 'rera_renewal_certificate'):
            return True
    else:
        return False


def profile_picture_name(instance, filename):
    return '/'.join(['reia', str(instance.id), "profile_picture.jpg"])


def content_file_name(instance, filename):
    file_type = str(instance.documents_type)
    regulatory_document = is_regulatory_document(instance, file_type)
    if regulatory_document:
        return '/'.join(['reia', str(instance.user_profile.id) + '/regulatory', filename])
    else:
        if not file_type == 'GET_ADVICE':
            ext = filename.split('.')[-1]
            reg_num = str(random.getrandbits(128))
            total = str(file_type)+reg_num
            filename = "%s.%s" % (total, ext)
        return '/'.join(['reia', str(instance.user_profile.id), filename])


class Country(models.Model):
    name = models.CharField(db_index=True, max_length=250, blank=True, null=True)
    dial_code = models.CharField(db_index=True, max_length=10, blank=True, null=True)
    code = models.CharField(db_index=True, max_length=4, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        app_label = 'datacenter'
        managed = True

    def __unicode__(self):
        return self.name


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)
    registration_id = models.CharField(max_length=10, blank=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    suffix = models.CharField(max_length=5, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    birthdate = models.DateField(blank=True, null=True)
    father_name = models.CharField(max_length=50, blank=True)
    mother_name = models.CharField(max_length=50, blank=True)
    marital_status = models.CharField(
        max_length=1, choices=MARITAL_CHOICES, blank=True)
    passport_no = models.CharField(max_length=15, blank=True)
    passport_valid_upto = models.DateField(null=True, blank=True)
    pan_no = models.CharField(max_length=15, blank=True)
    adhaar_card = models.CharField(max_length=15, blank=True)
    issued_on = models.DateField(null=True, blank=True)
    email = models.CharField(db_index=True, max_length=250)
    secondary_email = models.CharField(db_index=True, max_length=250, blank=True)
    mobile = models.CharField(db_index=True, max_length=20, null=True, blank=True)
    mobile2 = models.CharField(max_length=20, blank=True)
    landline = models.CharField(max_length=20, blank=True)
    # Address for Communication ==============================
    door_no = models.CharField(max_length=50, blank=True)
    street_name = models.CharField(max_length=250, blank=True)
    address = models.CharField(max_length=250, blank=True)
    locality = models.CharField(max_length=150, blank=True)
    landmark = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    pincode = models.CharField(max_length=15, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    blood_group = models.CharField(max_length=10, blank=True)
    picture = models.ImageField(upload_to=profile_picture_name, blank=True)
    source_media = models.CharField(max_length=250, blank=True)
    facebook_media = models.CharField(max_length=250, blank=True)
    google_media = models.CharField(max_length=250, blank=True)
    linkedin_media = models.CharField(max_length=250, blank=True)
    twitter_media = models.CharField(max_length=250, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    # Education Details ==============================
    qualification = models.CharField(max_length=100, blank=True)
    college_name = models.CharField(max_length=100, blank=True)
    year_passout = models.CharField(max_length=4, blank=True)
    education_category = models.CharField(max_length=30, blank=True)
    # Additional qualification in json format ========
    additional_qualification = models.TextField(blank=True)
    # Company Details  ==============================
    occupation = models.CharField(max_length=50, blank=True)
    company_name = models.CharField(max_length=80, blank=True)
    organisation_type = models.CharField(max_length=80, blank=True)
    company_address1 = models.CharField(max_length=250, blank=True)
    company_address2 = models.CharField(max_length=250, blank=True)
    company_landmark = models.CharField(max_length=100, blank=True)
    company_location = models.CharField(max_length=100, blank=True)
    company_state = models.CharField(max_length=50, blank=True)
    company_country = models.CharField(max_length=50, blank=True, null=True)
    company_locality = models.CharField(max_length=100, blank=True)
    company_city = models.CharField(max_length=50, blank=True)
    company_website = models.CharField(max_length=100, blank=True)
    company_pincode = models.CharField(max_length=15, blank=True)
    language_known = models.CharField(max_length=200, blank=True)
    designation = models.CharField(max_length=50, blank=True)
    total_experience = models.IntegerField(default=0, blank=True)
    annual_income = models.CharField(max_length=20, blank=True)
    # User Roles ==============================
    is_admin = models.BooleanField(default=0)
    is_advisor = models.BooleanField(default=0)
    is_member = models.BooleanField(default=0)
    is_crisil_admin = models.BooleanField(default=0)
    created_by = models.ForeignKey(
        User, blank=True, null=True, related_name='created_by')
    referral_code = models.CharField(max_length=50, null=True, blank=True)
    referred_by = models.ForeignKey(User, null=True, blank=True,
                                    related_name='user_referred')
    total_points = models.IntegerField(null=True, blank=True, default=0)
    languages_known_read_write = models.TextField(null=True, blank=True)
    mother_tongue = models.CharField(max_length=100, null=True, blank=True)
    primary_communication = models.CharField(max_length=10, null=True, blank=True)
    # Used to start counting user login only after the successful registrations
    login_count = models.IntegerField(default=0)
    communication_email_id = models.CharField(max_length=10, null=True, blank=True)
    # Proof Of Identity ==============================
    proof_of_identity = models.CharField(max_length=50, choices=POI_CHOICES, blank=True)
    # Proof of Address ===============================
    proof_of_address = models.CharField(max_length=50, choices=POA_CHOICES, blank=True)
    my_belief = models.CharField(
        max_length=300, blank=True, null=True)
    driving_license = models.CharField(max_length=20, null=True, blank=True)
    driving_license_expire_date = models.DateField(null=True, blank=True)
    self_description = models.TextField(null=True, blank=True)
    # user last login
    last_login = models.DateTimeField(null=True, blank=True)
    # Historical data ===========
    history = HistoricalRecords()
    # is company flag for company =============
    is_company = models.BooleanField(default=0)
    reputation_index_points = models.IntegerField(default=0, null=True, blank=True)
    # batch url(profile url)
    batch_code = models.CharField(
        max_length=50, blank=True, null=True)

    class Meta:
        app_label = 'datacenter'
        managed = True

    # override the unicode method to return the username on this model
    def __unicode__(self):
        return self.user.username

    @property
    def full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s %s' % (self.first_name, self.middle_name, self.last_name)
        return full_name.strip().replace('  ', ' ')

    def save(self, *args, **kwargs):
        if not self.batch_code:
            self.batch_code = hashlib.md5(
                str(self.id) + str(self.email)).hexdigest()
        return super(UserProfile, self).save(*args, **kwargs)

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance, email=instance.username)
            userprofile = UserProfile.objects.get(user=instance)
            userprofile.referral_code = hashlib.md5(userprofile.email).hexdigest()
            userprofile.save()
    post_save.connect(create_user_profile, sender=User)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


class UserStatus(models.Model):
    '''
     To manage number of status of user
     Field:
        user_profile - user profile object
        my_identity_status - Like to display my identity buttons to customer
        my_repute_status - Like to display my repute buttons to customer
        irda_status, amfi_status, sebi_status -- cliemed or not
    '''
    user_profile = models.ForeignKey(UserProfile, null=True, blank=True)
    mobile_verified = models.BooleanField(default=0)
    email_verified = models.BooleanField(default=0)
    my_identity_status = models.BooleanField(default=1)
    my_repute_status = models.BooleanField(default=1)
    irda_status = models.CharField(max_length=50, blank=True, null=True)
    amfi_status = models.CharField(max_length=50, blank=True, null=True)
    sebi_status = models.CharField(max_length=50, blank=True, null=True)
    regulatory_other_status = models.CharField(max_length=50, blank=True, null=True)
    highest_qualification_status = models.CharField(max_length=50, blank=True, null=True)
    # notification_service is used for to start/stop notification service to user
    notification_service = models.TextField(
        blank=True, default=json.dumps(DEFAULT_NOTIFICATION_SETTINGS))
    # system information
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        app_label = 'datacenter'
        managed = True

    UserProfile.status = property(lambda u: UserStatus.objects.get_or_create(
        user_profile=u)[0])


class EmailVerification(models.Model):
    user_profile = models.OneToOneField(UserProfile, null=True, blank=True)
    key_expires = models.DateTimeField(auto_now=True)
    activation_key = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        app_label = 'datacenter'
        managed = True


class UploadDocuments(models.Model):
    user_profile = models.ForeignKey(UserProfile, null=True, blank=True)
    documents = models.FileField(upload_to=content_file_name)
    documents_type = models.CharField(max_length=40, blank=True)
    registration_number = models.CharField(max_length=30, null=True, blank=True)
    status = models.CharField(max_length=40, blank=True)
    created_date = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    # Historical data ===========
    history = HistoricalRecords()

    class Meta:
        app_label = 'datacenter'
        managed = True


class India_Pincode(models.Model):
    '''
    please make a db file to load the initaial data with reia_pincode.sql
    `load data local infile '<path>/pin_code_master.csv' into table
    datacenter_india_pincode fields terminated by ',' enclosed by '"'
    lines terminated by '\n' (pin_code,district_name,state_name);`
    '''
    pin_code = models.BigIntegerField(db_index=True)
    state_name = models.CharField(max_length=50)
    district_name = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        app_label = 'datacenter'
        managed = True


class LoginAttempts(models.Model):
    user = models.ForeignKey(UserProfile)
    access_attempts = models.IntegerField(default=0, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        app_label = 'datacenter'
        managed = True


class Signzy(models.Model):
    urls = models.TextField(blank=True)
    extracted_data = models.TextField(blank=True)
    verification_data = models.TextField(blank=True)
    documents_type = models.CharField(max_length=30)
    user_profile = models.ForeignKey(UserProfile)
    created_date = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True
    )
    modified_date = models.DateTimeField(
        auto_now=True,
        blank=True,
        null=True
    )
    # Historical data ===========
    history = HistoricalRecords()

    class Meta:
        app_label = 'datacenter'
        managed = True


class PanNumberVerfication(models.Model):
    '''
    Used to Store Pan details which are come from thrid party
    '''
    user_profile = models.ForeignKey(UserProfile, null=True, blank=True)
    user_email = models.CharField(db_index=True, max_length=250)
    user_first_name = models.CharField(max_length=50)
    user_last_name = models.CharField(max_length=50)
    pan_number = models.CharField(max_length=20)
    nsdl_pan_details = models.CharField(max_length=300)
    pan_verified_status = models.BooleanField(default=0)
    remark = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        app_label = 'datacenter'
        managed = True


class DigitalFootPrint(models.Model):
    '''
    Digital Foot Print used to store user blogs and links and sm links
    '''
    user_profile = models.ForeignKey(UserProfile, null=True, blank=True)
    digital_links = models.TextField(null=True, blank=True)
    footprint_type = models.CharField(max_length=150, default="blog")
    source_media = models.CharField(max_length=150, default="self")
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        app_label = 'datacenter'
        managed = True

    def __unicode__(self):
        return str(self.user_profile)


class EducationAndCertificationDetails(models.Model):
    '''
    Table stores advisor's Educational and Certification detail
    '''
    user_profile = models.ForeignKey(UserProfile, null=True, blank=True)
    educational_details = models.TextField(blank=True)
    certification_details = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        app_label = 'datacenter'
        managed = True

    def __unicode__(self):
        return str(self.user_profile)
