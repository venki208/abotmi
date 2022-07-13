import os
import datetime
import json

from django.core.exceptions import ImproperlyConfigured
from mongoengine import connect

# with open('/home/abotmi/abotmi/config/dev_config.json') as f:
with open(os.environ.get('ABOTMI_SETTINGS')) as f:
    configs = json.loads(f.read())


def get_env_var(setting, configs=configs):
    '''
    Gets the value from ABOTMI_SETTINGS
    '''
    try:
        val = configs[setting]
        if val == 'True':
            val = True
        elif val == 'False':
            val = False
        return val
    except KeyError:
        error_msg = "ImproperlyConfigured: Set {0} environment variable".format(
            setting)
        raise ImproperlyConfigured(error_msg)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SECRET_KEY = 'syzg-=ovamkuuyx)y^zppfs$ps0l=53(c@)fz+d7yyg4)fc@27'

# Apps bundled with Django
DEFAULT_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
)

# Third party apps
THIRD_PARTY_APPS = (
    'widget_tweaks',
    'django_mandrill',
    'storages',
    'datetimewidget',
    'simple_history',
    'longerusernameandemail',
    'maintenance_mode',
    'rest_framework',
    'mathfilters',
    'channels',
)

# ABOTMI Apps
LOCAL_APPS = (
    'signup',
    'login',
    'home',
    'blog',
    'nfadmin',
    'blockchain',
    'datacenter',
    'dashboard',
    'common',
    'logAll',
    'company',
    'advisor_check',
    'nsdl',
    'reputation_index',
    'my_identity',
    'revenue',
    'my_growth',
    'reputation_index_signals',
    'my_repute',
    'member'
)
INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Django Middleware Class
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'login.middleware.LoginRequiredMiddleware',
    'logAll.middleware.LogAllMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    'maintenance_mode.middleware.MaintenanceModeMiddleware',
)

ROOT_URLCONF = 'reia.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'login.context_processors.general_settings',
                'common.context_processors.crisil_status_flags',
                'common.context_processors.common_objects',
                'common.context_processors.ip_country',
                'common.context_processors.common_constants',
            ],
            'loaders': [
                'app_namespace.Loader',
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]

WSGI_APPLICATION = 'reia.wsgi.application'

ADVISOR_CHECK_DB_ALIAS = "advisor_check"
DATABASES = {
    "default": {
        "ENGINE": get_env_var("nfdb_ENGINE"),
        "NAME": get_env_var("nfdb_NAME"),
        "USER": get_env_var("nfdb_USER"),
        "PASSWORD": get_env_var("nfdb_PASSWORD"),
        "HOST": get_env_var("nfdb_HOST"),
        "PORT": get_env_var("nfdb_PORT"),
    },
    "advisor_check": {
        "ENGINE": get_env_var("advisor_chk_ENGINE"),
        "NAME": get_env_var("advisor_chk_NAME"),
        "USER": get_env_var("advisor_chk_USER"),
        "PASSWORD": get_env_var("advisor_chk_PASSWORD"),
        "HOST": get_env_var("advisor_chk_HOST"),
        "PORT": get_env_var("advisor_chk_PORT"),
    }
}

DATABASE_ROUTERS = ['advisor_check.routers.AdvisorCheckRouter']

# Mongo Database Connection
connect(
    db=get_env_var('mongo_db'),
    username=get_env_var('mongo_username'),
    password=get_env_var('mongo_password'),
    host=get_env_var('mongo_host')
)


# cache database configuration
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://:redisAdmin@127.0.0.1:6379/1",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient"
#         }
#     }
# }
# --------------------------------------------------------------------
# WebSocket CHANNEL_LAYERS : Redis Settings
# --------------------------------------------------------------------
# REDIS_CONNECTION_URI = os.environ.get("REDIS_CONNECTION_URI", "redis://:redisAdmin@localhost:6379")
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "asgi_redis.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [(REDIS_CONNECTION_URI)],
#         },
#         "ROUTING": "reia.routing.channel_routing",
#     }
# }
# ASGI_APPLICATION = "reia.asgi.application"

# Cache time to live is 5 minutes in general.
CACHE_TTL = 60 * 5

AUTH_PROFILE_MODULE = 'datacenter.UserProfile'

# DataBase Fixtures
FIXTURE_DIRS = (os.path.join(BASE_DIR, 'fixtures'),)

# Rest FrameWork
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=30000),
    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Calcutta'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static")
LOADING_STATIC_FOR_PDF = os.path.join(BASE_DIR, "static")

MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')

LOGIN_URL = '/'
LOGOUT_URL = '/logout'
LOGIN_REDIRECT_URL = '/home/'

LOGIN_EXEMPT_URLS = (
    r'^get_in_touch/',
    r'^contact_us_reia/',
    r'^signup/*',
    r'^api/*',  # allow the entire /* subsection
    r'^blog/feed/',  # allow the entire RSS /* subsection
    r'^terms_and_condition/',
    r'^privacy_and_policy/',
    r'^disclaimer_reia/',
    r'^dashboard/disown_member_api/(?P<referral_code>[a-zA-Z0-9]+)/$',
    r'^steps_to_recover_password/',
    r'^company/',
    r'^server_health/*',
    r'^reputation-index/*',
    r'^revenue/*',
    r'^guest/(?P<slug>[a-zA-Z0-9]+)/',
    r'^my_identity/save_guest_details/',
    r'^digital-identity-modal/',
    r'^micro-learning-modal/',
    r'^reputation-index-modal/',
    r'^load-reputation-video-modal/',
    r'^dashboard/follower_advisor_mapping/',
    r'^member/get_member_response/',
    r'^member/get_member_rating',
    r'^member/get_profile_details/',
    r'^summary_of_abotmi_privacy_policy/',
    r'^code_of_coduct/',
    r'^get_advice_page/',
    r'^build_page/',
    r'^opportunities_page/',
    r'^my_repute/my_repute_static/',
    r'^summary_of_terms_condtions/',
    r'^advisor_page/',
    r'^cookie_policy/',
    r'^copyright_policy/',
    r'^ethical_commitment_page/',
    r'^my_repute/manage_reputation/',
    r'^my_repute/build_reputation/',
    r'^my_repute/share_reputation/',
    r'^purpose_page/',
    r'^people_page/',
    r'^partners_page/',
    r'^protection_page/',
    r'^refer_advice_page/',
    r'^rate_advice_page/',
    r'^abotmi_faq/',
    r'^how_it_work/',
    r'^refer_friend/',
    r'^about_us/',
    r'^why_us/',
    r'^investors/',
    r'^advisors/',
    r'^login/linkedin/',
    r'^login/linkedin_callback/',
    r'^notification/',
)

WKHTMLTOPDF_CMD = '/usr/bin/wkhtmltopdf'

EMAIL_BACKEND = 'django_mandrill.mail.backends.mandrillbackend.EmailBackend'
MANDRILL_API_KEY = "T17HP-nB5NEYp8sYrqQ1PQ"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'northfacing.in@gmail.com'
EMAIL_HOST_PASSWORD = 'northfacing@vol'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

REIA_ADMIN_EMAIL = 'contact@abotmi.com'

# ClickMeeting Webinar API KEY
WEBINAR_API_KEY = "us131b149b26896d341ee0d9ba5bbca6f03bb59a4e"

# Social Media Counter
SOCIAL_MEDIA_COUNT_URL = "https://free.sharedcount.com/url"
SHARED_COUNT_API_KEY = "8e22999cdb80b4c148986a8a83702f712da2897c"

LOGALL_LOG_HTML_RESPONSE = False

# Social Media Counter
SOCIAL_MEDIA_COUNT_URL = "https://free.sharedcount.com/url"
SHARED_COUNT_API_KEY = "8e22999cdb80b4c148986a8a83702f712da2897c"

# SMS Integration Details
SMS_URL = 'http://sms.valueleaf.com/sms/user/urlsms.php'
SMS_API = 'A22b641e72abf752bce522605284a9bcc'
SMS_SENDER_ID = 'UPWRDZ'
SMS_USERNAME = "mobisirnf"
SMS_PASSWORD = "Go to meeting@10am"

# Textient API AI
RANK_API_KEY = "y82QiA9dfH2DsnLr7q8sX5xzQikeMDdT97I4auv2"
RANK_API_URL = "https://rankapi.int.textient.com/v1"

# IP Location : ipinfo.io token
IP_INFO_URL = "https://ipinfo.io"
IP_INFO_TOKEN = "bac2b54bea24c5"

PRODUCT_NAME = 'UPWRDZ'

ADMINS = (
            ('venkatesh duddu', 'venkateshraja08@gmail.com'),
            ('Yamini', 'yamini.m@ptgindia.com')
        )

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