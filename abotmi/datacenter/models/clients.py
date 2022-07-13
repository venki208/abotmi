from django.db import models
from datacenter.models import UserProfile, Advisor
from simple_history.models import HistoricalRecords

GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
)
def client_profile_picture_name(instance, filename):
    return '/'.join(['reia/client', str(instance.id), "profile_picture.jpg"])

class ClientPlatform(models.Model):
    '''
    Desciption : To store other platform whoever need advisor service for 
                their client(example platform : uplyf, ..)
    Fields: platform_name, platform_name - represents platform,
            platform_email, is_active - activate/deactivate platform
    '''
    platform_name = models.CharField(max_length=40, unique=True, null=True, blank=True)
    platform_code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    platform_email  = models.CharField(db_index=True, max_length=250)
    is_active = models.BooleanField(default=1)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    # Historical data ===========
    history = HistoricalRecords()

    class Meta:
        app_label = 'datacenter'
        managed = True

class ClientDetails(models.Model):
    '''
    Desciption : To store clients one who want our advisor service
                 from other platform.
    Field : first_name, last_name, father_name, birth date, gender
            picture - profile pictrue of client, city, loccation, adhaar card,
            email, address, clien_platform - client from which platform (ex: uplyf, lic)
    '''
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    father_name = models.CharField(max_length=50, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    picture = models.ImageField(upload_to=client_profile_picture_name, blank=True, null=True)
    adhaar_card = models.CharField(max_length=15, blank=True)
    email = models.CharField(max_length=250, db_index=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=50, blank=True)
    client_platform = models.ForeignKey(ClientPlatform)
    is_active = models.BooleanField(default=1)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    # Historical data ===========
    history = HistoricalRecords()

    class Meta:
        app_label = 'datacenter'
        managed = True
        unique_together = (('email','client_platform'),)

class ClientAdvisorMapping(models.Model):
    '''
    Desciption : Client and Advisor mapping table
    Field : client, advisor
    '''
    client = models.ForeignKey(ClientDetails)
    user_profile = models.ForeignKey(UserProfile)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        app_label = 'datacenter'
        managed = True
        unique_together = (('client','user_profile'),)