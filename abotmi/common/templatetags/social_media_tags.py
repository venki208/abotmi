from django import template
from django.conf import settings

from common.api_constants import (
    GOOGLE_SINGLE_URL, FACEBOOK_SINGLE_URL, LINKEDIN_SINGLE_URL
)

register = template.Library()


@register.simple_tag
def get_social_media(name):
    context_dict = {
        'LOGIN_URL': settings.LOGIN_URL,
        'FACEBOOK_API': settings.FACEBOOK_API,
        'GOOGLE_CLIENTID': settings.GOOGLE_CLIENTID,
        'GOOGLE_REDIRECT': settings.GOOGLE_REDIRECT,
        'LINKEDIN_API': settings.LINKEDIN_API,
        'LINKEDIN_SUBMITTED_URL': settings.LINKEDIN_SUBMITTED_URL,
        'LINKEDIN_IMAGE_URL': settings.LINKEDIN_IMAGE_URL,
        'GOOGLE_SINGLE_URL': GOOGLE_SINGLE_URL,
        'FACEBOOK_SINGLE_URL': FACEBOOK_SINGLE_URL,
        'LINKEDIN_SINGLE_URL': LINKEDIN_SINGLE_URL,
    }
    return context_dict[name]
