from django.db import models

# commented for reference may use later
# from django.db.models import options as options
# options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)


class AdvisorData(models.Model):

    # Basic Profile
    title = models.CharField(max_length=5, blank=True)
    name = models.CharField(db_index=True, max_length=255, blank=True)
    # e-communication
    email = models.CharField(db_index=True, max_length=250)
    secondary_email = models.CharField(max_length=250, blank=True)
    mobile = models.CharField(db_index=True, max_length=20, blank=True, null=True)
    mobile2 = models.CharField(max_length=20, blank=True)
    landline = models.CharField(max_length=20, blank=True)
    # Company
    company = models.CharField(max_length=255, blank=True, null=True)
    # Address for Communication
    address = models.TextField(blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, default='India')
    pincode = models.CharField(max_length=15, blank=True)
    extra_fields = models.TextField(null=True, blank=True)
    # registrations details
    registrations = models.TextField(null=True, blank=True)
    # UPWRDZ Advisor Clime Status
    advisor_id = models.IntegerField(null=True, blank=True)  # upwrdz_user_profile_id
    category = models.TextField(null=True, blank=True, default="other")
    connected_members = models.CommaSeparatedIntegerField(
        null=True, blank=True, max_length=200)
    constitution = models.TextField(null=True, blank=True)
    source_link = models.TextField(null=True, blank=True)
    # System information
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        app_label = 'advisor_check'
        managed = True

    # override the unicode method to return the username on this model
    def __unicode__(self):
        return self.name


class IrdaData(models.Model):
    """
    used to hold IRDA advisor data
    fields has been collected from IRDA site.
    IRDA URN is unique for advisor, source is
    the link from where data has been collected.
    agent_id, license_no, sub_category, company,
    dp_id, absorbed_agent represents Agent ID,
    License No., Insurance Type, Insurer, Dp Id,
    Absorbed Agent of IRDA Site respectively.
    """
    license_no = models.CharField(db_index=True, unique=True, max_length=150, null=True)
    agent_id = models.CharField(max_length=150, null=True)
    name = models.CharField(db_index=True, max_length=250, null=True)
    email = models.CharField(max_length=250, null=True, blank=True)
    city = models.CharField(max_length=25, blank=True, null=True)
    mobile = models.CharField(db_index=True, max_length=25, null=True)
    mobile2 = models.CharField(db_index=True, max_length=25, null=True)
    source = models.CharField(max_length=150, null=True)
    organization = models.CharField(max_length=150, null=True)
    irda_urn = models.TextField(null=True, blank=True)
    sub_category = models.TextField(null=True, blank=True)
    company = models.CharField(max_length=250, null=True)
    dp_id = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    district = models.CharField(max_length=50, null=True)
    pin_code = models.CharField(max_length=10, null=True)
    valid_from = models.CharField(max_length=50, null=True)
    valid_till = models.CharField(max_length=50, null=True)
    absorbed_agent = models.CharField(max_length=150, null=True)
    # UPWRDZ Advisor Clime Status
    advisor_id = models.IntegerField(null=True, blank=True)  # upwrdz_user_profile_id
    claimed_status = models.CharField(max_length=50, null=True)
    # System information
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        app_label = 'advisor_check'
        managed = True

    # override the unicode method to return the username on this model
    def __unicode__(self):
        return str(self.irda_urn)


class AmfiData(models.Model):
    """
    Used to hold AMFI Advisor data
    arn is unique for AMFI advisors. Data
    has been collected from AMFIIndia Site.
    source is the link from where data has
    been collected. kyd_complaint, euin
    represents Kyd Complaint and EUIN of
    AMFIIndia Site.
    """
    arn = models.CharField(
        db_index=True, max_length=50, unique=True, blank=True, null=True)
    name = models.CharField(db_index=True, max_length=150, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    pincode = models.CharField(max_length=15, blank=True, null=True)
    email = models.CharField(db_index=True, max_length=250, blank=True, null=True)
    city = models.CharField(max_length=25, blank=True, null=True)
    mobile = models.CharField(db_index=True, max_length=25, blank=True, null=True)
    mobile2 = models.CharField(max_length=25, blank=True, null=True)
    source = models.CharField(max_length=150, null=True)
    valid_till = models.CharField(max_length=20, blank=True, null=True)
    valid_from = models.CharField(max_length=20, blank=True, null=True)
    kyd_complaint = models.CharField(max_length=25, blank=True, null=True)
    euin = models.CharField(max_length=15, blank=True, null=True)
    # UPWRDZ Advisor Clime Status
    advisor_id = models.IntegerField(null=True, blank=True)  # upwrdz_user_profile_id
    claimed_status = models.CharField(max_length=50, null=True)
    # System information
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        app_label = 'advisor_check'
        managed = True

    # override the unicode method to return the username on this model
    def __unicode__(self):
        return str(self.arn)


class CaData(models.Model):
    """
    used to hold CA advisor data. reg_id is unique.
    source contains from where the data has been
    collected.
    """
    reg_id = models.CharField(
        db_index=True, max_length=50, unique=True, blank=True, null=True)
    sub_category = models.CharField(max_length=20, null=True, blank=True)
    name = models.CharField(db_index=True, max_length=250, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    pincode = models.CharField(max_length=15, blank=True, null=True)
    email = models.CharField(db_index=True, max_length=250, blank=True, null=True)
    secondary_email = models.CharField(
        db_index=True, max_length=250, blank=True, null=True)
    landline = models.CharField(db_index=True, max_length=25, null=True)
    mobile = models.CharField(db_index=True, max_length=25, null=True)
    mobile2 = models.CharField(db_index=True, max_length=25, null=True)
    source = models.CharField(max_length=150, null=True)
    company = models.CharField(max_length=250, null=True)
    state = models.CharField(max_length=50, null=True)
    address = models.TextField(blank=True, null=True)
    # UPWRDZ Advisor Clime Status
    advisor_id = models.IntegerField(null=True, blank=True)  # upwrdz_user_profile_id
    claimed_status = models.CharField(max_length=50, null=True)
    # System information
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        app_label = 'advisor_check'
        managed = True

    # override the unicode method to return the username on this model
    def __unicode__(self):
        return str(self.reg_id)


class SebiData(models.Model):
    """
    Used to hold SEBI Advisor Data. Reg No is
    SEBI Registration No. and it is unique for
    SEBI Registeredclients. Source has the link
    from where data has been collected
    type_of_intermediary, fii_name,exchange_name, trade_name,
    affiliated_broker,affiliated_broker_reg_no represents
    Type of Intermediary, FII Name, Exchange Name,
    Trade Name, Affiliated Broker, Affiliated Broker Reg No
    of SEBI Site.
    """
    reg_no = models.CharField(
        db_index=True, max_length=50, unique=True, blank=True, null=True)
    name = models.CharField(db_index=True, max_length=250, blank=True, null=True)
    contact_person = models.CharField(
        db_index=True, max_length=250, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    email = models.CharField(db_index=True, max_length=250, blank=True, null=True)
    mobile = models.CharField(db_index=True, max_length=25, null=True)
    fax = models.CharField(max_length=25, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    pincode = models.CharField(max_length=15, blank=True, null=True)
    type_of_intermediary = models.CharField(max_length=50, blank=True, null=True)
    secondary_address = models.TextField(blank=True, null=True)
    secondary_email = models.CharField(
        db_index=True, max_length=250, blank=True, null=True)
    secondary_mobile = models.CharField(db_index=True, max_length=25, null=True)
    secondary_fax = models.CharField(max_length=25, blank=True, null=True)
    secondary_city = models.CharField(max_length=50, blank=True, null=True)
    secondary_state = models.CharField(max_length=50, blank=True, null=True)
    secondary_pincode = models.CharField(max_length=15, blank=True, null=True)
    valid_from = models.CharField(max_length=20, blank=True, null=True)
    valid_till = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)
    fii_name = models.CharField(max_length=50, blank=True, null=True)
    exchange_name = models.CharField(max_length=150, blank=True, null=True)
    trade_name = models.CharField(max_length=50, blank=True, null=True)
    affiliated_broker = models.CharField(max_length=50, blank=True, null=True)
    affiliated_broker_reg_no = models.CharField(max_length=50, blank=True, null=True)
    source = models.CharField(max_length=150, null=True)
    # UPWRDZ Advisor Clime Status
    advisor_id = models.IntegerField(null=True, blank=True)  # upwrdz_user_profile_id
    claimed_status = models.CharField(max_length=50, null=True)
    # System information
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        app_label = 'advisor_check'
        managed = True

    # override the unicode method to return the username on this model
    def __unicode__(self):
        return str(self.reg_no)


class BseData(models.Model):
    """
    Used to hold BSE Advisor Data.
    Clearance Number is Unique to all the records.
    Every BSE member contains of three sub categories
        1>Sub Brokers(Sebi registration unique number which is inserted in clearance
        number field)
        2>Remisiers(Remisiers registration unique number which is inserted in clearance
        number field)
        3>Authorised Persons(AP registration unique number which is inserted in clearance
        number field)
    There are different segments which will have their status in the segment_status field
    """
    authorised_persons = models.CharField(max_length=50, blank=True, null=True)
    bse_clearing_number = models.CharField(
        db_index=True, max_length=50, unique=True, blank=True, null=True)
    belongs_to_business_group = models.CharField(max_length=50, blank=True, null=True)
    board_of_directors_designation = models.CharField(
        max_length=500, blank=True, null=True)
    board_of_directors_name = models.CharField(max_length=500, blank=True, null=True)
    branch_offices = models.TextField(blank=True, null=True)
    broker_type = models.CharField(max_length=50, blank=True, null=True)
    change_in_status_constitution_of_ap = models.CharField(
        max_length=250, blank=True, null=True)
    chief_executive = models.CharField(max_length=500, blank=True, null=True)
    compliance_officer_1 = models.CharField(max_length=250, blank=True, null=True)
    compliance_officer_2 = models.CharField(max_length=250, blank=True, null=True)
    composite_corporate_membership = models.CharField(
        max_length=50, blank=True, null=True)
    constitution = models.CharField(max_length=500, blank=True, null=True)
    mobile = models.CharField(max_length=250, blank=True, null=True)
    email = models.CharField(max_length=250, blank=True, null=True)
    correspondence_office = models.TextField(blank=True, null=True)
    sebi_registration_date = models.CharField(max_length=50, blank=True, null=True)
    de_recognition_or_acceptance_date = models.CharField(
        max_length=50, blank=True, null=True)
    diciplinery_action_against_ap = models.CharField(max_length=50, blank=True, null=True)
    direct_phone = models.CharField(max_length=50, blank=True, null=True)
    fax = models.CharField(max_length=50, blank=True, null=True)
    listed_at = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    member_mapin = models.CharField(max_length=50, blank=True, null=True)
    other_indian_stock_exchanges_in_same_entity_clearing_no = models.CharField(
        max_length=250, blank=True, null=True)
    other_indian_stock_exchanges_in_same_entity_name_of_exchange = models.CharField(
        max_length=500, blank=True, null=True)
    other_indian_stock_exchanges_in_same_entity_sebi_registration_no = models.CharField(
        max_length=250, blank=True, null=True)
    no_of_terminals = models.CharField(max_length=50, blank=True, null=True)
    old_name_1_of_member = models.CharField(max_length=50, blank=True, null=True)
    old_name_2_of_member = models.CharField(max_length=50, blank=True, null=True)
    old_name_3_of_member = models.CharField(max_length=50, blank=True, null=True)
    other_capital_market_activities_name = models.CharField(
        max_length=250, blank=True, null=True)
    other_capital_market_activities_sebi_registration_no = models.CharField(
        max_length=250, blank=True, null=True)
    other_capital_market_activities_sebi_registration_start_date = models.CharField(
        max_length=250, blank=True, null=True)
    other_group_companies_in_the_capital_market_area_activity = models.TextField(
        blank=True, null=True)
    other_group_companies_in_the_capital_market_area_company_name = models.TextField(
        blank=True, null=True)
    phones = models.CharField(max_length=250, blank=True, null=True)
    pincode = models.CharField(max_length=50, blank=True, null=True)
    products_or_services_handled = models.CharField(max_length=50, blank=True, null=True)
    profile_of_member_as_submitted_by_member = models.TextField(blank=True, null=True)
    reference_to_bse_clearing_number = models.CharField(
        max_length=50, blank=True, null=True)
    registered_office = models.TextField(blank=True, null=True)
    remisiers = models.CharField(max_length=50, blank=True, null=True)
    sebi_registration_no = models.CharField(max_length=50, blank=True, null=True)
    sebi_registration_no_for_currency_derivatives = models.CharField(
        max_length=250, blank=True, null=True)
    sebi_registration_no_for_currency_derivatives_date = models.CharField(
        max_length=250, blank=True, null=True)
    segment_and_status_all_segments = models.CharField(
        max_length=250, blank=True, null=True)
    state = models.CharField(max_length=250, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    sub_brokers = models.CharField(max_length=50, blank=True, null=True)
    subsidiary_status = models.CharField(max_length=50, blank=True, null=True)
    terminal_details = models.CharField(max_length=250, blank=True, null=True)
    trade_name = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=250, blank=True, null=True)
    types_of_clients_served = models.CharField(max_length=250, blank=True, null=True)
    website = models.CharField(max_length=250, blank=True, null=True)
    year_broking_business_started = models.CharField(max_length=50, blank=True, null=True)
    year_of_bse_membership = models.CharField(max_length=50, blank=True, null=True)
    year_of_incorporation = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=250, blank=True, null=True)
    segment_status = models.TextField(blank=True, null=True)
    source_link = models.CharField(max_length=250, blank=True, null=True)
    # UPWRDZ Advisor Clime Status
    advisor_id = models.IntegerField(null=True, blank=True)  # upwrdz_user_profile_id
    claimed_status = models.CharField(max_length=50, null=True)
    # System information
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        app_label = 'advisor_check'
        managed = True

    # override the unicode method to return bse clearing number
    def __unicode__(self):
        return str(self.bse_clearing_number)


class MalaysianAdvisors(models.Model):
    """
    used to store the malaysian advisors
    """
    regulated_activity = models.TextField(null=True, blank=True)
    principal_company = models.CharField(max_length=100, null=True, blank=True)
    licence_number = models.CharField(max_length=30, db_index=True, blank=True, null=True)
    licensed_since = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=15, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    source = models.CharField(max_length=150, null=True)

    # basic data
    name = models.CharField(max_length=250, blank=True, null=True)
    email = models.CharField(max_length=250, blank=True, null=True)
    mobile = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=250, blank=True, null=True)
    # UPWRDZ Advisor Clime Status
    advisor_id = models.IntegerField(null=True, blank=True)  # upwrdz_user_profile_id
    claimed_status = models.CharField(max_length=50, null=True)
    # System information
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        app_label = 'advisor_check'
        managed = True

    # override the unicode method to return bse clearing number
    def __unicode__(self):
        return str(self.licence_number)


class UnitedStatesAdvisors(models.Model):
    """
    Used to hold the USA advisor data in that LIC ID (License ID) is unique
    """
    lic_id = models.CharField(max_length=50, blank=True, null=True)
    lic_type = models.CharField(max_length=15, null=True, blank=True)
    lic_issue_date = models.CharField(max_length=25, null=True, blank=True)
    lic_expiry_date = models.CharField(max_length=25, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    middle_name = models.CharField(max_length=25, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    st = models.CharField(max_length=50, null=True, blank=True)
    pincode = models.CharField(max_length=15, null=True, blank=True)
    telephone = models.CharField(max_length=15, null=True, blank=True)
    orig_st_cd = models.CharField(max_length=50, null=True, blank=True)
    qual_type = models.CharField(max_length=15, null=True, blank=True)
    report_date = models.CharField(max_length=25, null=True, blank=True)
    source = models.CharField(max_length=150, null=True)

    # BASIC DATA
    name = models.CharField(max_length=250, blank=True, null=True)
    email = models.CharField(max_length=250, blank=True, null=True)
    mobile = models.CharField(max_length=250, blank=True, null=True)
    # UPWRDZ Advisor Clime Status
    advisor_id = models.IntegerField(null=True, blank=True)  # upwrdz_user_profile_id
    claimed_status = models.CharField(max_length=50, null=True)
    # System information
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        app_label = 'advisor_check'
        managed = True

    # override the unicode method to return bse clearing number
    def __unicode__(self):
        return str(self.lic_id)


class FinraAdvisors(models.Model):
    """
    Used to hold the Finra Broker Check advisor data in that crd_no is unique
    """
    crd_no = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    middle_name = models.CharField(max_length=20, blank=True, null=True)
    alternate_name = models.CharField(max_length=100, blank=True, null=True)
    bc_scope = models.CharField(max_length=15, blank=True, null=True)
    ia_scope = models.CharField(max_length=15, blank=True, null=True)
    company = models.CharField(max_length=250, blank=True, null=True)
    company_crd_number = models.CharField(max_length=20, blank=True, null=True)
    company_address = models.TextField(blank=True, null=True)
    company_state_code = models.CharField(max_length=10, blank=True, null=True)
    company_zip_code = models.CharField(max_length=20, blank=True, null=True)
    registered_with_company_since = models.DateField(blank=True, null=True)
    exam_details = models.TextField(blank=True, null=True)
    registered_states = models.TextField(blank=True, null=True)
    sro_registrations = models.TextField(blank=True, null=True)
    previous_employments = models.TextField(blank=True, null=True)
    regulated_by_finra = models.CharField(max_length=50, blank=True, null=True)
    industry_start_date = models.DateField(blank=True, null=True)
    # BASIC DATA
    name = models.CharField(max_length=250, blank=True, null=True)
    email = models.CharField(max_length=250, blank=True, null=True)
    mobile = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    source = models.CharField(max_length=150, null=True)
    # UPWRDZ Advisor Clime Status
    advisor_id = models.IntegerField(null=True, blank=True)  # upwrdz_user_profile_id
    claimed_status = models.CharField(max_length=50, null=True)
    # System information
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        app_label = 'advisor_check'
        managed = True

    # override the unicode method to return bse clearing number
    def __unicode__(self):
        return str(self.crd_no)


class SingaporeAdvisors(models.Model):
    """
    Used to hold singapore data where member_number is unique id
    """
    english_name = models.CharField(max_length=50, null=True, blank=True)
    surname = models.CharField(max_length=50, null=True, blank=True)
    fpas_certification = models.CharField(max_length=50, null=True, blank=True)
    industry = models.CharField(max_length=50, null=True, blank=True)
    experience = models.CharField(max_length=20, null=True, blank=True)
    specialization = models.TextField(null=True, blank=True)
    company = models.CharField(max_length=250, null=True, blank=True)
    job_title = models.CharField(max_length=250, null=True, blank=True)
    office_address = models.TextField(null=True, blank=True)
    member_since = models.CharField(max_length=50, null=True, blank=True)
    member_number = models.CharField(max_length=20, blank=True, null=True)
    practitioner = models.CharField(max_length=50, null=True, blank=True)
    regulatory_no = models.CharField(max_length=20, null=True, blank=True)
    cfp_certified_from = models.CharField(max_length=50, null=True, blank=True)
    awp_certified_from = models.CharField(max_length=50, null=True, blank=True)
    afp_certified_from = models.CharField(max_length=50, null=True, blank=True)
    cfp_license_number = models.CharField(max_length=50, null=True, blank=True)
    member_ship_expiry_date = models.CharField(max_length=50, null=True, blank=True)
    # BASIC DATA
    name = models.CharField(max_length=250, blank=True, null=True)
    email = models.CharField(max_length=250, blank=True, null=True)
    mobile = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    source = models.CharField(max_length=150, null=True)
    # UPWRDZ Advisor Clime Status
    advisor_id = models.IntegerField(null=True, blank=True)  # upwrdz_user_profile_id
    claimed_status = models.CharField(max_length=50, null=True)
    # System information
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        app_label = 'advisor_check'
        managed = True

    # override the unicode method to return bse clearing number
    def __unicode__(self):
        return str(self.member_number)


class FinraFirms(models.Model):
    """
    Used to hold the Finra Broker Check firms data in that crd_no is unique
    """
    crd_no = models.CharField(max_length=20, blank=True, null=True)
    sec_no = models.CharField(max_length=20, blank=True, null=True)
    other_names = models.TextField(blank=True, null=True)
    finra_json = models.TextField(blank=True, null=True)
    # BASIC DATA
    name = models.CharField(max_length=250, blank=True, null=True)
    email = models.CharField(max_length=250, blank=True, null=True)
    mobile = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    source = models.CharField(max_length=150, null=True)
    # UPWRDZ Advisor Clime Status
    advisor_id = models.IntegerField(null=True, blank=True)  # upwrdz_user_profile_id
    claimed_status = models.CharField(max_length=50, null=True)
    # System information
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        app_label = 'advisor_check'
        managed = True

    # override the unicode method to return bse clearing number
    def __unicode__(self):
        return str(self.crd_no)
