from .base import *

DEBUG = True

# Session Poliyc
SESSION_COOKIE_HTTPONLY = True
SESSION_ENGINE = 'encrypted_cookies'
ENCRYPTED_COOKIE_KEYS = ['kmYZJ7W6yL9kdz-dA4tv_qXoAMQ_Dbl64BRh2RJFeAE=']

#  Allowed Hosts
ALLOWED_HOSTS = [
    'dev2.abotmi.com'
]

DEFAULT_DOMAIN_NAME = 'dev2.abotmi.com'
DEFAULT_DOMAIN_URL = 'https://' + DEFAULT_DOMAIN_NAME
DEFAULT_DOMAIN_URL1 = DEFAULT_DOMAIN_URL
DEFAULT_HOST = DEFAULT_DOMAIN_NAME

# Textient Rank URLS
RANK_API_KEY = "y82QiA9dfH2DsnLr7q8sX5xzQikeMDdT97I4auv2"
RANK_API_URL = "https://35.154.213.92/v1"

# Block Chain URLS
BLOCKCHAIN_URL = "https://devbc.upwrdz.com"
BLOCKCHAIN_IP = "devbc.upwrdz.com"
BLOCKCHAIN_PORT = 443
BLOCKCHAIN_ADMIN_ACCOUNT = "0x0e5b3ef7ca7e770bb5762fe2e3c83bb207489d3f"
BLOCKCHAIN_ADMIN_PWD = "restart"

# AWS S3 Bucket Settings
AWS_S3_ACCESS_KEY_ID = None  # django-storages will be able to get using boto
AWS_S3_SECRET_ACCESS_KEY = None  # django-storages will be able to get using boto
AWS_STORAGE_BUCKET_NAME = "abotmi-dev"
AWS_S3_CUSTOM_DOMAIN = DEFAULT_DOMAIN_NAME
AWS_S3_URL_PROTOCOL = "https:"
AWS_S3_REGION_NAME = 'us-west-1'
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_S3_FILE_OVERWRITE = True
AWS_S3_OBJECT_PARAMETERS = {
    'ServerSideEncryption': 'aws:kms',
    'SSEKMSKeyId': '3e0b975c-a204-400c-a89c-be36579815c1'
}

# MEDIA PATH for S3
MEDIA_ROOT = "/"
MEDIA_URL = "/media/"
DEFAULT_FILE_STORAGE = "filestorage.MediaRootS3BotoStorage"

# Social Media Api Keys
# Dev - API KEY : 2711966822361945 --> App Secret : 03912ce9472a18b757b352d06b101613
# Dev2 - API KEY : 2243027219304910 --> App Secret : 68dee48c42197552799b96a5a800f132
FACEBOOK_API = "2243027219304910"
FACEBOOK_APP_SECRET = "bc9263914d6b72945b8ec674a7fb31fc"
GOOGLE_CLIENTID = \
    "694526678521-mef1q2ctm0aicevuu8e285rog7kmijrd.apps.googleusercontent.com"

# dev server linkedin keys
# client_id --> "81ogys10jzqmyh"
# secret_id --> "nz1e3MvTHOY9yOMs"
# dev2 server linkedin keys
# client_id --> "81tayio8n5ksj6"
# secret_id --> "Tz8PW9niCoTKt1DP"
LINKEDIN_CLIENT_ID = "81tayio8n5ksj6"
LINKEDIN_SECRET_ID = "Tz8PW9niCoTKt1DP"

LINKEDIN_REDIRECT_URI = DEFAULT_DOMAIN_URL + '/login/linkedin_callback/'
LINKEDIN_STATE = 'DCEeFWf45A53sdfKef42412'

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
UPLYF_SERVER = 'https://dev.uplyf.com'
UPLYF_USER_NAME = 'reiadevspoc@reiaglobal.com'
UPLYF_PASSWORD = 'reiaspoc@devmobisir'
UPLYF_PORT = "443"
UPLYF_URL = UPLYF_SERVER + ":" + UPLYF_PORT
UPLYF_AUTH_URL = UPLYF_URL + '/api/get_auth_token'
UPLYF_TOKEN = None

UPWRDZ_USERNAME = "admin@mobisir.net"
UPWRDZ_PASSWORD = "devreiaglobal@mobisir"

# MLEGION Server name
MLEGION_SERVER = 'https://dev.mlegion.net'
MLEGION_USERNAME = 'upwrdzdevspoc@upwrdz.com'
MLEGION_PASSWORD = 'upwrdzspoc@devmobisir'


# WPB SPOC DETAILS
WPB_HOST = 'https://dev.whitepolarbear.org'
WPB_PORT = '8020'
WPB_URL = WPB_HOST
WPB_AUTH_URL = WPB_URL+'/api/user/get-auth-login/'
WPB_USER_ID = "abotmispoc@gmail.com"
WPB_PASSWORD = "devaBotmispoc@123"
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
