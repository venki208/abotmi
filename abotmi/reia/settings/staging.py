from .base import *

DEBUG = False

# Session Poliyc
SESSION_COOKIE_HTTPONLY = True
SESSION_ENGINE = 'encrypted_cookies'
ENCRYPTED_COOKIE_KEYS = ['kmYZJ7W6yL9kdz-dA4tv_qXoAMQ_Dbl64BRh2RJFeAE=']

#  Allowed Hosts
ALLOWED_HOSTS = [
    'stg.abotmi.com'
]

DEFAULT_DOMAIN_NAME = 'stg.abotmi.com'
DEFAULT_DOMAIN_URL = 'https://' + DEFAULT_DOMAIN_NAME
DEFAULT_DOMAIN_URL1 = DEFAULT_DOMAIN_URL
DEFAULT_HOST = DEFAULT_DOMAIN_NAME

# Textient Rank URLS
RANK_API_KEY = "y82QiA9dfH2DsnLr7q8sX5xzQikeMDdT97I4auv2"
RANK_API_URL = "https://rankapi.int.textient.com/v1"

# Block Chain URLS
BLOCKCHAIN_URL = "https://devbc.upwrdz.com"
BLOCKCHAIN_IP = "devbc.upwrdz.com"
BLOCKCHAIN_PORT = 443
BLOCKCHAIN_ADMIN_ACCOUNT = "0x0e5b3ef7ca7e770bb5762fe2e3c83bb207489d3f"
BLOCKCHAIN_ADMIN_PWD = "restart"

# AWS S3 Bucket Settings
AWS_S3_ACCESS_KEY_ID = None  # django-storages will be ablet to get using boto
AWS_S3_SECRET_ACCESS_KEY = None  # django-storages will be ablet to get using boto
AWS_STORAGE_BUCKET_NAME = "stgabotmi-prod"
AWS_S3_CUSTOM_DOMAIN = DEFAULT_DOMAIN_NAME
AWS_S3_URL_PROTOCOL = "https:"
AWS_S3_REGION_NAME = 'us-west-1'
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_S3_FILE_OVERWRITE = True
AWS_S3_OBJECT_PARAMETERS = {
    'ServerSideEncryption': 'aws:kms',
    'SSEKMSKeyId': '783c1a74-bbdc-4df1-8440-0f4a1a31b4fe'
}

# MEDIA PATH for S3
MEDIA_ROOT = "/"
MEDIA_URL = "/media/"
DEFAULT_FILE_STORAGE = "filestorage.MediaRootS3BotoStorage"

# MAINTENANCE_MODE Settings
# if True the maintenance-mode will be activated
MAINTENANCE_MODE = False
# if True the staff will not see the maintenance-mode page
MAINTENANCE_MODE_IGNORE_STAFF = False
# if True the superuser will not see the maintenance-mode page
MAINTENANCE_MODE_IGNORE_SUPERUSER = False
# list of ip-addresses that will not be affected by the maintenance-mode
# ip-addresses will be used to compile regular expressions objects
MAINTENANCE_MODE_IGNORE_IP_ADDRESSES = ()
# list of urls that will not be affected by the maintenance-mode
# urls will be used to compile regular expressions objects
MAINTENANCE_MODE_IGNORE_URLS = ()
# the absolute url where users will be redirected to during maintenance-mode
MAINTENANCE_MODE_REDIRECT_URL = None
# the template that will be shown by the maintenance-mode page
MAINTENANCE_MODE_TEMPLATE = '503.html'
'''the path of the function that will return the template context -> 
    "myapp.mymodule.myfunction" 
'''
MAINTENANCE_MODE_TEMPLATE_CONTEXT = None

# Social Media Api Keys
FACEBOOK_API = "2198091720224091"
FACEBOOK_APP_SECRET = "727a74b7d024c0312339af773e10ab80"
GOOGLE_CLIENTID = \
    "694526678521-gi680vetg016n0g2bfpevkmecmo68il1.apps.googleusercontent.com"
LINKEDIN_API = "8167t78er6wycq"

# Social Media Redirect URLs
GOOGLE_REDIRECT = DEFAULT_DOMAIN_URL
LINKEDIN_SUBMITTED_URL = DEFAULT_DOMAIN_URL
LINKEDIN_IMAGE_URL = DEFAULT_DOMAIN_URL + "/static/images/sm-banner.jpg"

# Aadhaar request urls
AADHAAR_INITIATION_URL = 'https://prod.aadhaarbridge.com/kua/_init'
AADHAAR_FETCH_KYC_URL = 'https://prod.aadhaarbridge.com/kua/_kyc'

# IPINFO TOKEN
IP_INFO_TOKEN = "bac2b54bea24c5"

# ICORE DETAILS
ICORE_HOST = "https://icoreindia.com"
ICORE_PORT = "443"
ICORE_API_URL = ICORE_HOST + ":" + ICORE_PORT + "/wp-json"
ICORE_WP_URL = ICORE_HOST + ":" + ICORE_PORT + "/wp-admin"
ICORE_ADMIN = "nfadmin"
ICORE_ADMIN_PWD = "NF@1.6fib"
ICORE_XMLRPC = "https://test.icoreindia.com:443/xmlrpc.php"

# UPLYF Server name
UPLYF_TITLE = 'UPLYF'
UPLYF_SERVER = 'https://uplyf.com'
UPLYF_USER_NAME = 'reiaspoc@reiaglobal.com'
UPLYF_PASSWORD = 'reiaspoc@testmobisir'
UPLYF_PORT = "443"
UPLYF_URL = UPLYF_SERVER + ":" + UPLYF_PORT
UPLYF_AUTH_URL = UPLYF_URL + '/api/get_auth_token'
UPLYF_TOKEN = None

UPWRDZ_USERNAME = 'upwrdzspoc@mobisir.net'
UPWRDZ_PASSWORD = 'upwrdzspoc@mobisir'

# MLEGION Server name
MLEGION_SERVER = 'https://test.mlegion.net'
MLEGION_USERNAME = 'upwrdzdevspoc@upwrdz.com'
MLEGION_PASSWORD = 'upwrdzspoc@devmobisir'


# WPB SPOC DETAILS
WPB_HOST = 'https://test.whitepolarbear.org'
WPB_PORT = '8020'
WPB_URL = WPB_HOST
WPB_AUTH_URL = WPB_URL + '/api/user/get-auth-login/'
WPB_USER_ID = "admin@wpb.org"
WPB_PASSWORD = "wpbadmin@123#"
WPB_TOKEN = None

# encrypt key
ENCRYPT_KEY = b's3cLJ71igTZRN37VcexCE7BNJtzrwHg6vQB16g_aLGw='
# Intializing Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'reialogformat': {
            'format': "%(asctime)s|%(levelname)s|%(name)s:%(lineno)s|ACTION: %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/home/abotmi/abotmi/logs/abotmi.log',
            'formatter': 'reialogformat',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
        },
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'INFO',
            'formatter': 'reialogformat'
        },
    },
    'nfadmin': {
        '': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'formatter': 'verbose'
        },
    },
}
