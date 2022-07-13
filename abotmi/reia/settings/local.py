from .base import *

DEBUG = True

ALLOWED_HOSTS = []

# Adding local env additional application
INSTALLED_APPS += (
    'debug_toolbar',
)

STATICFILES_FINDERS += (
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')

DEFAULT_DOMAIN_NAME = 'localhost:8000'
DEFAULT_DOMAIN_URL = 'http://' + DEFAULT_DOMAIN_NAME
DEFAULT_DOMAIN_URL1 = DEFAULT_DOMAIN_URL
DEFAULT_HOST = DEFAULT_DOMAIN_NAME

RANK_API_KEY = "y82QiA9dfH2DsnLr7q8sX5xzQikeMDdT97I4auv2"
RANK_API_URL = "https://192.168.0.202/v1"
MEETUP_GROUP_NAME = "upwrdz-meetup-group"
MEETUP_KEY = "33e411b637f44447b4a795c335c471a"
BLOCKCHAIN_URL = "https://devbc.upwrdz.com"
BLOCKCHAIN_IP = "devbc.upwrdz.com"
BLOCKCHAIN_PORT = 443
BLOCKCHAIN_ADMIN_ACCOUNT = "0x0e5b3ef7ca7e770bb5762fe2e3c83bb207489d3f"
BLOCKCHAIN_ADMIN_PWD = "restart"

# Social Media Api Keys
FACEBOOK_API = "278212815921681"
FACEBOOK_APP_SECRET = "5a6b654ccccf0ef726b9fbcf0ab4d863"
GOOGLE_CLIENTID = "266742724883-g2al1rhd2c8ejulvhn6pn439o2h3goos.apps.googleusercontent.com"
LINKEDIN_API = "75xgpkd7ynz4hy"

# Social Media Redirect URLs
GOOGLE_REDIRECT = DEFAULT_DOMAIN_URL
LINKEDIN_SUBMITTED_URL = DEFAULT_DOMAIN_URL
LINKEDIN_IMAGE_URL = DEFAULT_DOMAIN_URL+"/static/images/sm-banner.jpg"
# =====================================================================

# Aadhaar request urls
AADHAAR_INITIATION_URL = 'https://prod.aadhaarbridge.com/kua/_init'
AADHAAR_FETCH_KYC_URL = 'https://prod.aadhaarbridge.com/kua/_kyc'

# IPINFO TOKEN
IP_INFO_TOKEN = "bac2b54bea24c5"

# ICORE DETAILS
ICORE_HOST = "https://test.icoreindia.com"
ICORE_PORT = "443"
ICORE_API_URL = ICORE_HOST+":"+ICORE_PORT+"/wp-json"
ICORE_WP_URL = ICORE_HOST+":"+ICORE_PORT+"/wp-admin"
ICORE_ADMIN = "nfadmin"
ICORE_ADMIN_PWD = "NF@1.6fib"
ICORE_XMLRPC = "https://test.icoreindia.com:443/xmlrpc.php"

# UPLYF Server name
UPLYF_TITLE = 'UPLYF'
UPLYF_SERVER = 'http://localhost:8000'
UPLYF_USER_NAME = 'admin@mobisir.net'
UPLYF_PASSWORD = 'nftp@123#'
UPLYF_PORT = "443"
UPLYF_URL = UPLYF_SERVER+":"+UPLYF_PORT
UPLYF_AUTH_URL = UPLYF_URL+'/api/get_auth_token'
UPLYF_TOKEN = None

UPWRDZ_USERNAME = 'admin@mobisir.net'
UPWRDZ_PASSWORD = 'nftp@123#'

# MLEGION Server name
MLEGION_SERVER = 'http://localhost:5000'
MLEGION_USERNAME = 'admin@mobisir.net'
MLEGION_PASSWORD = 'nftp@123#'

# WPB SPOC DETAILS
WPB_HOST = 'https://dev.whitepolarbear.org'
WPB_PORT = '8020'
WPB_URL = WPB_HOST
WPB_AUTH_URL = WPB_URL+'/api/user/get-auth-login/'
WPB_USER_ID = "admin@wpb.org"
WPB_PASSWORD = "wpbadmin@123#"
WPB_TOKEN = None

# Linkedin keys
LINKEDIN_CLIENT_ID = ""
LINKEDIN_SECRET_ID = ""

LINKEDIN_REDIRECT_URI = DEFAULT_DOMAIN_URL + '/login/linkedin_callback/'
LINKEDIN_STATE = ''

# encrypt key
ENCRYPT_KEY = b's3cLJ71igTZRN37VcexCE7BNJtzrwHg6vQB16g_aLGw='
# ====================================================================
# LOGGING Settings
# ====================================================================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'reia.log',
            'formatter': 'verbose'
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django': {
            'handlers':['file'],
            'propagate': True,
            'level':'DEBUG',
        },
        'django.request': {
           'handlers': ['file'],
           'propagate': False,
           'level': 'DEBUG'
        },
        'login': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        'signup': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        'home': {
            'handlers':['file'],
            'level' : 'DEBUG',
        },
        'nfadmin':{
            'handlers':['console'],
            'level': 'DEBUG',
        },
        'api': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'uploader':{

            'handlers': ['file'],
            'level': 'DEBUG',

        }
    }
}
# ====================================================================

REDIS_CONNECTION_URI = os.environ.get("REDIS_CONNECTION_URI", "redis://:redisAdmin@localhost:6379")
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(REDIS_CONNECTION_URI)],
        },
        "ROUTING": "reia.routing.channel_routing",
    }
}