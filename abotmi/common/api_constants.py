# All API Urls
from django.conf import settings

# UPWRDZ API Urls
UPWRDZ_AUTH_URL = settings.DEFAULT_DOMAIN_URL1 + '/api/get-auth-token/'
# Revenue API's
ADD_CLIENT_API = settings.DEFAULT_DOMAIN_URL1 + '/revenue/create-client/'
MAKE_TRANSACTIONS_API = settings.DEFAULT_DOMAIN_URL1 + '/revenue/make-transaction/'
ADVISOR_REVENUE_DETAILS_API = settings.DEFAULT_DOMAIN_URL1 + "/revenue/get-advisor-transactions/"
REVENUE_DETAILS_API = settings.DEFAULT_DOMAIN_URL1 + '/revenue/revenue-details/'


# UPLYF API Urls
# Member Urls
AUTH_URL = settings.UPLYF_SERVER + '/api/get-auth-token/'
ADD_MEMBER = settings.UPLYF_SERVER + '/api/accounts/user_referral/'
ADVISOR_MEMBER_MAPING = settings.UPLYF_SERVER + '/api/accounts/user_advisor_mapping/'

# Enquiry Management URLS
ENQUIRY_MANAGEMENT_DETAILS = settings.UPLYF_SERVER +'/api/member-advisor-selected/'
ENQUIRY_MANAGEMENT_ACCEPT_REJECT_STATUS = settings.UPLYF_SERVER + '/api/advisor-accept-reject/'
ENQUIRY_MANAGEMENT_ACCEPT_REJECT_LIST = settings.UPLYF_SERVER + '/api/list-advisor-enquiry-list/'

# Project Details URLS
UPLYF_PROJECT_DETAILS =settings.UPLYF_SERVER+'/api/savings/reingo-project-card/'
UPLYF_PROJECT_NAMES = settings.UPLYF_SERVER + '/api/get-project-names/'

# Go to UPLYF button URL
UPLYF_USER = settings.UPLYF_SERVER +'/api/advisors/check_and_register/'
UPLYF_USER_LOGIN = settings.UPLYF_SERVER +'/api/advisors/check_auth_and_redirect/'
CHECK_UPLYF_USER = settings.UPLYF_SERVER +'/api/advisors/check_user_email/'

# Client Management URLS
VIEW_MEMBERS_DETAILS = settings.UPLYF_SERVER+'/api/accounts/advisor_mapped_all_users/'
VIEW_INVITED_MEMBERS_DETAILS = settings.UPLYF_SERVER+'/api/accounts/advisor_user_invited/'

# ADVIOSRS UPLYF Transcations URLS
GET_UPLYF_TRANSACTIONS = settings.UPLYF_SERVER + '/api/advisors/get_advisor_transactions/'
UPLOAD_REINGO_TRANSACTION_DOCUMENT_URL = settings.UPLYF_SERVER + '/api/upload_reingo_transactions/'

# Send updated event details to UPLYF
SEND_UPDATED_EVENT = settings.UPLYF_SERVER + '/api/common/send_email_after_updating_event/'
SEND_DELETED_EVENT_DATA = settings.UPLYF_SERVER + '/api/common/send_email_after_deleting_event/'

# MLEGION URLS
MLEGION_AUTH_TOKEN_URL = settings.MLEGION_SERVER + '/auth_token'
GET_ADVISORS_EVENTS = settings.MLEGION_SERVER + '/get_individual_events'
DELETE_EVENTS = settings.MLEGION_SERVER + '/delete_event'
CREATE_EVENTS = settings.MLEGION_SERVER + '/create_event'
UPDATE_EVENTS = settings.MLEGION_SERVER + '/update_event'

# Common URL Constants
USER_UPLOAD_DOCUMENTS_LINK = settings.DEFAULT_DOMAIN_URL + "/signup/submit_documents/"
NEXT_URL_LINK = settings.DEFAULT_DOMAIN_URL + '/'
REFERRAL_LINK = settings.DEFAULT_DOMAIN_URL + "/signup/?ref_link="
DISOWN_LINK = settings.DEFAULT_DOMAIN_URL + "/dashboard/disown_member_api/"

# Single page social media URL link
GOOGLE_SINGLE_URL = settings.DEFAULT_DOMAIN_URL + "/login/google_sm/"
FACEBOOK_SINGLE_URL = settings.DEFAULT_DOMAIN_URL + "/login/facebook_sm/"
LINKEDIN_SINGLE_URL = settings.DEFAULT_DOMAIN_URL + "/login/linkedin_sm/"
