from django.conf import settings
# Referral Point Type Table Define
SIGNUP_POINTS = "signup_advisor"

REGISTERED_ADVISOR = "registered_advisor"

CERTIFIED_ADVISOR = "certified_advisor"

CRISAL_VERIFICATION = "crisal_verification_advisor"

MEETUP_GROUP_NAME = getattr(settings, "MEETUP_GROUP_NAME", "meetup-group-sshjAoTJ")
MEETUP_KEY = getattr(settings, "MEETUP_KEY", "33e411b637f44447b4a795c335c471a")

MEETUP_CREATE_EVENT_API = "https://api.meetup.com/2/event"

MEETUP_CREATE_EVENT_SUCCESS = "Meetup event scheduled/created successfully"

EVENT_HOURS = [h for h in range(0, 25)]

EVENT_MINUTES = [m for m in range(5, 65, 5)]

NO_MEETUP_EVENTS = 'You have not scheduled any meetup event'

SEND_MEETUP_INVITATION_SUCCESS = 'Specified persons are invited for the created Mlegion \
    event'

# # USED FOR REIA LEVELS
# REIA_LEVEL_1 = "REISE - Real Estate Investment Support Executive"
# REIA_LEVEL_2 = "AREIA - Associate Real Estate Investment Advisor"

# PROGRESS BAR VALUES
FIRST_STEP = 1.33333333333
SECOND_STEP = 0.48780487804
THIRD_STEP = 5
FORUTH_STEP = 10

ALL_FINANCIAL_INSTRUMENT = [
    "Equity",
    "Wealth Advisory",
    "Mutual Fund",
    "Insurance",
    "Real Estate",
    "Portfolio Management"
]
FINANCIAL_INSTRUMENT_NULL_JSON = [{
    "instruments": "select", "experience": ""
}]
DSA_RESULTS_NULL_JSON = [{
    "dsa_bank_name": "", "dsa_code": "", "dsa_how_long_associated": ""}]
RERA_VALUES_NULL_JSON = [{
    "rera_registration_no": "", "rera_state": "", "rera_expire_date": ""}]

# CRISIL APPLICATION STATUS
CRISIL_NOT_APPLIED = "not_applied"
CRISIL_APPLIED = "applied_for_certificate"
CRISIL_PAYMENT_SUBMITTED = "payment_details_submitted"
CRISIL_RENEWAL_PAYMENT_SUBMITTED = "renewal_payment_details_submitted"
CRISIL_PAYMENT_RE_SUBMIT = "re_submit_details"
CRISIL_RENEWAL_PAYMENT_RE_SUBMIT = "renewal_re_submit_details"
CRISIL_CERTIFICATE_IN_PROCESS = "crisil_certificate_in_process"
CRISIL_RENEWAL_CERTIFICATE_IN_PROCESS = "crisil_renewal_certificate_in_process"
CRISIL_VERIFICATION_FAILED = 'crisil_verification_failed'
CRISIL_GOT_CERTIFICATE = "got_crisil_certificate"
CRISIL_EXPIRED = "crisil_certificate_expired"
CRISIL_EXPIRED_BY_USER = "crisil_certificate_expired_by_user"
CRISIL_RENEWAL = "crisil_certificate_renewal"
CRISIL_ONLINE_PAYMENT_DESCRIPTION = 'CRISIL Certifiate cost'
CRISIL_ONLINE_PAYMENT_NAME = 'CRISIL Payment'

# CRISIL BANK DETAILS
CRISIL_ACCOUNT_NAME = "NorthFacing RealTech Pvt.Ltd"
CRISIL_ACCOUNT_NUMBER = "9876543210"
CRISIL_BANK_NAME = "HDFC Bank"
CRISIL_BANK_BRANCH = "JP Nagar 2nd Phase"
CRISIL_BANK_IFSC_CODE = "HDFC000058"

# CRISIL Upload Document URLS
CRISIL_URL_ONE = settings.DEFAULT_DOMAIN_URL+'/dashboard/'

# TRANSCATION TABLE STATUS
TR_PAID = "paid"
TR_RENEWAL_PAID = "renewal_paid"
TR_BOUNCED = "bounced"
TR_RENEWAL_BOUNCED = "renewal_bounced"
TR_INVALID = "invalid"
TR_RENEWAL_INVALID = "renewal_invalid"
TR_TYPE = "NEFT/RTGS"
TR_TYPE_ONLINE = 'online'

# CRISIL Certification Cost value and Discount
CRISIL_CERTIFICATE_VALUE = 11000
CRISIL_CERTIFICATE_DISCOUNT = 50  # 50 percentage
TAX_PERCENTAGE_CRISIL = 18  # 18 Percentage
CRISIL_CERTIFICATE_VALUE_WITHOUT_DISCOUNT = 25300.00
CRISIL_OFFERED_YEARS = 1  # in Years
CERTIFICATE_YEARS = 2
CERTIFICATE_RENEWAL_YEAR = 1  # in Years
CRISIL_CERTIFICATE_RENEWAL_VALUE = 6750  # crisil renewal amount

# CRISIL Titles
APPLIED_ADVISORS = 'Applied Advisors'
CRISIL_PAYMENT_DETAILS = 'CRISIL Payment Details'
CRISIL_VERIFIED_ADVISORS = 'CRISIL Verified Advisors'
CRISIL_RENEWAL_ADVISORS = 'CRISIL Renewal Advisors'
CRISIL_EXPIRED_ADVISORS = 'CRISIL Expired Advisors'
INVOICE_NUMBER_RENEWAL = '10-901-A-02-'
INVOICE_NUMBER_NEW = '10-901-A-01-'
NEW = 'new'
RENEWAL = 'renewal'
START_INVOICE_SEQUENCE = '000001'

# REIA Register Link
REGISTER_LINK = "https://test.reiaglobal.com/signup/register_advisor/"

OLD_SECONDARY_EMAIL = 'old_secondary_email'
REIA_URL = 'https://www.reiaglobal.com'

# SignZy document Verification

# Authentication URL
SIGNZY_AUTHENTICATION_URL = "https://signzy.tech/api/v2/patrons/login"

# upload file url
SIGNZY_UPLOAD_URL = "https://persist.space/api/files/upload"

# verification url
SIGNZY_VERIFICATION_URL = "https://use.signzy.tech/identities/verifications"

# extraction url
SIGNZY_EXTRACTION_URL = "https://use.signzy.tech/identities/extractions"

# get in touch admin email id
REIA_HELP_ADMIN_EMAIL = "help@reiaglobal.com"

UPWRDZ_ADMIN_EMAIL = "admin@upwrdz.com"
UPLYF_ADMIN_EMAIL = "admin@uplyf.com"

# email for Enquiry
REIA_ENQUIRY_ADMIN_EMAIL = "yamini@mobisir.net"

# value for Communication Email ID
PRIMARY = 'primary'
SECONDARY = 'secondary'
PRIMARY_COMMUNICATION_HOME = 'home'
REGULAR_ADVISOR = 'Regular Advisor'

# checking advisor details are found or not at compnay admin
DETAILS_FOUND = 'details_found'
DETAILS_NOT_FOUND = 'details_not_found'

# Users count
USERS_COUNT = 25

# checking user is affiliatedcompany advisor or not
COMPANY_USER = 'company_user'
NOT_APPROVED = 'not_approved'
APPROVED = 'approved'
DIS_OWN = 'dis_own'

# value for advisor goal or LEVELS
CONNECTED = 'connected'
WELL_CONNECTED = 'well_connected'
HIGHLY_CONNECTED = 'highly_conneted'
TRUSTED = 'trusted'
LARGE_CLIENT_BASED = 'large_client_based'
MOST_TRUSTED = 'most_trusted'
TRUSTED_ECONOMIC_ADVISOR = 'trusted_economic_advisor'
FIRST_LEVEL_MINIMUM_ADVISOR_COUNT = 100
SECOND_LEVEL_MINIMUM_ADVISOR_COUNT = 500
MINIMUM_AVG_RATING = 3.0

# SSL certificate verification
SSL_VERIFY = True

# USER TYPE
MEMBER_TYPE = 'Member'

PROFILE_PICTURE = 'Profile Picture'
RECAPTCHA_KEY = '6LdemSEUAAAAAJ3gfqRs_7HOvWHTGVfceZya3FlQ'

# Social media page urls
FACEBOOK_PAGE_URL = 'https://www.facebook.com/upwrdz'
GOOGLE_PLUS_PAGE_URL = 'https://plus.google.com/u/0/108141008039962220017'
LINKEDIN_PAGE_URL = 'https://www.linkedin.com/company-beta/13320923'
TWITTER_PAGE_URL = 'https://twitter.com/upwrdz'
INDIAN_NATIONALITY = 'India'

# Linkedin OAuth Urls
LN_CALLBACK_URL = settings.DEFAULT_DOMAIN_URL + '/login/linkedin_callback/'
LN_AUTH_URL = 'https://www.linkedin.com/oauth/v2/authorization'
LN_TOKEN_URL = 'https://www.linkedin.com/oauth/v2/accessToken'
LN_GET_EMAIL_URL = 'https://api.linkedin.com/v2/emailAddress?q=members&projection=\
    (elements*(handle~))'
LN_GET_PROFILE_URL = 'https://api.linkedin.com/v2/me?projection=(id,firstName,lastName,\
    profilePicture(displayImage~:playableStreams))'

# Sociam media Share links
FACEBOOK_SHARE_URL = 'https://graph.facebook.com/oauth/access_token?'
GOOGLE_SHARE_URL = 'https://clients6.google.com/rpc'
LINKEDIN_SHARE_URL = "https://www.linkedin.com/countserv/count/share?url="

FB_GRAPH_URL = "https://graph.facebook.com/"

# EIPV Documents type
EIPV_AADHAAR = 'eipv_aadhaar'
EIPV_PANCARD = 'eipv_pancard'
EIPV_SIGNATURE = 'eipv_signature'
EIPV_FACE_CAPTURE = 'eipv_face_capture'
EIPV_PASSPORT = 'eipv_passport'
EIPV_IDCARD = 'eipv_idcard'
EIPV_DOCUMENT = 'eipv_doc'

# Documents Type
PAN_CARD = 'pan_card'
GOVT_PROOF = 'govt_proof'

# Source media constant sending to UPLYF
UPWRDZ_MEDIA = 'UPWRDZ'

# source media
SIGNUP_WITH_EMAIL = 'signup_with_email'
GOOGLE_MEDIA = 'google'
FACEBOOK_MEDIA = 'facebook'
LINKEDIN_MEDIA = 'linkedin'

MEMBER_SIGNUP_WITH_EMAIL = 'member_signup_with_email'
MEMBER_FACEBOOK_MEDIA = 'member_facebook'
MEMBER_GOOGLE_MEDIA = 'member_google'
MEMBER_LINKEDIN_MEDIA = 'member_linkedin'

# UPWRDZ support team Email-ID
UPWRDZ_SUPPORT = "info@abotmi.com"

# UPLYF user's status
NEW_UPLYF_USER = 'user_does_not_exist'
EXISTING_UPLYF_USER = 'existing_user'

# User Role's Constants
ADVISOR_ROLE = 'advisor'
MEMBER_ROLE = 'member'


# Blockchain Config
BLOCKCHAIN_URL = getattr(settings, "BLOCKCHAIN_URL", "")
BLOCKCHAIN_IP = getattr(settings, "BLOCKCHAIN_IP", "")
BLOCKCHAIN_PORT = getattr(settings, "BLOCKCHAIN_PORT", "")
BLOCKCHAIN_ADMIN_ACCOUNT = getattr(settings, "BLOCKCHAIN_ADMIN_ACCOUNT", "")
BLOCKCHAIN_ADMIN_PWD = getattr(settings, "BLOCKCHAIN_ADMIN_PWD", "")
BLOCKCHAIN_TLS = True
KYC_CONTRACT = "KYC_CONTRACT"

# Blockchain SSL Certification
BLOCKCHAIN_SSL_VERFIY = True

# SERVER DOMAINS
SERVER_DOMAINS = [
    'dev.abotmi.com',
    'test.abotmi.com',
    'abotmi.com',
    'prod.abotmi.com',
    'www.abotmi.com',
    'demo.abotmi.com'
]

# Page Titles
MY_IDENTITY = 'My Identity'
MY_HUB = 'My Hub'
MY_GROWTH = 'My Growth'
MY_REPUTE = 'My Repute'
PERSONAL_INFORMATION = 'Personal Information'
ADVISOR_REGISTRATION = 'Credibility Self Declaration'
BUSINESS_INFORMATION = 'Business Information'
MEETUP = 'Meetup'
WEBINAR = 'Webinar'
EIPV = 'E-IPV'
SET_PASSWORD = 'Set Password'
EKYC_AADHAAR = 'e-KYC Aadhaar'

# Advisor video shoot
VIDEO_REQUEST_STATUS = 'Requested'
VIDEO_REQUEST_APPROVED = 'Approved'
VIDEO_PUBLISH_STATUS = 'Published'
VIDEO_PUBLISH_APPROVED = 'Approved'
VIDEO_PUBLISH_REJECTED = 'Rejected'

# financial_instruments Constants
INSURANCE_FINANCIAL_INSTRUMENTS = 'Insurance'
EQUITY_FINANCIAL_INSTRUMENTS = 'Equity'
MUTUAL_FUND_FINANCIAL_INSTRUMENTS = 'Mutual Fund'

# Tables Used for Reputation index
TABLE_USER_PROFILE = "UserProfile"
TABLE_ADVISOR = 'Advisor'
TABLE_ADVISOR_RATING = 'AdvisorRating'
TABLE_TRACK_WEBINAR = 'TrackWebinar'
TABLE_MEETUP_EVENT = 'MeetUpEvent'
TABLE_BSE_DATA = 'BseData'
TABLE_COMPANY_ADVISOR_MAPPING = 'CompanyAdvisorMapping'

# Advisor check constatns
FIRM_NAME = 'firm_name'
CSRF_MIDDELWARE_TOKEN = 'csrfmiddlewaretoken'
PAGE = 'page'
IRDA_TABLE = 'IrdaData'
SEBI_TABLE = 'SebiData'
CA_TABLE = 'CaData'
AMFI_TABLE = 'AmfiData'
ADVISOR_DATA_TABLE = 'AdvisorData'
ADVISOR_CHECK_APP = 'advisor_check'
BSE_TABLE = 'BseData'

# OTP constant
OTP_MOBILE = 'otp_mobile'
OTP_EMAIL = 'otp_email'
OTP_TO_MOBILE = 'mobile'
OTP_TO_EMAIL = 'email'
OTP_TO_BOTH = 'both'
SIGNUP_OTP = 'signup_otp'

# micro learning Payment
MICRO_LEARNING_PAYMENT_NAME = 'MICRO LEARNING VIDEO Payment'

# REGION CODE
REGION_US = "US"
REGION_SG = "SG"
REGION_MY = "MY"
REGION_CA = "CA"
REGION_IN = "IN"
REGION_DEFAULT = REGION_IN

# Advisor Regulatory Columns
IRDA_STATUS_FIELD = 'irda_status'
AMFI_STATUS_FIELD = 'amfi_status'
SEBI_STATUS_FIELD = 'sebi_status'
REGULATORY_VERIFIED = 'verified'

# Regulatory Documents
SEBI_CERTIFICATE = 'sebi_certificate'
SEBI_RENEWAL_CERTIFICATE = 'sebi_renewal_certificate'
AMFI_CERTIFICATE = 'amfi_certificate'
AMFI_RENEWAL_CERTIFICATE = 'amfi_renewal_certificate'
IRDA_CERTIFICATE = 'irda_certificate'
IRDA_RENEWAL_CERTIFICATE = 'irda_renewal_certificate'
OTHER_CERTIFICATE = 'others_certificate'
OTHER_RENEWAL_CERTIFICATE = 'others_renewal_certificate'
RERA_CERTIFICATE = 'rera_certificate'
RERA_RENEWAL_CERTIFICATE = 'rera_renewal_certificate'

# Highest educational and additional education qualification certificates
HIGHEST_QUALIFICATION = 'highest_qualification_upload'
ADDITIONAL_EDUC_QUALIFICATION1 = 'document_edu_qua1'
ADDITIONAL_EDUC_QUALIFICATION2 = 'document_edu_qua2'
ADDITIONAL_EDUC_QUALIFICATION3 = 'document_edu_qua3'
ADDITIONAL_EDUC_QUALIFICATION4 = 'document_edu_qua4'
ADDITIONAL_EDUC_QUALIFICATION5 = 'document_edu_qua5'

# Education qualification categories
GRADUATION = 'Graduation'
POST_GRADUATION = 'Post Graduation'
DOCTORATE = 'Doctorate'
POST_DOCTORATE = 'Post Doctorate'
PROFESSIONAL_QUALIFICATION = 'Professional Qualification'
OTHER_QUALIFICATION = 'Other Qualification'

# PREMIUM INSTUTIONS LIST
PREMIUM_INSTUTIONS_LIST = [
    'IIMS',
    'XLRI',
    'IIFT',
    'SP Jain',
    'Jamanlal Bajaj Institute of Management Studies'
]

# HIGHEST EDUCATION DICT
HIGHEST_EDU_DICT = {
    POST_DOCTORATE : "post_doct",
    DOCTORATE : "doct",
    POST_GRADUATION : "post_graduation",
    GRADUATION : "graduation",
    PROFESSIONAL_QUALIFICATION : "prof_qualification",
    OTHER_QUALIFICATION : "other_qualification"
}

# Education category check list for special mba or diploma
EDU_CAT_SPL_IN_MBA_OR_DIP_LIST = [POST_DOCTORATE, DOCTORATE, POST_GRADUATION]

# Additional qualification in mba or diploma list
ADD_QUALIFICATION_IN_MBA_OR_DIP_LIST = [
    'MBA',
    'Diploma in Economics',
    'Diploma in  Financial'
]

# Proficiency in other subjects
PROF_IN_ADD_SUB = ['CA', 'CS', 'CFA', 'CIMA', 'ICWA']

# Following activities constants
IN_PROGRESS = 'in_progress'
FOLLOWING = 'following'
UNFOLLOW = 'unfollow'
DO_NOT_FOLLOW = 'do_not_follow'
DISCONNECTED = 'disconnected'
REJECTED = 'request_rejected'
PROFILE_URL = settings.DEFAULT_DOMAIN_URL+'/profile/'


# Follow activity url
ACCEPT_URL = settings.DEFAULT_DOMAIN_URL+'/dashboard/follower_advisor_mapping/'

# Give advice rating url
ADVICE_STATUS_URL = settings.DEFAULT_DOMAIN_URL+'/member/get_member_response/'
SHOW_PROFILE_URL = settings.DEFAULT_DOMAIN_URL+'/member/get_profile_details/'

# members status for the mail
ACCEPTED = 'accepted'
REJECTED = 'rejected'

# FASIA constants
FASIAAMERICA = 'FASIAAMERICA'
FASIA_DOMAIN = 'www.fasiaamerica.org'
FASIA_COMPANY_EMAIL = 'contact@fasiaamerica.org'

# MLEGION constants
MLEGION_CATEGORY = 'Investment'
MLEGION_SUB_CATEGORY = 'Real_estate'

# CRISIL Upload Document URLS
WPB_URL = settings.WPB_URL

# wpb course status
STUDY_INPROGRESS = 'Inprogress'
STUDY_COMPLETED = 'Completed'
STUDY_NEXT = 'Next'

FINCANCIAL_INSTRUMENTS = [
    'Equity',
    'Wealth Advisory',
    'Mutual Fund',
    'Insurance',
    'Real Estate',
    'Portfolio Management'
]
