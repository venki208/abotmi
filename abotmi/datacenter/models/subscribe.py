from django.db import models
from datacenter.models import UserProfile
from simple_history.models import HistoricalRecords

# CONSTANTS
PACKAGE_CHOICE_LIST = (
    ('STANDARD','STANDARD'),
    ('DELUXE','DELUXE'),
    ('PREMIUM','PREMIUM'),
    ('EXECUTIVE','EXECUTIVE'),
    ('PLATINUM','PLATINUM'),
)

class SubscriptionCategoryMaster(models.Model):
    """
    Details: used to hold the category master like
    IDENTITY_PACK, MICRO_LEARNING_PACK etc.
    """
    category_name = models.CharField(max_length=250, unique=True)
    # system information
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    # Historical data ===========
    history = HistoricalRecords()

    class Meta:
        app_label = 'datacenter'
        managed = True

    def __unicode__(self):
        return str(self.category_name)

class SubscriptionPackageMaster(models.Model):
    """
    Details: To store all subscription packages
    """
    package_code = models.CharField(max_length=50, unique=True)
    package_name = models.CharField(max_length=50)
    package_description = models.TextField(blank=True, null=True)
    feature_data = models.TextField(blank=True, null=True)
    package_type = models.CharField(max_length=50, choices=PACKAGE_CHOICE_LIST, default='STANDARD')
    package_amount = models.FloatField(default=0, blank=True, null=True)
    package_duration = models.IntegerField(default=0, null=True, blank=True)
    subscription_category = models.ForeignKey(SubscriptionCategoryMaster, null=True, blank=True)
    published = models.BooleanField(default=1)
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    # Historical data ===========
    history = HistoricalRecords()

    class Meta:
        app_label = 'datacenter'
        managed = True

    def __unicode__(self):
        return str(self.package_code)


class AdvisorSubscriptionPackageOrder(models.Model):
    """
    Details: package Order of Subscription by the advisor
    Fields : user_profile, subscription_type(refer SubscriptionPackageMaster),
            subscription_value(package price at the time of order creation),
            subscription_status(activated/de-activated), current_package_criteria(priciple of current activated package), expire_date (expire date of package)
    """
    user_profile = models.ForeignKey(UserProfile)
    subscription_type = models.ForeignKey(SubscriptionPackageMaster)
    subscription_value = models.FloatField(default=0, null=True, blank=True)
    subscription_status = models.CharField(max_length=30, null=True, blank=True)
    current_package_criteria = models.TextField(null=True, blank=True)
    expire_date = models.DateField(null=True, blank=True)
    payment_status = models.CharField(max_length=30, null=True, blank=True)
    #unique_reference_key is stored in AllTransactionsDetails table, send in requests of payment gateway
    unique_reference_key = models.CharField(max_length=50,blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    # Historical data ===========
    history = HistoricalRecords()

    class Meta:
        app_label = 'datacenter'
        managed = True

    def __unicode__(self):
        return str(self.user_profile)

class FeatureListMaster(models.Model):
    """
    Details: Core list of Features will be captured and will be mapped with subscription packs

    """
    feature_name = models.CharField(max_length=250)
    feature_description = models.TextField(blank=True, null=True)
    feature_short_name = models.CharField(max_length=250, null=True, blank=True)
    subscription_category = models.ForeignKey(SubscriptionCategoryMaster)
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    # Historical data ===========
    history = HistoricalRecords()

    class Meta:
        app_label = 'datacenter'
        managed = True
        unique_together = ('feature_name', 'feature_short_name','subscription_category')

    def __unicode__(self):
        return self.feature_name

# ============================================================================
# FeatureSubscriptionPkgMapping will be removed once functionality is working fine
# ============================================================================
class FeatureSubscriptionPkgMapping(models.Model):
    """
    Details: used to hold the feature and subscription pack mapping
    """
    subscription_pkg = models.ForeignKey(SubscriptionPackageMaster)
    feature_list = models.ForeignKey(FeatureListMaster)
    feature_data = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    # Historical data ===========
    history = HistoricalRecords()

    class Meta:
        app_label = 'datacenter'
        managed = True
        unique_together = ('subscription_pkg', 'feature_list',)

    def __unicode__(self):
        data = str(self.subscription_pkg.package_name)+"_"+str(self.feature_list.feature_name)
        return data

class MicroLearningVideoPkg(models.Model):
    """
    Details: used to hold the feature and subscription pack mapping
    """
    advisor_subscription_pkg = models.ForeignKey(AdvisorSubscriptionPackageOrder)
    video_count = models.IntegerField(default=0, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    # Historical data ===========
    history = HistoricalRecords()

    class Meta:
        app_label = 'datacenter'
        managed = True

    def __unicode__(self):
        return str(self.video_count)
