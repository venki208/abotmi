from django.conf import settings  # import the settings file
from common.constants import (
    FACEBOOK_PAGE_URL, GOOGLE_PLUS_PAGE_URL, LINKEDIN_PAGE_URL, TWITTER_PAGE_URL,
)
from common.api_constants import (
    GOOGLE_SINGLE_URL, FACEBOOK_SINGLE_URL, LINKEDIN_SINGLE_URL
)


def general_settings(request):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return_dict = {
        'LOGIN_URL': settings.LOGIN_URL,
        'FACEBOOK_API': settings.FACEBOOK_API,
        'LINKEDIN_SUBMITTED_URL': settings.LINKEDIN_SUBMITTED_URL,
        'FACEBOOK_SINGLE_URL': FACEBOOK_SINGLE_URL,
        'FACEBOOK_PAGE_URL': FACEBOOK_PAGE_URL,
        'GOOGLE_PLUS_PAGE_URL': GOOGLE_PLUS_PAGE_URL,
        'LINKEDIN_PAGE_URL': LINKEDIN_PAGE_URL,
        'TWITTER_PAGE_URL': TWITTER_PAGE_URL,
        'DEFAULT_DOMAIN_URL': settings.DEFAULT_DOMAIN_URL
    }
    return return_dict
