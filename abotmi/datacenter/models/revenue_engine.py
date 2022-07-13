from django.db import models
from datacenter.models import ClientDetails, ClientPlatform, Advisor
from simple_history.models import HistoricalRecords

class RevenueType(models.Model):
    '''
    Description : To store type of revenue from service
    Fields : revenue_name, revenue_code - represents the revenue type
            is_active - activate/deactivate revenue type
    '''
    revenue_name = models.CharField(max_length=40, unique=True, blank=True)
    revenue_code = models.CharField(max_length=10, unique=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_wallet = models.BooleanField(default=0)
    is_active = models.BooleanField(default=1)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    # Historical data ===========
    history = HistoricalRecords()
    
    class Meta:
        app_label = 'datacenter'
        managed = True

class TypeRevenuePlatformMapping(models.Model):
    '''
    Description : to store mapping platform and type of revenue with %
    Fields : platform - reffering from ClientPlatform,
            revenue_type - reffering from RevenueType,
            platform, revenue_type are unique field,
            revenue_percentage - percentage of revenue from platform for service.
            is_active - to activate/deactivate revenue type
    '''
    platform = models.ForeignKey(ClientPlatform, related_name='payer')
    revenue_type = models.ForeignKey(RevenueType)
    receiver = models.ForeignKey(ClientPlatform, related_name='receiver', null=True, blank=True)
    revenue_percentage  = models.FloatField(default=0,blank=True, null=True)
    is_active = models.BooleanField(default=1)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    # Historical data ===========
    history = HistoricalRecords()

    class Meta:
        app_label = 'datacenter'
        managed = True
        unique_together = (('platform','revenue_type'),)

class RevenueTransactions(models.Model):
    '''
    Desciption : To store revenu details the service.
    Fields : product_id - id of product of service,
            service_advisor - reffering from advisor (one who giving service to client)
            client - reffering from ClientDetails (one who getting service form upwrdz)
            transaction_value - client transaction product value,
            revenue_platform - reffering from TypeRevenuePlatformMapping,
            pay_from - payer for this transaction
            pay_to - Earn for this transaction
            revenue_in_percentage - service fee for this transaction from transcation value in %,
            revenue - service fee for this transaction from transcation value in amount,
            received_amount - status of receiving amount from platform to upwrdz,
            pyament_received_date - date of the payment
    '''
    product_id = models.CharField(max_length=20, null=True, blank=True)
    service_advisor = models.ForeignKey(Advisor, null=True, blank=True)
    client = models.ForeignKey(ClientDetails, null=True, blank=True)
    transaction_value = models.FloatField(default=0, null=True, blank=True)
    pay_from = models.CharField(db_index=True, max_length=250, null=True, blank=True)
    pay_to = models.CharField(db_index=True, max_length=250, null=True, blank=True)
    revenue_platform  = models.ForeignKey(TypeRevenuePlatformMapping, null=True, blank=True)
    source_revenue = models.FloatField(max_length=30, null=True, blank=True)
    revenue_in_percentage = models.FloatField(default=0, null=True, blank=True)
    revenue = models.FloatField(default=0, null=True, blank=True)
    is_paid = models.BooleanField(default=0)
    payment_received_date = models.DateField(null=True, blank=True)
    parent_transaction_id = models.IntegerField(default=0, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    # Historical data ===========
    history = HistoricalRecords()

    class Meta:
        app_label = 'datacenter'
        managed = True