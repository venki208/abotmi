from django.db import models


class UserMobileOtp(models.Model):
    '''
    for storing otp Details of user
    user_profile_id <int>: Need to pass the UserProfileTable id
    otp* <string>: otp
    mobile <string>: Mandatory to save if OTP send to mobile
        need to pass mobile number with country code
    email <string>: Mandatory to save if OTP send to email
    otp_source <string>: mobile/email
    verified <boolean>: True/False
    verified_data <Json>: Need to pass string json
    '''
    user_profile_id = models.IntegerField(blank=True, null=True)
    otp = models.CharField(max_length=10, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=250, blank=True)
    otp_source = models.CharField(max_length=50, null=True, blank=True)
    verified = models.BooleanField(default=0)
    verify_data = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        app_label = 'datacenter'
        managed = True

    def __unicode__(self):
        return str(self.otp)


class GuestUser(models.Model):
    '''
    Description : To store guest user details
    Field : user_profile is advisor of upwrdz, name - guest name, mobile - guest mobile,
            email - guest email.
    '''
    user_profile = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(db_index=True, max_length=250, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        app_label = 'datacenter'
        managed = True
        unique_together = (('user_profile', 'email'),)
