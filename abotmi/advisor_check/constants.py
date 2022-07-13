from django.conf import settings

ADVISOR_TYPE = 'ADVISOR_CHECK'

NOT_APPROVED = 'not_approved'

SIGNUP_WITH_EMAIL = 'signup_with_email'

'''
constants for  pagination in the search
'''
CARDS_PER_PAGE = 15
PAGE_RANGE = 5
START_PAGES = 10

# Advisor check registration number fields
IRDA_REG_FIELD = 'irda_urn'
SEBI_REG_FIELD = 'reg_no'
AMFI_REG_FIELD = 'arn'
CA_REG_FIELD = 'reg_id'
BSE_REG_FIELD = 'bse_clearing_number'
MY_REG_FIELD = 'licence_number'
SG_REG_FIELD = 'member_number'
US_REG_FIELD = 'lic_id'

# Advisor table registraion number fields
IRDA_NUMBER = 'irda_number'
SEBI_NUMBER = 'sebi_number'
AMFI_NUMBER = 'amfi_number'

# Claimed status
CLAIMED_STATUS_VERIFIED = 'verified'
CLAIMED_STATUS_NOT_VERIFIED = 'not_verified'

# Category types
CATEGORY_OTHER = 'other'

# Page Titles
SEARCH = 'Search'
ADVISOR_CHECK = 'Advisor Check'

# page types
ADVISOR_PROFILE = 'profile'
ADVISOR_REPUTE = 'repute'

# PAGE URLS
''' need to pass -> %(id, catogery_type) '''
AD_CHK_PROFILE_URL = settings.DEFAULT_DOMAIN_URL+'/advisor_check/profile/%s/%s/'
''' need to pass -> %(batchcode) '''
ABOTMI_PROFILE_URL = settings.DEFAULT_DOMAIN_URL+'/profile/%s/'
''' need to pass -> %(batchcode) '''
ABOTMI_REPUTE_URL = settings.DEFAULT_DOMAIN_URL+'/repute_index/%s/'

# Action Type
VIEW = 'view'
