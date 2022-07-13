from django.db import models
from datacenter.models import UserProfile, AllTransactionsDetails
from simple_history.models import HistoricalRecords

class MywalletTransaction(models.Model):
    """
    Details: it is all about credit and debit transaction of mywallet
    Fields: user_profile, wallet_name(crisil wallet, identity_pack_wallet, video wallet),
            source_wallet_type(refer wallet and etc)
            debited_amount(advisor used this wallet money for their subscription)
            credited_amount(advisor will get wallet money becuse his refered advisor
                doing transaction), description, revenue_transaction
            (refer revenue_transaction which have all detials of transaction)
    """
    user_profile = models.ForeignKey(UserProfile)
    wallet_name = models.CharField(max_length=20, null=True, blank=True)
    source_wallet_type = models.CharField(max_length=20, null=True, blank=True)
    credited_amount = models.FloatField(default=0, blank=True, null=True)
    debited_amount = models.FloatField(default=0, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    source_transaction = models.ForeignKey(AllTransactionsDetails, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    # Historical data ===========
    history = HistoricalRecords()

    class Meta:
        app_label = 'datacenter'
        managed = True

class MyWallet(models.Model):
    """
    Details: To store all type of wallet money of users
    Fields: user_profile, wallet_name(crisil wallet, identity_pack_wallet, video wallet),
            total_wallet
    """
    user_profile = models.ForeignKey(UserProfile)
    wallet_name = models.CharField(max_length=20)
    total_wallet = models.FloatField(default=0, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    # Historical data ===========
    history = HistoricalRecords()

    class Meta:
        app_label = 'datacenter'
        managed = True
        unique_together = (('user_profile','wallet_name'),)