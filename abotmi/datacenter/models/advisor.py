import hashlib
from django.contrib.auth.models import User
from django.db import models
from simple_history.models import HistoricalRecords
from datacenter.models import UserProfile, Country, TransactionsDetails


class AdvisorType(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    is_management = models.BooleanField(default=0)

    class Meta:
        app_label = 'datacenter'
        managed = True

    def __unicode__(self):
        return self.name


class Advisor(models.Model):
    user_profile = models.OneToOneField(UserProfile, null=True, blank=True)
    my_promise = models.TextField(blank=True)
    # Questionnaire    ===============================
    questions = models.TextField(blank=True)
    # advisor status   ===============================
    is_submitted_questions = models.BooleanField(default=0, blank=True)
    is_document_submited = models.BooleanField(default=0)
    # checking kyc 2nd form completion
    is_advisor_details_submitted = models.BooleanField(default=0, blank=True)
    is_submitted_all = models.BooleanField(default=0)
    is_confirmed_advisor = models.BooleanField(default=0)
    is_register_advisor = models.BooleanField(default=0)
    is_wpb_user = models.BooleanField(default=0)
    is_certified_advisor = models.BooleanField(default=0)
    is_honorable_advisor = models.BooleanField(default=0)
    wordpress_user_id = models.CharField(max_length=10, default=0)
    type_of_advisor = models.ForeignKey(AdvisorType, blank=True, null=True)
    # Crisil Users ====================================
    crisil_application_status = models.CharField(max_length=50, default='not_applied')
    is_crisil_verified = models.BooleanField(default=0)
    crisil_registration_number = models.CharField(max_length=30, null=True, blank=True)
    crisil_expiry_date = models.DateField(null=True, blank=True)
    # Credibility Declaration form
    is_registered_advisor = models.BooleanField(default=0)
    sebi_number = models.CharField(blank=True, null=True, max_length=50)
    amfi_number = models.CharField(blank=True, null=True, max_length=50)
    irda_number = models.CharField(blank=True, null=True, max_length=50)
    # start date
    sebi_start_date = models.DateField(null=True, blank=True)
    irda_start_date = models.DateField(null=True, blank=True)
    amfi_start_date = models.DateField(null=True, blank=True)
    # expiry date
    sebi_expiry_date = models.DateField(null=True, blank=True)
    irda_expiry_date = models.DateField(null=True, blank=True)
    amfi_expiry_date = models.DateField(null=True, blank=True)
    other_expiry_date = models.DateField(null=True, blank=True)
    other_registered_organisation = models.CharField(
        blank=True, null=True, max_length=100)
    other_registered_number = models.CharField(blank=True, null=True, max_length=50)
    practice_country = models.ForeignKey(Country, blank=True, null=True)
    practice_city = models.CharField(max_length=50, blank=True, null=True)
    practice_location = models.CharField(max_length=50, blank=True, null=True)
    practice_years = models.PositiveIntegerField(blank=True, null=True)
    # practice_details holds contry,city,location,pincode in json
    practice_details = models.TextField(blank=True, null=True) 
    financial_instruments = models.TextField(blank=True, null=True)
    other_financial_instruments = models.CharField(max_length=50, blank=True, null=True)
    credibility_declaration_qualification = models.CharField(
        max_length=50, blank=True, null=True)
    # certification title ==============================
    certification_title = models.TextField(blank=True, null=True)
    # RERA Fields =============================
    is_rera = models.BooleanField(default=0)
    rera_details = models.TextField(blank=True)
    total_clients_served = models.PositiveIntegerField(blank=True, null=True)
    total_advisors_connected = models.PositiveIntegerField(blank=True, null=True)
    # my sales ==============================
    my_sales = models.CharField(max_length=500, blank=True, null=True)
    # reia goals ============================
    reia_goals = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    # In Person Verification ================
    ipv_status = models.BooleanField(default=False)
    # DSA Details
    dsa_details = models.TextField(blank=True, null=True)
    # Skills of advisor
    skills = models.TextField(blank=True, null=True)
    # advisor expertise in
    expertise = models.TextField(blank=True, null=True)
    # Calendly link of advisor
    calendly_link = models.CharField(max_length=250, null=True, blank=True)

    # Historical data ===========
    history = HistoricalRecords()

    class Meta:
        app_label = 'datacenter'
        managed = True

    def __unicode__(self):
        return str(self.user_profile)

UserProfile.advisor = property(lambda u: Advisor.objects.get_or_create(user_profile=u)[0])


class ExternalUser(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    sebi_number = models.CharField(
        max_length=50, blank=True, null=True)
    sebi_expiry_date = models.DateTimeField(blank=True, null=True)
    amfi_number = models.CharField(
        max_length=50, blank=True, null=True)
    amfi_expiry_date = models.DateTimeField(blank=True, null=True)
    irda_number = models.CharField(
        max_length=50, blank=True, null=True)
    irda_expiry_date = models.DateTimeField(blank=True, null=True)
    other_registered_organisation = models.CharField(
        max_length=100, blank=True, null=True)
    other_registered_number = models.CharField(
        max_length=50, blank=True, null=True)
    other_certificate_expiry_date = models.DateTimeField(blank=True, null=True)
    # RERA Details
    rera_details = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    # Historical data ===========
    history = HistoricalRecords()

    class Meta:
        app_label = 'datacenter'
        managed = True

    def __unicode__(self):
        return self.email


class AdvisorRating(models.Model):
    advisor = models.ForeignKey(Advisor, blank=True, null=True)
    trust = models.FloatField(default=0)
    financial_knowledge = models.FloatField(default=0)
    communication = models.FloatField(default=0)
    advisory = models.FloatField(default=0)
    ethics = models.FloatField(default=0)
    customer_care = models.FloatField(default=0)
    no_of_questions = models.FloatField(default=6)
    avg_rating = models.FloatField(default=0)
    activation_key = models.CharField(max_length=250, blank=True, null=True)
    external_user = models.ForeignKey(
        ExternalUser, blank=True, null=True)
    existing_user_profile = models.ForeignKey(
        UserProfile, blank=True, null=True)
    user_type = models.CharField(max_length=20, blank=True, null=True)
    feedback = models.CharField(max_length=250, blank=True, null=True)
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
        return str(self.advisor)


class NoticeBoard(models.Model):
    NEWS_TYPE_CHOICES = (
            ("notice", "notice"),
            ("news", "news")
        )
    news_type = models.CharField(
        max_length=20, choices=NEWS_TYPE_CHOICES, default="notice")
    notice_date = models.DateTimeField(null=True, blank=True)
    headline = models.CharField(max_length=500, null=True, blank=True)
    notice = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    # Historical data ===========
    history = HistoricalRecords()

    class Meta:
        app_label = 'datacenter'
        managed = True

    def __unicode__(self):
        return self.headline


class CrisilCertifications(models.Model):
    transcation_id = models.ForeignKey(TransactionsDetails)
    advisor_id = models.ForeignKey(Advisor)
    crisil_registration_number = models.CharField(max_length=30, null=True, blank=True)
    crisil_issued_date = models.DateField(null=True, blank=True)
    crisil_expiry_date = models.DateField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    # Historical data ===========
    history = HistoricalRecords()

    class Meta:
        app_label = 'datacenter'
        managed = True

    def __unicode__(self):
        return str(self.crisil_registration_number)

Advisor.crisil_certificate = property(
    lambda u: CrisilCertifications.objects.get_or_create(advisor_id=u)[0])


def company_logo(instance, filename):
    return '/'.join(['reia', str(instance.user_profile_id), "company_logo.jpg"])


class AffiliatedCompany(models.Model):
    user_profile = models.OneToOneField(UserProfile, blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True)
    tagline = models.CharField(max_length=90, blank=True)
    website_url = models.URLField(blank=True)
    objective = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    address = models.TextField(blank=True)
    domain_name = models.TextField(blank=True)  # domain name of the company
    contact_number = models.TextField(blank=True)  # multiple contact number will be saved
    social_media = models.TextField(blank=True)
    logo = models.ImageField(upload_to=company_logo, blank=True)
    awards_or_rewards = models.TextField(blank=True)
    terms_and_conditions = models.BooleanField(default=0)
    users_count = models.IntegerField(default=0)
    membership_type = models.CharField(max_length=100, blank=True, null=True)
    segment = models.CharField(max_length=200, blank=True, null=True)
    corprate_identity_no = models.CharField(max_length=50, blank=True, null=True)
    registered_location = models.CharField(max_length=50, blank=True, null=True)
    registration_no = models.CharField(max_length=20, blank=True, null=True)
    company_category = models.CharField(max_length=50, blank=True, null=True)
    company_sub_category = models.CharField(max_length=50, blank=True, null=True)
    class_of_company = models.CharField(max_length=10, blank=True, null=True)
    date_of_incorporation = models.DateField(null=True, blank=True)
    activity = models.TextField(blank=True, null=True)
    board_of_directors = models.TextField(blank=True, null=True)
    registered_under_and_no = models.TextField(blank=True, null=True)
    branches_office_establishment = models.IntegerField(blank=True, null=True)
    franchisee_office_establishment = models.IntegerField(blank=True, null=True)
    authorized_capital = models.FloatField(blank=True, null=True)
    paid_up_capital = models.FloatField(blank=True, null=True)
    number_client = models.IntegerField(blank=True, null=True)
    number_of_employee = models.IntegerField(blank=True, null=True)

    created_date = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(
        auto_now=True, blank=True, null=True)

    class Meta:
        app_label = 'datacenter'
        managed = True

    def __unicode__(self):
        return self.company_name


class CompanyAdvisorMapping(models.Model):
    company_user_profile = models.ForeignKey(UserProfile, related_name="company_profile")
    advisor_user_profile = models.ForeignKey(UserProfile, related_name="user_profile")
    status = models.CharField(max_length=24, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(
        auto_now=True, blank=True, null=True)

    class Meta:
        app_label = 'datacenter'
        managed = True
        unique_together = (('company_user_profile', 'advisor_user_profile'),)

    def __unicode__(self):
        return str(self.company_user_profile)


class AdvisorVideoRequest(models.Model):
    """
    Advisor video request for shooting
    """
    video_title = models.CharField(max_length=150, blank=True, null=True)
    user_profile = models.ForeignKey(UserProfile, null=True, blank=True)
    video_description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=25, blank=True, null=True)
    shoot_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        app_label = 'datacenter'
        managed = True


class AdvisorPublishedVideo(models.Model):
    """
    Advisor Published Video
    user_profile - user_profile object
    video_title - title of the video
    video_link - youtube like / vimeo link
    status - video to be published in upwrdz or not controlled by nfadmin
    """
    user_profile = models.ForeignKey(UserProfile, null=True, blank=True)
    video_title = models.CharField(max_length=150, blank=True, null=True)
    video_link = models.TextField(blank=True, null=True)
    video_description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        app_label = 'datacenter'
        managed = True
   
    def __unicode__(self):
        return str(self.user_profile)


class AdvisorProfileShare(models.Model):
    """
    Definition: Advisor add member detail to share his profile to see by them.
    Fields: name, email, adviosr(refer advisor), 
            viewed_date(update date at the time of memeber seen his profile)
            created_date will be consider as shared link date
    """
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(db_index=True, max_length=250)
    advisor = models.ForeignKey(Advisor)
    viewed_date = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        app_label = 'datacenter'
        managed = True
   
    def __unicode__(self):
        return str(self.email)


class ProfileShareMapping(models.Model):
    """
    Definition: viewed memeber mapping with advisor
    Field: advisor(refer advisor), viewed_user_profile(refer UserProfile),
            viewed_page(my identity, my_repute)
    """
    advisor = models.ForeignKey(Advisor)
    viewed_user_profile = models.ForeignKey(UserProfile)
    viewed_page = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        app_label = 'datacenter'
        managed = True

    def __unicode__(self):
        return str(self.viewed_user_profile)


class ActivityFollowers(models.Model):
    """
    Definition: Advisor Followers
    Field: user_profile, followers, following_status
    followee_user_profile is following follower_user_profile
    follower_user_profile -> loggedin user profile id
    followee_user_profile --> id of user to request for following
    """
    user_profile = models.ForeignKey(
        UserProfile, null=True, blank=True, related_name="followee_user_profile")
    followers = models.ForeignKey(
        UserProfile, null=True, blank=True, related_name="follower_user_profile")
    # status: following, unfollow, donotfollow, inprogress
    activation_key = models.TextField(blank=True, null=True)
    following_status = models.CharField(max_length=20, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        app_label = 'datacenter'
        managed = True
  
    def __unicode__(self):
        return str(self.user_profile)


class AdvChkProfileConnectMap(models.Model):
    '''
    Storing Advisor check profile viewed data and connect data
    user_profile -> need to pass abotmi database member's UserProfile id
    advisor_chk_id -> need to pass advisor check database table id
                        (id can be SebiData, AmfiData, IrdaData, etc.. tables)
    regsitration_type -> Advisor check Registration table name
    action_type -> 'view' or 'connect'
    '''
    user_profile = models.ForeignKey(
        UserProfile, blank=True, related_name="member_profile_id")
    advisor_chk_id = models.IntegerField(blank=True)
    registration_type = models.CharField(blank=True, max_length=50)
    action_type = models.CharField(blank=True, max_length=30)
    email = models.EmailField(max_length=250, blank=True)
    created_date = models.DateTimeField(blank=True, auto_now_add=True)
    modified_date = models.DateTimeField(blank=True, auto_now=True)

    class Meta:
        unique_together = (
            ('user_profile', 'advisor_chk_id',
             'registration_type', 'action_type')
        )

    def __unicode__(self):
        return str(self.user_profile)
