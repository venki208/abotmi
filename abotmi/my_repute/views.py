# python lib
import ast
import logging

# Django lib
from django.shortcuts import render
from django.http import HttpResponse

# Database models
from datacenter.models import ReputationIndexMetaData

# constatns
from common.constants import MY_REPUTE, RECAPTCHA_KEY

# Local Imports
from common.views import (logme)

# Rest framework imports
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes)
from rest_framework.permissions import AllowAny, IsAuthenticated

logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def index(request, shared_up_id=None):
    '''
    Description: Loading Advisors Reputation index and Navigating to my_repute html
    '''
    user_profile_id = None
    if shared_up_id:
        user_profile_id = shared_up_id
    else:
        user_profile_id = request.user.profile.id
    if user_profile_id:
        title = MY_REPUTE
        is_pincode_present_in_meta = False
        ri_meta = ReputationIndexMetaData.objects.filter(
            user_profile=user_profile_id).first()
        if ri_meta:
            if ri_meta.pincodes:
                try:
                    pincode_arr = ast.literal_eval(ri_meta.pincodes)
                    if pincode_arr:
                        if int(ri_meta.user_profile.pincode) in pincode_arr:
                            is_pincode_present_in_meta = True
                except:
                    pass
        return render(request, 'my_repute/my_repute.html', locals())
    else:
        return HttpResponse("Profile id not found in request")


def demo_repute(request, slug):
    '''
    Description: my_repute - coming_soon html when user login as a guest user
    '''
    social_auth_ses = request.session.get('social_auth_ses', None)
    return render(request, 'my_repute/coming_soon.html', locals())


def my_repute_static(request):
    '''
    Loading My repute static content
    '''
    PAGE_TITLE = 'My Repute page'
    recaptcha_key = RECAPTCHA_KEY
    hide_signup_popup = 1
    logger.info(
        logme("redirected to my repute page", request)
    )
    return render(request, 'my_repute/my_repute_static.html', locals())


def manage_reputation(request):
    '''
    Loading manage repute static content
    '''
    PAGE_TITLE = 'Manage Repute page'
    recaptcha_key = RECAPTCHA_KEY
    hide_signup_popup = 1
    logger.info(
        logme("redirected to build manage page", request)
    )
    return render(request, 'my_repute/manage_reputation.html', locals())


def build_reputation(request):
    '''
    Loading build repute static content
    '''
    PAGE_TITLE = 'Build Repute page'
    recaptcha_key = RECAPTCHA_KEY
    hide_signup_popup = 1
    logger.info(
        logme("redirected to build repute page", request)
    )
    return render(request, 'my_repute/build_reputation.html', locals())


def share_reputation(request):
    '''
    Loading share repute static content
    '''
    PAGE_TITLE = 'Share Repute page'
    recaptcha_key = RECAPTCHA_KEY
    hide_signup_popup = 1
    logger.info(
        logme("redirected to share repute page", request)
    )
    return render(request, 'my_repute/share_reputation.html', locals())
