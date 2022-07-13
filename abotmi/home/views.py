import os
import base64
import datetime
import json
import logging
import random
import requests
import uuid

# Django Libs
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache
from django.db.models import Sum, Avg, Q
from django.http import HttpResponseRedirect, HttpResponse, Http404, JsonResponse
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext, loader
from django.utils.crypto import get_random_string

# Database Models
from datacenter.models import (
    UserProfile, Member, UserReferral, AdvisorRating,
    Advisor, UploadDocuments, CompanyAdvisorMapping,
    AffiliatedCompany, UserStatus, Country, ReferFriend, Notification,
    Testimonial
)

# Local Imports
from .serializers import NotificationListSerializer
from common import constants
from common.views import (
    get_all_advisors_count, logme, get_binary_image,
    get_notification_services_json, get_ipinfo)
from common.notification.views import NotificationFunctions
from blog.views import create_word_press_user
from login.decorators import check_role_and_redirect
from login.forms import UserProfileForm, MemberForm
from signup.djmail import (
    send_mandrill_email, send_mandrill_email_with_attachement,
    send_mandrill_email_admin)

# Constatns
from common.api_constants import (
    GOOGLE_SINGLE_URL, FACEBOOK_SINGLE_URL, LINKEDIN_SINGLE_URL
)

# Wordpress
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, comments, posts
from wordpress_xmlrpc.methods.posts import NewPost
from wordpress_xmlrpc.base import *
from wordpress_xmlrpc.wordpress import WordPressComment

# REST Framework imports
from rest_framework_jwt.settings import api_settings
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

logger = logging.getLogger(__name__)


@login_required()
@check_role_and_redirect
def index(request):
    '''
    Rendering Home Page
    '''
    title = 'Home'
    GOOGLE_CLIENTID = settings.GOOGLE_CLIENTID
    GOOGLE_REDIRECT = settings.GOOGLE_REDIRECT
    GOOGLE_SINGLE_URL = GOOGLE_SINGLE_URL
    recaptcha_key = constants.RECAPTCHA_KEY
    new_user = False
    if 'new_google_user' in request.session:
        if request.session['new_google_user']:
            new_user = True
            del request.session['new_google_user']

    user_profile_obj = UserProfile.objects.get(user=request.user)
    if not user_profile_obj.registration_id:
        while(True):
            num = uuid.uuid4().hex[:10]
            if not UserProfile.objects.filter(registration_id=num):
                user_profile_obj.registration_id = num
                user_profile_obj.save()
                break
            else:
                continue
    '''
        creating Word press user and store word press user id in the advisor table
    '''
    if not request.user.is_superuser and user_profile_obj.is_advisor:
        icore_wp_user_id = create_word_press_user(request)
        if icore_wp_user_id:
            advisor_details = Advisor.objects.get(user_profile=user_profile_obj)
            advisor_details.wordpress_user_id = icore_wp_user_id
            advisor_details.save()
            logger.info(
                logme("created word press user & stored wordpress userid=%s in the \
                    advisor table" % (str(icore_wp_user_id)), request)
            )
    country_list = Country.objects.all().values('name')
    request.session['login_or_signup'] = 1
    # -----------------------
    # REGION_IN ADVISORS
    # -----------------------
    advisor_type_ca_count = 0
    advisor_type_sebi_count = 0
    advisor_type_irda_count = 0
    advisor_type_amfi_count = 0
    advisor_type_bse_count = 0
    advisor_type_other = 0
    total_advisor_count = 0
    # -----------------------
    advisor_check_data = cache.get('advisor_data')
    ip_details = get_ipinfo(request)
    ip_region = ip_details.get("country", constants.REGION_DEFAULT)
    if not advisor_check_data:
        advisor_check_data = get_all_advisors_count(
            request, region=ip_region)
        # 60 mins * 60 secs * 24 hrs = 86400
        cache.set('advisor_data', advisor_check_data, 86400)
        logger.info(logme('advisor check data accessed', request))
    if advisor_check_data:
        advisor_check_data = advisor_check_data[0].get('Advisor Enrolled', None)
        if advisor_check_data:
            if len(str(advisor_check_data)) % 2 == 0:
                advisor_check_data = str(advisor_check_data)
            else:
                advisor_check_data = "0"+str(advisor_check_data)
            advisor_check_data = [advisor_check_data[i - 2 if i - 2 >= 0 else 0:i]
                                  for i in range(len(str(advisor_check_data)), 0, -2)]
        advisor_check_data_list = advisor_check_data
        column_size = None
        user_agent_country = ip_region
    logger.info(
        logme('redirecting to upwrdz home page', request)
    )
    return render(request, 'index_base.html', locals())


@login_required()
def user_logout(request):
    '''
    Making User Logged out
    '''
    title = 'Home'
    logout(request)
    logger.info(
        logme("successfully logged out, redirected to home page", request)
    )
    # Navigating the user back to the Login page.
    return HttpResponseRedirect('/')


def change_password(request):
    '''
    Navigating to Change Password html
    '''
    title = 'Settings'
    user_status = request.user.profile.status
    context_dict = {}
    if user_status.notification_service:
        services = json.loads(user_status.notification_service)
        sms_status = services.get("sms_alert", True)
        newsletter_status = services.get("newsletter_alert", True)
        invitation_and_message = services.get("invitation_and_message", True)
        activity_involve = services.get("activity_involve", True)
        activity_by_network = services.get("activity_by_network", True)
        blog = services.get("blog", True)
        microlerning = services.get("microlerning", True)
        context_dict = {
            'sms_status': sms_status,
            'newsletter_status': newsletter_status,
            'invitation_and_message': invitation_and_message,
            'activity_involve': activity_involve,
            'activity_by_network': activity_by_network,
            'blog': blog,
            'microlerning': microlerning
        }
    logger.info(
        logme("redirected to change password page", request)
    )
    return render(request, "home/changepassword.html", context=context_dict)


def ethical_commitment_page(request):
    '''
    Navigating to ethical commitment html
    '''
    title = 'Ethical Commitment'
    logger.info(
        logme("redirected to the ethical commitment page", request)
    )
    return render(request, 'home/ethical_commitment_page.html', locals())


def code_of_coduct(request):
    '''
    Navigating to code_of_conduct html
    '''
    title = 'Code of coduct'
    logger.info(
        logme("redirected to the code of conduct page", request)
    )
    return render(request, 'home/code_of_coduct.html', locals())


def get_in_touch(request):
    '''
    Navigating to get_in_touch html
    '''
    title = 'Get in touch'
    context = RequestContext(request)
    hide_signup_popup = 1
    logger.info(
        logme("redirected to the get in touch page", request)
    )
    return render(request, 'home/get_in_touch.html', locals())


def contact_us_reia(request):
    '''
    Sending Contact us form to UPWRDZ admin through email and Thank you mail to user
    '''
    context = RequestContext(request)
    if request.method == 'POST':
        name = request.POST['name']
        mobile_number = request.POST['mobile_number']
        email_id = request.POST['email']
        city = request.POST['location']
        content_msg = request.POST['content_msg']
        context_dict = {
            'name': name,
            'mobile': mobile_number,
            'user_email': email_id,
            'city': city,
            'message': content_msg
        }
        send_mandrill_email('ABOTMI_27', [email_id], context=context_dict)
        send_mandrill_email_admin(
            'ABOTMI_24',
            [constants.REIA_ENQUIRY_ADMIN_EMAIL], request.POST['email'],
            context_dict
        )
        logger.info(
            logme("email sent to advisor & reia admin from contact us page", request)
        )
        return HttpResponse('success')
    else:
        logger.info(
            logme("GET request - access forbidden to contact us page", request)
        )
        return HttpResponse('Access forbidden')


def user_service_status_update(request):
    '''
    Descrption: Modifing the service
    '''
    if request.method == 'POST':
        name = None
        status = None
        if request.POST['name']:
            name = request.POST['name']
        if request.POST['status']:
            status = True if request.POST['status'] == 'true' else False
        user_status, created = UserStatus.objects.get_or_create(
            user_profile=request.user.profile
        )
        if name == "my_identity":
            user_status.my_identity_status = status
        if name == 'my_repute':
                user_status.my_repute_status = status
        user_status.save()
        return HttpResponse('success')
    else:
        return HttpResponse('Access Forbidden')


def notification_services_status(request):
    '''
    Descrption: Modifing the status for sending messages to Advisor.
    '''
    context = RequestContext(request)
    if request.method == 'POST':
        alert_status = request.POST['alert_status']
        notification_type = request.POST['notification_type']
        user_status = request.user.profile.status
        if notification_type:
            notifications = json.loads(user_status.notification_service)
            if alert_status == 'true':
                notifications[notification_type] = True
                notification_service = json.dumps(notifications)
                user_status.notification_service = notification_service
            else:
                notifications[notification_type] = False
                notification_service = json.dumps(notifications)
                user_status.notification_service = notification_service
            user_status.save()
        logger.info(
            logme("modified the status=%s for sending messages to \
                advisor" % (str(alert_status)), request)
        )
        return HttpResponse('success')


def privacy_and_policy(request):
    '''
    Navigating to privacy_and_policy html
    '''
    recaptcha_key = constants.RECAPTCHA_KEY
    title = 'Privacy and Policy'
    hide_signup_popup = 1
    logger.info(
        logme("redirected to the privacy policy page", request)
    )
    return render(request, 'home/privacy_and_policy.html', locals())


def summary_of_abotmi_privacy_policy(request):
    '''
    Navigate to summary of abomti privacy policy
    '''
    title = 'Summary of abomti privacy policy'
    recaptcha_key = constants.RECAPTCHA_KEY
    hide_signup_popup = 1
    logger.info(
        logme("redirected to summary of abomti privacy policy", request)
    )
    return render(request, 'home/summary_of_abotmi_privacy_policy.html', locals())


def summary_of_terms_condtions(request):
    '''
    Navigate to summary of abomti user agreement
    '''
    title = 'Summary of abomti terms and conditions'
    recaptcha_key = constants.RECAPTCHA_KEY
    hide_signup_popup = 1
    logger.info(
        logme("redirected to summary of abomti conditions", request)
    )
    return render(request, 'home/summary_of_terms_condtions.html', locals())


def get_advice_page(request):
    '''
    Navigate to get advice content page.
    '''
    title = 'Get Advice page'
    recaptcha_key = constants.RECAPTCHA_KEY
    hide_signup_popup = 1
    logger.info(
        logme("redirected to get advice content page", request)
    )
    return render(request, 'home/get_advice_page.html', locals())


def refer_advice_page(request):
    '''
    Navigate to refer advice content page.
    '''
    title = 'Refer advice page'
    recaptcha_key = constants.RECAPTCHA_KEY
    hide_signup_popup = 1
    logger.info(
        logme("redirected to refer advice content page", request)
    )
    return render(request, 'home/refer_advice_page.html', locals())


def rate_advice_page(request):
    '''
    Navigate to rate advice content page.
    '''
    title = 'Rate advice page'
    recaptcha_key = constants.RECAPTCHA_KEY
    hide_signup_popup = 1
    logger.info(
        logme("redirected to rate advice content page", request)
    )
    return render(request, 'home/rate_advice_page.html', locals())

# commented temporarly we use future purpose
# def build_page(request):
#     '''
#     Navigate to build page
#     '''
#     title = 'Build page'
#     recaptcha_key = constants.RECAPTCHA_KEY
#     hide_signup_popup = 1
#     logger.info(
#         logme("redirected to build page", request)
#     )
#     return render(request, 'home/build_page.html', locals())


def purpose_page(request):
    '''
    Navigate to purpose page
    '''
    title = 'Purpose page'
    recaptcha_key = constants.RECAPTCHA_KEY
    hide_signup_popup = 1
    logger.info(
        logme("redirected to purpose page", request)
    )
    return render(request, 'home/purpose_page.html', locals())


def about_us(request):
    '''
    Navigate to aboutus page
    '''
    title = 'About us'
    logger.info(
        logme("redirected to aboutus page", request)
    )
    return render(request, 'home/about_us.html', locals())


def people_page(request):
    '''
    Navigate to people page
    '''
    title = 'People page'
    recaptcha_key = constants.RECAPTCHA_KEY
    hide_signup_popup = 1
    logger.info(
        logme("redirected to people page", request)
    )
    return render(request, 'home/people_page.html', locals())


def partners_page(request):
    '''
    Navigate to partners page
    '''
    title = 'Partners page'
    recaptcha_key = constants.RECAPTCHA_KEY
    hide_signup_popup = 1
    logger.info(
        logme("redirected to partners page", request)
    )
    return render(request, 'home/partners_page.html', locals())


def opportunities_page(request):
    '''
    Navigate to opportunities page
    '''
    title = 'Opportunities page'
    recaptcha_key = constants.RECAPTCHA_KEY
    hide_signup_popup = 1
    logger.info(
        logme("redirected to opportunities page", request)
    )
    return render(request, 'home/opportunities_page.html', locals())


def protection_page(request):
    '''
    Navigate to protection page
    '''
    title = 'Protection page'
    recaptcha_key = constants.RECAPTCHA_KEY
    hide_signup_popup = 1
    logger.info(
        logme("redirected to protection page", request)
    )
    return render(request, 'home/protection_page.html', locals())


def advisor_page(request):
    '''
    Navigate to advisor page
    '''
    title = 'Advisor How It Works'
    # recaptcha_key = constants.RECAPTCHA_KEY
    # hide_signup_popup = 1
    logger.info(
        logme("redirected to advisor page", request)
    )
    return render(request, 'home/advisor_page.html', locals())


def cookie_policy(request):
    '''
    Navigate to cookie policy page
    '''
    title = 'Cookie policy Page'
    recaptcha_key = constants.RECAPTCHA_KEY
    hide_signup_popup = 1
    logger.info(
        logme("redirected to Cookie policy Page", request)
    )
    return render(request, 'home/cookie_policy.html', locals())


def copyright_policy(request):
    '''
    Navigate to copyright policy page
    '''
    title = 'copyright policy Page'
    recaptcha_key = constants.RECAPTCHA_KEY
    hide_signup_popup = 1
    logger.info(
        logme("redirected to copyright policy Page", request)
    )
    return render(request, 'home/copyright_policy.html', locals())


def why_us(request):
    '''
    Navigate to why us page
    '''
    title = 'Why Us'
    logger.info(
        logme("redirected to why us page", request)
    )
    return render(request, 'home/why_us.html', locals())


# Temporarly commented 
# def learn_more_resources(request):
#     '''
#     Navigating to learn_more_resources html
#     '''
#     title = 'Resources'
#     logger.info(
#         logme("redirected to the learn more resources page", request)
#     )
#     return render(request, 'home/learn_more_resources.html', locals())


def advisor_loop_termsandconditions(request):
    '''
    Navigating to advisor_loop_termsandconditions html
    '''
    title = 'Advisor LOOP Terms and Conditions'
    logger.info(
        logme("redirected to advisor loop terms and conditions page", request)
    )
    return render(request, 'home/advisor_loop_termsandconditions.html', locals())


def kyc_registration_terms_conditions(request):
    '''
    Navigating to kyc_registration_terms_conditions html
    '''
    title = 'KYC Registration Terms and Conditions'
    logger.info(
        logme("redirected to the KYC registration terms & conditions page", request)
    )
    return render(request, 'home/kyc_registration_terms_conditions.html', locals())


def home(request):
    '''
    Navigating to index_base html
    '''
    title = 'Home'
    testimonals = Testimonial.objects.all()
    return render(request, 'index_base.html', locals())


def apply_crisil_verification(request):
    '''
    setting apply_for_crisil in session to load the Apply CRISIL Modal when user
    Navigting to Dashboard
    '''
    title = 'Apply CRISIL verification'
    context = RequestContext(request)
    request.session['apply_for_crisil'] = 1
    logger.info(
        logme("redirected to apply CRISIL verification dashboard page", request)
    )
    return HttpResponseRedirect('/dashboard/')


def crisil_verified_advisor(request):
    '''
    Navigating to crisil_verified_advisor html
    '''
    title = 'CRISIL verified advisor'
    logger.info(
        logme("redirected to the CRISIL verified advisor page", request)
    )
    return render(request, 'home/crisil_verified_advisor.html', locals())


def signup_terms_and_conditions(request):
    '''
    Navigting to signup_terms_and_conditions html
    '''
    recaptcha_key = constants.RECAPTCHA_KEY
    logger.info(
        logme("redirected to signup terms & conditions page", request)
    )
    return render(request, 'home/signup_terms_and_conditions.html', locals())


def server_health(request):
    '''
    returns the server alive or not
    '''
    current_ts = datetime.datetime.now()
    server_health = "WOW I am Alive TimeStamp: "+str(current_ts)
    logger.info(
        logme('checked server health', request)
    )
    return HttpResponse(server_health)


def abotmi_faq(request):
    '''
    Navigating to abotmi faq html
    '''
    title = 'ABOTMI faq'
    logger.info(
        logme("redirected to ABOTMI faq page", request)
    )
    return render(request, 'home/abotmi_faq.html', locals())


def how_it_work(request):
    '''
    Navigating to how it works html
    '''
    title = 'How It works'
    logger.info(
        logme("redirected to How It works page", request)
    )
    return render(request, 'home/how_it_work.html', locals())


def advisors(request):
    '''
    Navigating to advisors html
    '''
    title = 'Advisors'
    logger.info(
        logme("redirected to advisors page", request)
    )
    return render(request, 'home/advisors.html', locals())


def investors(request):
    '''
    Navigating to investors html
    '''
    title = 'Investors'
    logger.info(
        logme("redirected to Investors page", request)
    )
    return render(request, 'home/investors.html', locals())


def refer_friend(request):
    '''
    refer friend details are saving and triggering a mail for both ends.
    '''
    if request.method == "POST":
        name = request.POST.get('name', None)
        email = request.POST.get('your_email', None)
        friend_name = request.POST.get('refer_first_name', None)
        friend_email = request.POST.get('refer_email', None)
        try:
            refer_friend, created = ReferFriend.objects.get_or_create(
                email=email, friend_email=friend_email)
        except Exception as e:
            print (e)
        if refer_friend:
            refer_friend.name = name
            refer_friend.friend_name = friend_name
            refer_friend.save()
            try:
                send_mandrill_email(
                    'ABOTMI_14',
                    [email],
                    context={
                        'referred_name': friend_name,
                        'referred_by_name': name
                    }
                )
                send_mandrill_email(
                    'ABOTMI_13',
                    [friend_email],
                    context={
                        'referred_name': friend_name,
                        'referred_by_name': name,
                        'url': settings.DEFAULT_DOMAIN_URL
                    }
                )
            except:
                logger.debug('Mail failed while sending request to user')
            return HttpResponse('You have referred you friend', status=200)
        else:
            return HttpResponse('unable to refer friend.', status=204)


def list_notifications(request):
    title = 'Notifications'
    user_profile = request.user.profile
    n_f = Notification.objects.filter(
        receive_id=str(user_profile.id)
        ).order_by('-created_date')[:10 if request.is_ajax() else None]
    nf_res = NotificationListSerializer(
        n_f,
        many=True,
        context={'user_profile': user_profile}
    )
    context_dict = {
        'nf_res': nf_res.data,
        'n_f_count': n_f.count(),
        'title': title
    }
    Notification.objects.all().update(view_status=True)
    if request.is_ajax():
        template_name = 'home/notification_dropdown.html'
    else:
        template_name = 'home/notification.html'
    return render(request, template_name, context=context_dict)


def get_notification_count(request):
    user_profile = request.user.profile
    n_f = Notification.objects.filter(
        receive_id=str(user_profile.id),
        view_status=False).order_by('-created_date').count()
    return JsonResponse(data={'nf_count': n_f})


def update_notification_status(request):
    '''
    Updating the notification status
    '''
    if request.method == 'POST':
        ids = request.POST.getlist('ids[]', [])
        if ids:
            ids = map(str, ids)
            nf = NotificationFunctions.update_read_status(ids)
            return HttpResponse(200)
        else:
            return HttpResponse(400)
    else:
        return HttpResponse(405)
