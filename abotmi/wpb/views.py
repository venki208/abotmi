# python libs
import json
import logging
import requests
from requests.exceptions import Timeout

# django libs
from django.conf import settings
from django.http import HttpResponse
from django.template import RequestContext

# Database imports
from django.contrib.auth.models import User
from datacenter.models import Advisor, UserProfile

# Local Imports
from common.encryption_util import encrypt
from common.views import logme
# wpb libs
from wpb.wpb_api import get_wpb_auth_token

logger = logging.getLogger(__name__)


def launch_wpb_app(request):
    '''
    Description: api/create_user_session is_wpb_user
    '''
    WPB_URL = settings.WPB_URL
    context = RequestContext(request)
    context_dict = {
        'PRODUCT_NAME': settings.PRODUCT_NAME,
        'WPB_URL': settings.WPB_URL
    }
    if request.method == 'POST':
        get_or_create_user_json = get_or_create_user(
            request, request.user.profile, request.user.profile.advisor)
        if request.user.profile.advisor.is_wpb_user:
            try:
                return HttpResponse(get_or_create_user_json['response'])
            except Exception as e:
                logger.error(
                    logme('Unable to launch the wpb. error:{}'.format(e), request)
                )
        else:
            logger.info(
                logme('not a wpb user, access denied', request)
            )
            return HttpResponse('you do not have access to this page')

    if request.method == 'GET':
        logger.info(
            logme('GET request - access forbidden for wpb', request)
        )
        return HttpResponse('you do not have access to this page \
        <a href="/">click here to return home</a>')


def get_or_create_user(request, user_profile, advisor):
    '''
    Description:
        # Obtain the context from the HTTP request.
        # 1) Get WPB TOKEN form settings
        # 2) if WPB TOKEN not found get using get_wpb_auth_token()
        # 3) if user exists show WPB user details and course status
        # 4) if user does not exists show create and course list
    '''
    context = RequestContext(request)
    context_dict = {
        'PRODUCT_NAME': settings.PRODUCT_NAME,
        'WPB_URL': settings.WPB_URL
    }
    course_id = request.POST.get('course_id', None)
    course_name = request.POST.get('course_name', None)
    user_profile = request.user.profile
    user_data = {
        'first_name': user_profile.first_name,
        'middle_name': user_profile.middle_name,
        'last_name': user_profile.last_name,
        'username': request.user.username,
        'address': user_profile.door_no + user_profile.street_name,
        'city': user_profile.city,
        'user_state': user_profile.state,
        'user_country': user_profile.country,
        'dob': user_profile.birthdate,
        'zipcode': user_profile.pincode,
        'mobile_no': user_profile.mobile,
        'company_name': user_profile.company_name,
        'company_website': user_profile.company_website,
        'course_name': course_name,
        'course_id': course_id,
        'signup_platform': 'abotmi',
        'password': encrypt(request.user.password)

    }
    logger.debug('user_data')
    logger.debug(user_data)
    if not settings.WPB_TOKEN:
        auth_status = get_wpb_auth_token()
        logger.debug('auth_status ')
        logger.debug(auth_status)
    token = settings.WPB_TOKEN
    header = {'Authorization': 'JWT %s' % token}
    token_obj = None
    url = settings.WPB_URL + '/api/user/register_user_by_spoc/'
    req = requests.post(url, headers=header, data=user_data)
    logger.debug('req')
    logger.debug(req)
    json_res = req.content.encode('UTF-8')
    token_obj = json.loads(json_res)
    logger.debug('token_obj')
    logger.debug(token_obj['status'])
    if token_obj['status']:
        advisor.is_wpb_user = True
        advisor.save()
    logger.debug(req.status_code)
    logger.debug(req.content)
    logger.info(
        logme('advisor joined stream', request)
    )
    return token_obj


def get_all_wpb_course(request, user):
    '''
    Description: Get all available course for this user
    '''
    stream_course_list = None
    token_obj = None
    if not settings.WPB_TOKEN:
        auth_status = get_wpb_auth_token()
        logger.debug('auth_status')
        logger.debug(auth_status)
    try:
        url = settings.WPB_URL+'/api/user/get_all_courses/'
        token = settings.WPB_TOKEN
        header = {'Authorization': 'JWT %s' % (token)}
        data = {'wpb_user': user.username}
        '''
        Getting all courses from wpb.
        Request should complete with in 5sec
        '''
        req = requests.post(
            url,
            headers=header,
            data=data,
            timeout=5
        )
        json_res = req.content.encode('UTF-8')
        token_obj = json.loads(json_res)
        logger.info(
            logme('Returned all wpb course list', request)
        )
    except Timeout as to:
        logger.error(
            logme(
                'Timeout request from wpb request/response is not completed in 5sec',
                request
            )
        )
    except Exception as e:
        logger.error(
            logme(
                'Unable to load the all courses from wpb. error:{}'.format(e),
                request
            )
        )
    return token_obj
