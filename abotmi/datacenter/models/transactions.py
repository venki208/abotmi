from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
from datacenter.models import UserProfile, UploadDocuments, AdvisorSubscriptionPackageOrder

class TransactionsDetails(models.Model):

    TR_STATUS = (
        ('reconciled', 'Reconciled'),
        ('bounced', 'Bounced'),
    )

    TR_TYPE = (
        ('offline', 'Offline'),
        ('online', 'Online'),
    )

    invoice_number = models.CharField(max_length=25, unique=True, blank=True)
    bank_name = models.CharField(max_length=50, blank=True, null=True)
    cheque_dd_no = models.CharField(max_length=50, blank=True, null=True)
    cheque_dd_date =  models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    amount = models.FloatField(default=0)
    promo_code = models.CharField(max_length=20, blank=True, null=True)
    discounted_amount = models.FloatField(default=0)
    credited_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50,
        choices=TR_STATUS, blank=True, null=True)
    transaction_type = models.CharField(max_length=10,
        choices=TR_TYPE,blank=True, null=True)
    user_profile = models.ForeignKey(UserProfile)
    upload_cheque_dd_id = models.ForeignKey(UploadDocuments, blank=True, null=True)
    serial_no = models.IntegerField(default='0')
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
        return self.user_profile.email

UserProfile.payment = property(lambda u: TransactionsDetails.objects.get_or_create(user_profile=u)[0])

class PromoCodes(models.Model):
    user_profile = models.ForeignKey(UserProfile)
    promo_code = models.CharField(db_index=True,max_length=10, blank=True)
    code_percent = models.FloatField(default=0)
    expiry_date  = models.DateField(null=True, blank=True)
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
        return self.promo_code

class AadhaarTransactions(models.Model):
    '''
    Used to store the aadhaar TransactionsDetails status data
    '''
    user_profile = models.ForeignKey(UserProfile)
    email = models.CharField(max_length=250)
    aadhaar_number = models.CharField(max_length=25, blank=True)
    aadhaar_status_code = models.CharField(max_length=150, blank=True)
    success_status = models.BooleanField(default=0)
    aadhaar_reference_code = models.CharField(max_length=100, blank=True)
    api_type = models.CharField(max_length=10, blank=True)
    ekyc_details = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add = True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now = True, blank=True, null=True)

    class Meta:
        app_label = 'datacenter'
        managed = True

class AllTransactionsDetails(models.Model):

    TR_TYPE = (
        ('mywallet', 'mywallet'),
        ('online', 'Online'),
    )

    order_id = models.IntegerField(default=0)
    transaction_type = models.CharField(max_length=10,choices=TR_TYPE,blank=True, null=True)
    transaction_value = models.FloatField(default=0)
    credited_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    payment_response = models.TextField(null=True, blank=True)
    service_type = models.CharField(max_length=20,blank=True, null=True)
    unique_reference_key = models.CharField(max_length=50,blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    # Historical data ===========
    history = HistoricalRecords()

    class Meta:
        app_label = 'datacenter'
        managed = True
        unique_together = ('order_id','service_type')
