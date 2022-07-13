# Python lib
import datetime
import json
import hashlib
import logging
import time
import random
import urllib
import requests

# Django Libs
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache
from django.conf import settings
from django.template import RequestContext, loader
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt

# Database Models
from datacenter.models import (
    UserProfile, Advisor, MeetUpEvent, EmailVerification, SocialMedia, Testimonial
)

# Local imports
from common.constants import (
    RECAPTCHA_KEY, COMPANY_USER, REGION_DEFAULT, OTP_TO_EMAIL, OTP_TO_MOBILE, REGION_IN,
    SIGNUP_OTP, MEMBER_SIGNUP_WITH_EMAIL, LN_CALLBACK_URL, LN_AUTH_URL, LN_TOKEN_URL,
    LN_GET_EMAIL_URL, LN_GET_PROFILE_URL
)
from common.notification.constants import(
    SIGNUP_TEMPLATE, EMAIL_VERF_TEMPLATE, LEARN_ABOUT_MY_IDENTITY, LEARN_ABOUT_MY_HUB,
    LEARN_ABOUT_COURSE
)
from common.views import (
    referral_points, get_all_advisors_count, logme, get_notification_services_json,
    get_ipinfo, Otp, get_ip_region
)
from common.linkedin_api import LinkiedinOAuth
from common.utils import UtilFunctions
from common.notification.views import NotificationFunctions
from login.common_views import LoginCommonFunctions
# from login.decorators import active_and_login_required, active_and_advisor
from reputation_index.common_functions import advisor_scoring_fb, advisor_scoring_linkedin
from signup.djmail import send_mandrill_email

# Constatns
from common.api_constants import (
    GOOGLE_SINGLE_URL, FACEBOOK_SINGLE_URL, LINKEDIN_SINGLE_URL
)

logger = logging.getLogger(__name__)


def index(request):
    '''
    Navigating to Login Page with Advisor Check count
    '''
    if request.method == 'GET':
        title = 'Log In'
        recaptcha_key = RECAPTCHA_KEY
        user_agent_country = get_ip_region(request)
        # getting linkedin data from session
        ln_email = request.session.get('ln_email', '')
        ln_f_name = request.session.get('ln_f_name', '')
        ln_l_name = request.session.get('ln_l_name', '')
        ln_user_selected_role = request.session.get('user_selected_role', 'advisor')
        ln_next_url = request.session.get('ln_next_url', None)
        # Getting advisor check serach data from linkedin session
        ad_chk_name = request.session.get('ad_chk_name', '')
        ad_chk_last_name = request.session.get('ad_chk_last_name', '')
        ad_chk_email = request.session.get('ad_chk_email', '')
        ad_chk_mob = request.session.get('ad_chk_mob', '')
        ad_chk_loc = request.session.get('ad_chk_loc', '')
        ad_chk_country = request.session.get('ad_chk_country', '')
        ad_chk_reg = request.session.get('ad_chk_reg', '')
        # deleteing the linkedin session data
        if 'ln_email' in request.session:
            del request.session['ln_email']
        if 'ln_f_name' in request.session:
            del request.session['ln_f_name']
        if 'ln_l_name' in request.session:
            del request.session['ln_l_name']
        if 'ln_next_url' in request.session:
            del request.session['ln_next_url']
        
        if request.user.is_authenticated():
            logger.info(logme('advisor successfully redirected to login', request))
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        else:
            LOGIN_URL = settings.LOGIN_URL
            FACEBOOK_API = settings.FACEBOOK_API
            next_url = ln_next_url if ln_next_url else request.GET.get(
                'next', settings.LOGIN_REDIRECT_URL)
            testimonals = Testimonial.objects.all()
            logger.info(logme('redirected to login page', request))
            return render(request, 'login.html', locals())


@login_required()
def user_logout(request):
    '''
    Function for Logging out the User
    '''
    if request.method == 'POST':
        # Since we know the user is logged in, we can now just log them out.
        if request.user.is_authenticated():
            if request.session.get('user_selected_role', None):
                del request.session['user_selected_role']
            if request.session.get('social_auth_ses', None):
                del request.session['social_auth_ses']
            logger.info(
                logme('advisor clicked logout', request)
            )
        logout(request)
        # Take the user back to the homepage.
        return HttpResponse('success')
    if request.method == "GET":
        logger.info(
            logme('GET request- access forbidden to logout', request)
        )
        return HttpResponse('Access forbidden')


def social_media_login(request):
    '''
    Description: Signup/Signin with Social media
    '''
    if request.method == 'POST':
        user_password = get_random_string(length=8)
        source_media = request.POST.get('source_media', None)
        user_selected_role = request.POST.get('user_selected_role', 'advisor')
        exist_user = 'user_exist'
        social_signup = LoginCommonFunctions({'request': request})
        data = {
            'password': user_password,
            'source_media': source_media
        }
        s_signup = social_signup.get_or_create_social_media_advisor(object=data)
        created = s_signup.get('is_created', None)
        user = s_signup.get('user', None)
        status = s_signup.get('status', None)
        user_profile = s_signup.get('user_profile', None)
        user_status = user_profile.status

        # IP recongnization
        ip_region = get_ip_region(request)

        nf = NotificationFunctions(request=request, receive=user_profile)

        '''
        Updating mobile and emila verification status
        '''
        # Getting email, mobile verification status from session
        email_verified = request.session.get('email_verified_status', None)
        mobile_verified = request.session.get('mobile_verified_status', None)
        # deleting the session key
        if 'email_verified_status' in request.session:
            del request.session['email_verified_status']
        if 'mobile_verified_status' in request.session:
            del request.session['mobile_verified_status']
        # Updating email, mobile verification status
        if ip_region == 'IN':
            user_status.mobile_verified = mobile_verified
        user_status.email_verified = email_verified

        if not status == 204 and status:
            if source_media == "facebook":
                access_token = request.POST.get("token", None)
                email = request.POST.get("email", None)
                if access_token and email:
                    try:
                        response = advisor_scoring_fb(email, access_token)
                        logger.info(
                            logme("Scoring api response "+str(response), request)
                        )
                    except Exception as e:
                        logger.info(
                            logme("Scoring api exception occered "+str(e), request)
                        )
            if source_media == "linkedin":
                headLine = request.POST.get("headline", None)
                summary = request.POST.get("summary", None)
                email = request.POST.get("email", None)
                if headLine and email and summary:
                    try:
                        response = advisor_scoring_linkedin(email, headLine, summary)
                        logger.info(
                            logme("Scoring api response "+str(response), request)
                        )
                    except Exception as e:
                        logger.info(
                            logme("Scoring api exception occered "+str(e), request)
                        )
            if created:
                exist_user = 'new_user'
                user_status.save()
                nf.save_notification(
                    notification_type=SIGNUP_TEMPLATE,
                )
            if user:
                if user.is_active and user.is_staff:
                    login(request, user)
                    # Setting user selected role in session
                    request.session['user_selected_role'] = user_selected_role
                    # setting advisor check search datain session for inverstor
                    if request.session['user_selected_role'] == 'investor':
                        ad_chk_name = request.POST.get('ad_chk_name', None)
                        ad_chk_email = request.POST.get('ad_chk_email', None)
                        ad_chk_mob = request.POST.get('ad_chk_mob', None)
                        ad_chk_loc = request.POST.get('ad_chk_loc', None)
                        ad_chk_country = request.POST.get('ad_chk_country', None)
                        if ad_chk_name:
                            request.session['ad_chk_name'] = ad_chk_name
                        if ad_chk_email:
                            request.session['ad_chk_email'] = ad_chk_email
                        if ad_chk_mob:
                            request.session['ad_chk_mob'] = ad_chk_mob
                        if ad_chk_loc:
                            request.session['ad_chk_loc'] = ad_chk_loc
                        if ad_chk_country:
                            request.session['ad_chk_country'] = ad_chk_country
                        if not user_profile.is_member:
                            user_profile.is_member = True
                            user_profile.save()
                    res = {
                        'log_usr_type': exist_user,
                        'account_type': 'active',
                        'user_selected_role': user_selected_role
                    }
                    if user_profile.is_company:
                        logger.info(
                            logme("user is company, logged in with linkedin",request)
                        )
                        res = {
                            'log_usr_type': COMPANY_USER,
                            'account_type': 'active'
                        }
                    else:
                        res = {
                            'log_usr_type': exist_user,
                            'account_type': 'active',
                            'user_selected_role': user_selected_role
                        }
                    return JsonResponse(res)
                else:
                    return JsonResponse({'account_type': 'deactivated'})
            else:
                return JsonResponse({'account_type': 'deactivated'})
        else:
            return JsonResponse({'account_type': 'deactivated'})


def investor_social_media_login(request):
    '''
    Description: Signup/Signin with Social media
    '''
    if request.method == 'POST':
        user_password = get_random_string(length=8)
        source_media = request.POST.get('source_media', None)
        exist_user = 'user_exist'
        social_auth = request.POST.get('social_auth', None)
        ad_chk_name = request.POST.get('ad_chk_name', None)
        ad_chk_email = request.POST.get('ad_chk_email', None)
        ad_chk_mob = request.POST.get('ad_chk_mob', None)
        ad_chk_loc = request.POST.get('ad_chk_loc', None)
        ad_chk_country = request.POST.get('ad_chk_country', None)
        if ad_chk_name:request.session['ad_chk_name'] = ad_chk_name
        if ad_chk_email:request.session['ad_chk_email'] = ad_chk_email
        if ad_chk_mob:request.session['ad_chk_mob'] = ad_chk_mob
        if ad_chk_loc:request.session['ad_chk_loc'] = ad_chk_loc
        if ad_chk_country:request.session['ad_chk_country'] = ad_chk_country
        social_signup = LoginCommonFunctions({'request':request})
        data={
            'password': user_password,
            'source_media': source_media
        }
        s_signup = social_signup.get_or_create_social_media_advisor(object = data)
        created = s_signup.get('is_created', None)
        user = s_signup.get('user', None)
        status = s_signup.get('status', None)
        user_profile = s_signup.get('user_profile', None)
        # IP recongnization
        ip_details = get_ipinfo(request)
        user_agent_country = ip_details.get(
            "country", REGION_DEFAULT)
        if not status == 204 and status:
            if created:
                exist_user = 'new_user'
            if user:
                if user.is_active and user.is_staff:
                    if not request.user.is_authenticated():
                        otp = Otp(
                            request,
                            user_profile_id=user_profile.id,
                            name=user_profile.first_name.split(" ")[0]
                        )
                        otp.send_otp(
                            mobile=user_profile.mobile,
                            email=user_profile.email,
                            otp_type=OTP_TO_EMAIL
                        )
                        del(otp)
                    if request.POST.get('inv_chk_login', None):
                        request.session['inv_chk_login'] = request.POST.get('inv_chk_login', None)
                    request.session['social_auth_ses'] = "True"
                    response = {
                        'exist_user': exist_user,
                        'profile_id' : user_profile.id,
                        'social_auth_ses': request.session['social_auth_ses'],
                        'inv_chk_login': request.session.get('inv_chk_login', None),
                        'is_authenticated': request.user.is_authenticated()
                    }
                    save_social_media_info(request, user_profile)
                    return JsonResponse(response)
                else:
                    return HttpResponse('deactivated')
            else:
                return HttpResponse('deactivated')
        else:
            return HttpResponse('Invalid Login2')


def save_social_media_info(request,user_profile=None):
    '''
    Saving social media information
    '''
    ref_link = request.POST.get('ref_link', None)
    email = request.POST.get('email', None)
    source_media = request.POST.get('source_media', None)
    first_name = request.POST.get('first_name', None)
    last_name = request.POST.get('last_name', None)
    birthday = request.POST.get('birthday', None)
    gender = request.POST.get('gender', None)
    mobile = request.POST.get('mobile', None)
    user_type = request.POST.get('user_type', None)
    user_profile = user_profile if user_profile else request.user.profile
    social_media, created = SocialMedia.objects.get_or_create(
        user_profile = user_profile, sm_source=source_media)
    if social_media:
        social_media.sm_source = source_media
        social_media.title = ''
        social_media.email_id = email
        social_media.first_name = first_name
        social_media.middle_name = last_name
        social_media.last_name = last_name
        social_media.gender = gender
        social_media.mobile = mobile
        social_media.user_type = user_type
        social_media.save()
    return True


def sm_google_login(request):
    '''
    Navigatin to google_login_view html
    '''
    context_dict = {
        'PRODUCT_NAME' : settings.PRODUCT_NAME,
        'GOOGLE_CLIENTID': settings.GOOGLE_CLIENTID,
        'GOOGLE_REDIRECT': settings.GOOGLE_REDIRECT,
    }
    logger.info(
        logme("redirected to google login view page",request)
    )
    return render_to_response(
        'login/google_login_view.html',
        context_dict,
        context_instance=RequestContext(request)
    )


def sm_facebook_login(request):
    ''' Navigating to  facebook_login_view html'''
    context_dict = {
        'FACEBOOK_API': settings.FACEBOOK_API,
        'GOOGLE_REDIRECT': settings.GOOGLE_REDIRECT,
    }
    logger.info(
        logme("redirected to facebook login view",request)
    )
    return render_to_response(
        'login/facebook_login_view.html',
        context_dict,
        context_instance=RequestContext(request)
    )


def sm_linkedin_login(request):
    ''' Navigating to linkedin_login_view html '''
    context_dict = {
        'LINKEDIN_API': settings.LINKEDIN_API,
        'GOOGLE_REDIRECT': settings.GOOGLE_REDIRECT,
    }
    logger.info(
        logme("redirected to linkedin login view",request)
    )
    return render_to_response(
        'login/linkedin_login_view.html',
        context_dict,
        context_instance=RequestContext(request)
    )


def ajax_login(request):
    '''
    Use to login through ajax
    '''
    if request.method == 'POST':
        username = request.POST['username'].strip()
        password = request.POST['password']
        user_selected_role = request.POST.get('user_selected_role', 'advisor')
        user = authenticate(username=username, password=password)
        login_response = {
            'status': 'false',
            'messages': 'invalid username / password',
            'next': settings.LOGIN_URL
        }
        if user:
            if user.is_active and user.is_staff:
                user_profile = user.profile
                user_profile.last_login = user.last_login
                if user_profile.is_advisor:
                    advisor = user_profile.advisor
                user_profile.save()

                if user_profile.is_advisor or user_profile.is_admin or user.is_superuser:
                    login(request, user)
                    request.session['user_selected_role'] = user_selected_role
                    if request.POST.get('next', None):
                        login_response = {
                            'status': 'true',
                            'messages': 'success',
                            'next': request.POST["next"]
                        }
                        logger.info(
                            logme("user successfully logged in through ajax modals, can be advisor, admin or superuser",request)
                        )
                    else:
                        login_response = {
                            'status': 'true',
                            'messages': 'success',
                            'next': settings.LOGIN_REDIRECT_URL
                        }
                        logger.info(
                            logme("User Successfully logged in",request)
                        )
                elif user_profile.is_company:
                    login(request, user)
                    login_response = {
                        'status': 'true',
                        'messages': 'success',
                        'next': '/company/my_company_track/'
                    }
                    logger.info(
                        logme("company user successfully logged in through ajax modals",request)
                    )
                elif user_profile.is_crisil_admin:
                    login(request, user)
                    login_response = {
                        'status':'true',
                        'messages': 'crisil admin',
                        'next' : '/nfadmin/crisil_admin_panel/'
                    }
                    logger.info(
                        logme("crisil admin user successfully logged in through ajax modals",request)
                    )
                elif user_profile.is_member:
                    login(request, user)
                    login_response = {
                        'status': 'true',
                        'messages': 'success',
                        'next': '/member/'
                    }
                    logger.info(
                        logme("membver user successfully logged in ",request)
                    )
                else:
                    login_response = {
                        'status': 'false',
                        'messages': 'invalid username / password',
                        'next': settings.LOGIN_URL
                    }
                    logger.info(
                        logme("user tried to login through ajax models,not advisor, superuser, crisil admin, admin, company",request)
                    )
            else:
                login_response = {
                    'status': 'false',
                    'messages': 'invalid username / password',
                    'next': settings.LOGIN_URL
                }
                logger.info(
                    logme("user tried to login through ajax models, user not active or not staff",request)
                )
        else:
            login_response = {
                'status': 'false',
                'messages': 'invalid username / password',
                'next': settings.LOGIN_URL
            }
            logger.info(
                logme("user tried to login through ajax models, invalid username or password",request)
            )
        return JsonResponse(login_response)

    if request.method == 'GET':
        logger.info(
            logme("GET request-access forbidden for login using ajax models",request)
        )
        return HttpResponseRedirect(settings.LOGIN_URL)


def email_signup(request):
    '''
        Create New user by direct signup
    '''
    if request.method == 'POST':
        direct_signup = LoginCommonFunctions({'request': request})
        password = request.POST.get('password', None)
        randome_password = UtilFunctions.generate_randome_password()
        data = {
            'password': password if password else randome_password
        }
        is_created = direct_signup.createuser(
            object=data
        )
        status_code = is_created.get('status')
        user = is_created.get('user', None)
        user_status = is_created.get('user_status', None)
        user_profile = is_created.get('user_profile', None)
        user_selected_role = request.POST.get('user_selected_role', 'advisor')

        # Notification class object
        nf = NotificationFunctions(request=request, receive=user_profile)

        # Advisor check search request data
        ad_chk_name = request.POST.get('ad_chk_name', None)
        ad_chk_last_name = request.POST.get('ad_chk_last_name', None)
        ad_chk_email = request.POST.get('ad_chk_email', None)
        ad_chk_mob = request.POST.get('ad_chk_mob', None)
        ad_chk_loc = request.POST.get('ad_chk_loc', None)
        ad_chk_country = request.POST.get('ad_chk_country', None)
        ad_chk_reg = request.POST.get('ad_chk_reg', None)

        # IP recognization
        ip_region = get_ip_region(request)

        # Getting email, mobile verification status from session
        email_verified = request.session.get('email_verified_status', False)
        mobile_verified = request.session.get('mobile_verified_status', False)

        # deleting the session key
        if 'email_verified_status' in request.session:
            del request.session['email_verified_status']
        if 'mobile_verified_status' in request.session:
            del request.session['mobile_verified_status']

        # Updating email, mobile verification status
        if ip_region == 'IN':
            user_status.mobile_verified = mobile_verified
        user_status.email_verified = email_verified

        # setting user source according to selected role
        if user_selected_role == 'advisor':
            if status_code == 201:
                user_profile.source_media = "signup_with_email"
            user_profile.is_advisor = True
        else:
            if status_code == 201:
                user_profile.source_media = "member_signup_with_email"
            user_profile.is_member = True
        if status_code == 201:
            nf.save_notification(
                notification_type=SIGNUP_TEMPLATE,
            )
        user_profile.save()
        user_status.save()
        del(nf)
        del(direct_signup)

        # Making Login for user
        if ((user_selected_role == 'advisor' and status_code == 201) or
                (user_selected_role == 'investor')):
            login(request, user)
            request.session['user_selected_role'] = user_selected_role
            # setting advisor check search request data in session
            if ad_chk_name:
                request.session['ad_chk_name'] = ad_chk_name
            if ad_chk_email:
                request.session['ad_chk_email'] = ad_chk_email
            if ad_chk_mob:
                request.session['ad_chk_mob'] = ad_chk_mob
            if ad_chk_loc:
                request.session['ad_chk_loc'] = ad_chk_loc
            if ad_chk_country:
                request.session['ad_chk_country'] = ad_chk_country
            if ad_chk_reg:
                request.session['ad_chk_reg'] = ad_chk_reg

        # Html response data
        res_data = {}
        res_data['user_selected_role'] = user_selected_role
        res_data['advisor'] = user_profile.is_advisor
        res_data['member'] = user_profile.is_member
        res_data['status_code'] = status_code
        if user_selected_role == 'advisor' and status_code == 201:
            return JsonResponse(res_data, status=status_code)
        elif user_selected_role == 'investor' and status_code is not 500:
            return JsonResponse(res_data, status=status_code)
        else:
            return JsonResponse(status=500)
    else:
        logger.info(
            logme("GET request- access forbidden, direct sign up failed", request)
        )
        return HttpResponse(status=405)


def resend_otps(request):
    '''
    Resending the OTP to Email/Mobile
    '''
    if request.method == 'POST':
        user = request.user
        user_profile_id = request.POST.get('profile_id', None)
        mode = request.POST.get('mode', None)
        user_profile = UserProfile.objects.filter(
            id=user_profile_id).select_related('user').first()
        ip_region = request.session['ip_info']
        user_agent_country = ip_region.get(
                "country", REGION_DEFAULT)
        otp = Otp(
            request,
            user_profile_id=user_profile.id,
            name=user_profile.first_name.split(" ")[0]
        )
        if mode == "mobile":
            otp.send_otp(
                mobile=user_profile.mobile,
                email=user_profile.email,
                otp_type=OTP_TO_MOBILE
            )
        elif mode == "both" and user_agent_country == REGION_IN:
            otp.send_otp(
                mobile=user_profile.mobile,
                email=user_profile.email,
                otp_type=OTP_TO_MOBILE
            )
            otp.send_otp(
                mobile=user_profile.mobile,
                email=user_profile.email,
                otp_type=OTP_TO_EMAIL
            )
        else:
            otp.send_otp(
                mobile=user_profile.mobile,
                email=user_profile.email,
                otp_type=OTP_TO_EMAIL
            )
            del(otp)
        logger.info(
            logme("The OTP has been sent.", request)
        )
        return JsonResponse({'status': 200})
    else:
        logger.error(
            logme("The OTP sending has been failed.", request)
        )
        return JsonResponse({'status': 500})


def resend_email_mobile_otps(request):
    '''
    Resending the OTP to Email/Mobile
    '''
    if request.method == 'POST':
        email = request.POST.get('email', None)
        mobile = request.POST.get('mobile', None)
        mode = request.POST.get('mode', None)
        name = request.POST.get('name', None)
        signup_otp = request.POST.get('signup_otp', None)
        ip_region = request.session['ip_info']
        user_agent_country = ip_region.get(
                "country", REGION_DEFAULT)
        otp = Otp(
            request
        )
        if mode == "mobile":
            otp.send_resend_signup_otp(
                mobile=mobile,
                email=email,
                name=name,
                otp_type='signup_otp'
            )
        else:
            otp.send_resend_signup_otp(
                mobile=mobile,
                email=email,
                name=name,
                otp_type='signup_otp'
            )
        del(otp)
        logger.info(
            logme("The OTP has been sent.", request)
        )
        return JsonResponse({'status': 200, 'mode': mode})
    else:
        logger.error(
            logme("The OTP sending has been failed.", request)
        )
        return JsonResponse({'status': 500})


def activate_member_activation_link(request):
    '''
    This function is used in set password for new user.
    '''
    if request.method == 'GET':
        try:
            verification = EmailVerification.objects.get(activation_key=request.GET['ack'])
            verification.delete()
        except:
            logger.info(
                logme("activation mail may be wrong or expired",request)
            )
            return HttpResponse("Activation link may be wrong or expired")
        user_auth_obj = User.objects.get(username=verification.user_profile.user.username)
        request.session['username'] = user_auth_obj
        logger.info(
            logme("email activation link verified, account activated", request)
        )
        return render(request, 'signup/recheck.html', locals())
    if request.method == 'POST':
        user = request.session.get('username')   # ====Receiving session for using the user details in Post
        user_auth_obj = User.objects.get(username=user)
        json_data = json.loads(request.body)
        user_auth_obj.set_password(json_data['password'])
        user_auth_obj.save()
        logger.info(
            logme("password set successfully",request)
        )
        return HttpResponse(settings.LOGIN_REDIRECT_URL)


def validate_otp(request):
    '''
    Validating the Emial/Mobile OTP
    '''
    if request.method == 'POST':
        signup_otp = request.POST.get('signup_otp', None)
        email_otp = request.POST.get('email_otp', None)
        mobile_otp = request.POST.get('mobile_otp', None)
        first_name = request.POST.get('first_name', None)
        email = request.POST.get('email', None)
        mobile = request.POST.get('mobile', None)
        otp_obj = Otp(request)
        user_agent_country = get_ip_region(request)
        email_verified_status = None
        mobile_verified_status = None
        if email_otp:
            is_email_verified = otp_obj.validate_otp(
                otp=email_otp,
                email=email,
                otp_type=SIGNUP_OTP,
            )
            email_verified_status = is_email_verified
            request.session['email_verified_status'] = is_email_verified
        if mobile_otp:
            is_mobile_verified = otp_obj.validate_otp(
                otp=mobile_otp,
                mobile=mobile,
                otp_type=SIGNUP_OTP,
            )
            mobile_verified_status = is_mobile_verified
            request.session['mobile_verified_status'] = is_mobile_verified
        return JsonResponse({
            'email_verf_stat': email_verified_status,
            'mob_verf_stat': mobile_verified_status
        }, status=200)
    else:
        return HttpResponse('Access forbidden', status=405)


def verify_otp_and_login(request):
    '''
    Verifying the Email/Mobile/Both OTP and making user log in
    '''
    if request.method == 'POST':
        user_profile_id = request.POST.get('profile_id', None)
        email_otp = request.POST.get('email_otp', None)
        mobile_otp = request.POST.get('mobile_otp', None)
        user_profile = UserProfile.objects.filter(
            id=user_profile_id).select_related('user').first()
        if user_profile:
            user = user_profile.user
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            user_status = user_profile.status
            otp_obj = Otp(request, user_profile_id, user_profile.first_name)
            if email_otp:
                is_email_verified = otp_obj.validate_otp(
                    otp=email_otp,
                    email=user_profile.email,
                    otp_type=OTP_TO_EMAIL
                )
                if is_email_verified:
                    user_status.email_verified = True
            if mobile_otp:
                is_mobile_verified = otp_obj.validate_otp(
                    otp=mobile_otp,
                    mobile=user_profile.mobile,
                )
                if is_mobile_verified:
                    user_status.mobile_verified = True
            user_status.save()
            user.save()
            del(otp_obj)
            ip_details = get_ipinfo(request)
            ip_region = ip_details.get("country", REGION_DEFAULT)
            if user_profile.is_member:
                # member social media sign up
                if (not user_profile.source_media == MEMBER_SIGNUP_WITH_EMAIL
                    and user_status.email_verified):
                    if not request.user.is_authenticated():
                        login(request, user)
                # member sign up to see the advisor's profile
                if user_profile.source_media == MEMBER_SIGNUP_WITH_EMAIL:
                    # Indian user
                    if (user_status.email_verified and user_status.mobile_verified
                            and ip_region == REGION_IN):
                                if not request.user.is_authenticated():
                                    login(request, user)
                    # Non Indian user
                    elif (user_status.email_verified and ip_region != REGION_IN):
                                if not request.user.is_authenticated():
                                    login(request, user)
            if user_profile.is_advisor:
                # Indian advisor direct sign up
                if ip_region == REGION_IN:
                    if user_status.email_verified and user_status.mobile_verified:
                        if not request.user.is_authenticated():
                            login(request, user)
                else:
                    if user_status.email_verified:
                        if not request.user.is_authenticated():
                            login(request, user)
            return JsonResponse({
                    'is_mob_verf': user_status.mobile_verified,
                    'is_email_verf': user_status.email_verified,
                    'social_auth_ses': request.session.get('social_auth_ses', None)
                }, status=200)
        else:
            return HttpResponse(status=204)
    else:
        return HttpResponse(status=405)


def get_advisor_check_total_enrolled_count(request):
    '''
    Description: function for getting country based Advisor check count
    '''
    if request.method == 'POST':
        country_type = request.POST.get('country_name', None)
        if country_type:
            advisor_chk_data = get_all_advisors_count(
                request, region=country_type)
            if advisor_chk_data:
                request.session['country_type'] = country_type
                enrolled_advisors = advisor_chk_data[0].get('Advisor Enrolled', None)
                if len(str(enrolled_advisors)) % 2 == 0:
                    enrolled_advisors = str(enrolled_advisors)
                else:
                    enrolled_advisors = "0" + str(enrolled_advisors)
                advisor_chk_enrolled_count = [
                    enrolled_advisors[i - 2 if i - 2 >= 0 else 0:i]
                    for i in range(len(str(enrolled_advisors)), 0, -2)]
            return render(request, 'home/enrolled_advisors_count.html', locals())


def set_user_role(request):
    '''
    Setting selected role in request
    '''
    user_selected_role = request.POST.get('user_role', None)
    if user_selected_role:
        request.session['user_selected_role'] = user_selected_role
        return HttpResponse('success')
    else:
        return HttpResponse('failed')


def send_signup_otp(request):
    '''
    checking the USER AGENT COUNTRY and sending OTP for EMAIL or MOBILE
    '''
    if request.method == 'POST':    
        email = request.POST.get('email', None)
        mobile = request.POST.get('mobile', None)
        first_name = request.POST.get('first_name', None)
        otp_obj = Otp(request)
        user_agent_country = get_ip_region(request)
        if user_agent_country == "IN":
            mobile_otp = otp_obj.send_signup_otp(
                mobile=mobile,
                name=first_name,
                otp_type=SIGNUP_OTP
            )
        email_otp = otp_obj.send_signup_otp(
            email=email,
            name=first_name,
            otp_type=SIGNUP_OTP
        )
        response = {
            'status_text': 'success',
            'status_code': 200,
            'ip_country': user_agent_country
        }
        del(otp_obj)
        return JsonResponse(response, status=200)
    else:
        return JsonResponse(status=405)


@csrf_exempt
def linkedin(request):
    '''
    Navigating User to linkedin page (OAuth Concept) to get the user details
    '''
    user_selected_role = request.GET.get('user_selected_role', 'advisor')
    # Advisor check search request data
    ad_chk_name = request.GET.get('ad_chk_name', None)
    ad_chk_last_name = request.GET.get('ad_chk_last_name', None)
    ad_chk_email = request.GET.get('ad_chk_email', None)
    ad_chk_mob = request.GET.get('ad_chk_mob', None)
    ad_chk_loc = request.GET.get('ad_chk_loc', None)
    ad_chk_country = request.GET.get('ad_chk_country', None)
    ad_chk_reg = request.GET.get('ad_chk_reg', None)
    next_url = request.GET.get('next_url', '/home/')

    ln_obj = LinkiedinOAuth()
    ln_url = ln_obj.get_autherization_url()
    del(ln_obj)
    # Settings user selected role in to session
    request.session['user_selected_role'] = user_selected_role
    # setting advisor check search request data in session
    if ad_chk_name:
        request.session['ad_chk_name'] = ad_chk_name
    if ad_chk_email:
        request.session['ad_chk_email'] = ad_chk_email
    if ad_chk_mob:
        request.session['ad_chk_mob'] = ad_chk_mob
    if ad_chk_loc:
        request.session['ad_chk_loc'] = ad_chk_loc
    if ad_chk_country:
        request.session['ad_chk_country'] = ad_chk_country
    if ad_chk_reg:
        request.session['ad_chk_reg'] = ad_chk_reg
    if next_url:
        request.session['ln_next_url'] = next_url
    logger.info(
        logme('Redirecting to Linkedin to get the linkedin details of user', request)
    )
    return HttpResponseRedirect(ln_url)


@csrf_exempt
def callback(request):
    '''
    Callback url from linkedin.
    After user gave permissions in linkedin, it will redirect user to this function with
    authorization code and state details.
    '''
    ln_obj = LinkiedinOAuth()
    token = ln_obj.get_auth_token(request)
    if token:
        # Getting Email from Linkedin
        email = ln_obj.get_email()
        if email:
            # Setting Email in session
            request.session['ln_email'] = email
            # Getting profile data from linkedin
            profile = ln_obj.get_profile()
            first_name = profile['first_name']
            last_name = profile['last_name']
            if first_name and last_name:
                # settings first_name & last_name in sesson
                request.session['ln_f_name'] = first_name
                request.session['ln_l_name'] = last_name
            else:
                request.session['ln_res'] = 'ln_error'
        else:
            request.session['ln_res'] = 'ln_error'
    else:
        request.session['ln_res'] = 'ln_error'
    del(ln_obj)
    return redirect('/login/')
