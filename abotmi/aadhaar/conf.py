from django.conf import settings

AADHAR_BRIDGE_OTP = None
AADHAR_BRIDGE_KYC = None
AADHAR_BRIDGE_CHANNEL = None
AADHAR_BRIDGE_CERTIFICATE_TYPE = None
AADHAAR_SACODE = "0b484d" #This code is for REIA adhaar bridge
AADHAAR_SALT = "28a3261a16" #This code is for REIA adhaar bridge
UPLYF_URL = settings.DEFAULT_DOMAIN_URL+'/#/save'
AADHAAR_SUCCESS_URL = settings.DEFAULT_DOMAIN_URL + '/aadhaar/success'
AADHAAR_FAILURE_URL = settings.DEFAULT_DOMAIN_URL + '/aadhaar/failed'
AADHAR_MOBILE_SUCESSS_URL = settings.DEFAULT_DOMAIN_URL + '/static/www/index.html#/eKYCsuccess'
AADHAR_MOBILE_FAILURE_URL = settings.DEFAULT_DOMAIN_URL + '/static/www/index.html#/eKYCfailure'
AADHAAR_ADVISOR_STR = "advisor"
AADHAAR_MEMBER_STR = "member"
AADHAAR_MEMBER_SUCCESS_URL = settings.DEFAULT_DOMAIN_URL + '/aadhaar/member_success'
AADHAAR_MEMBER_FAILRE_URL = settings.DEFAULT_DOMAIN_URL + '/aadhaar/member_failed'
AADHAAR_MOBI_MEMBER_SUCCESS_URL = settings.DEFAULT_DOMAIN_URL + '/static/index.html#/member_eKYCsuccess'
AADHAAR_MOBI_MEMBER_FAILURE_URL = settings.DEFAULT_DOMAIN_URL + '/static/index.html#/member_eKYCfailure'

# Production url
AADHAAR_INITIATION_URL =  settings.AADHAAR_INITIATION_URL
AADHAAR_FETCH_KYC_URL = settings.AADHAAR_FETCH_KYC_URL

AADHAAR_MOBILE_MEMBER_SUCCESS_URL = settings.DEFAULT_DOMAIN_URL + '/static/www/index.html#/eKYCsuccess?type="mobile"'
AADHAAR_MOBILE_MEMBER_FAILURE_URL = settings.DEFAULT_DOMAIN_URL + '/static/www/index.html#/eKYCfailure?type="mobile"'

AADHAAR_FAILURE_EMAIL_SEND_TO = "devops@mobisir.net"
AADHAAR_ERROR_CODE = ["AB-203", "AB-208", "AB-209", "AB-211", "AB-212", "AB-213", "AB-214", "AB-215"]
# AADHAAR_FAILURE_EMAIL_TO_ADMIN = "REIA_22"


def get_ab_214_error_meaning():
    return "Failure of the first request of the month (after billing) because balance is lower than the monthly minimum"


def get_ab_208_error_meaning():
    return "Invalid environment(make sure you are fetching data from environment in which eKYC wasperformed)"

AADHAAR_ERROR_CODE_MEANING = {
    "AB-203": "Invalid Sub-AUA code",
    "AB-208": get_ab_208_error_meaning(),
    "AB-209": "Contact us",
    "AB-211": "Plan is not active",
    "AB-212": "Plan is expired",
    "AB-213": "Insufficient Api Count",
    "AB-214": get_ab_214_error_meaning(),
    "AB-215": "Insufficient balance to perform kyc"
}


# if settings.AADHAR_BRIDGE_CHANNEL:
#     AADHAR_BRIDGE_CHANNEL = settings.AADHAR_BRIDGE_CHANNEL
# else:
#     AADHAR_BRIDGE_CHANNEL = "SMS"
#
# if settings.AADHAR_BRIDGE_CERTIFICATE_TYPE:
#     AADHAR_BRIDGE_CERTIFICATE_TYPE = settings.AADHAR_BRIDGE_CERTIFICATE_TYPE
# else:
#     AADHAR_BRIDGE_CERTIFICATE_TYPE = "prod"
