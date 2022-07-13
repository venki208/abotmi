# Python lib
import os
import base64
import cStringIO as StringIO
import datetime
from datetime import timedelta
import dateutil.parser
import hashlib
import json
import logging
import random
import requests
import uuid
import ast
import dateutil.parser

# django libs
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout, login
from django.contrib.sites.models import Site
from django.core import serializers
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import default_storage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Sum, Avg, Q
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext, Context
from django.template.loader import render_to_string, get_template
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, View

# signup app modules
# Advisor Check
from advisor_check.constants import ADVISOR_TYPE
from advisor_check.common_views import AdvisorCheckCommonFunctions
from advisor_check.models import IrdaData, AmfiData, SebiData

from blockchain.tasks import create_user_blockchain_account_and_transaction
from blog import views as blog_views

# common
from common import constants
from common.api_constants import (
    GOOGLE_SINGLE_URL, FACEBOOK_SINGLE_URL, LINKEDIN_SINGLE_URL, NEXT_URL_LINK
)
from common.notification.constants import(
    REGISTRATION_TEMPLATE, REFER_REGISTRATION, RATE_RES, RANK_RES
)
from common.utils import generate_key, send_sms_alert, clean_text
from common.views import (
    referral_points, check_crisil_advisor, generate_pdf, get_all_advisors_count,
    get_binary_image, upload_image_and_get_path, get_eipv_documents, logme,
    get_sms_status, get_kyc_step_status, get_practice_contry_details_json,
    UploadDocumentsFunctions, get_remove_rera_doc, EducationQualificationFunctions,
    get_ip_region)

# login
from login.decorators import allow_crisil_admin, referral_user, allow_advisor

# models
from datacenter.models import (
    Advisor, EmailVerification, UserProfile, CrisilCertifications, UploadDocuments,
    India_Pincode, UserReferral, Country, ExternalUser, AdvisorRating,
    NoticeBoard, AffiliatedCompany, CompanyAdvisorMapping, PanNumberVerfication,
    UserMobileOtp, AdvisorType, PromoCodes, DigitalFootPrint,
    EducationAndCertificationDetails)

# nsdl
from nsdl.tasks import get_pan_details

from forms import InviteAdvisorForm, memberreferform
from signup.djmail import (
    send_mandrill_email, send_mandrill_email_with_attachement, 
    send_mandrill_email_dynamic_from, send_mandrill_email_admin, 
    send_mandrill_email_admin_subject)

# Dashboard notifications
from common.notification.views import NotificationFunctions

# icore
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, comments, posts
from wordpress_xmlrpc.methods.posts import NewPost
from wordpress_xmlrpc.base import *
from wordpress_xmlrpc.wordpress import WordPressComment

# general python libs
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from random import randint
from time import gmtime, strftime
from urlparse import urlparse
from mimetypes import MimeTypes

# other apps in project
from xhtml2pdf import pisa
from tld import get_tld
from wkhtmltopdf.views import PDFTemplateResponse

logger = logging.getLogger(__name__)


@referral_user
def signup(request):
    '''
    Navigting to Signup Page
    '''
    context = RequestContext(request)
    if request.method == 'GET':
        if request.user.is_authenticated():
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        else:
            ref = request.GET.get('ref_link', None)
            recaptcha_key = constants.RECAPTCHA_KEY
            if settings.FACEBOOK_API:
                facebook_api = settings.FACEBOOK_API
            # IP Recognisation
            ip_details = request.session['ip_info']
            user_agent_country = ip_details.get("country", constants.REGION_DEFAULT)
            ip_region = user_agent_country
            context_dict = {
                'LOGIN_URL': settings.LOGIN_URL,
                'FACEBOOK_API': settings.FACEBOOK_API,
                'FACEBOOK_SINGLE_URL': FACEBOOK_SINGLE_URL,
                'next': request.GET.get('next', settings.LOGIN_REDIRECT_URL),
                'REF': ref,
                'ip_region': ip_region,
                'title': 'Login'
            }
            logger.info(
                logme("login page opened using referral link", request)
            )
            return render_to_response(
                'login.html',
                context_dict,
                context_instance=RequestContext(request)
            )


def register(request):
    '''
    Submitting the Advisor Registration details
    '''
    if request.method == 'POST':
        # Auth User ---
        user = User.objects.get(username=request.user.username)
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        user.first_name = request.POST.get('first_name', None)
        user.last_name = request.POST['last_name']
        user.save()
        req_type = request.POST.get('req_type', None)
        # Auth User ---
        # User Profile ---
        user_profile = UserProfile.objects.get(user=user)
        user_profile.first_name = request.POST['first_name']
        user_profile.middle_name = request.POST['middle_name']
        user_profile.last_name = request.POST['last_name']
        user_profile.mobile = request.POST['mobile']
        user_profile.email = request.POST['username']
        user_profile.secondary_email = request.POST['secondary_email']
        if request.POST.get('communication_email_secondary', None) == constants.SECONDARY:
            user_profile.communication_email_id = constants.SECONDARY
        else:
            user_profile.communication_email_id = constants.PRIMARY
        user_profile.suffix = request.POST.get('suffix', '')
        # date converted indian format into python format
        if request.POST.get('birthdate', None):
            date_birth = datetime.datetime.strptime(
                request.POST.get('birthdate', None), '%m-%d-%Y').strftime('%Y-%m-%d')
            user_profile.birthdate = date_birth
            user_profile.save()
        user_profile.gender = request.POST['gender'][0]
        user_profile.is_advisor = True
        user_profile.nationality = request.POST.get('nationality', '')
        user_profile.street_name = request.POST.get('street_name', '')
        user_profile.address = request.POST.get('address', '')
        user_profile.city = request.POST.get('city', '')
        user_profile.pincode = request.POST.get('pincode', '')
        user_profile.state = request.POST.get('state', '')
        user_profile.country = request.POST.get('country', '')
        user_profile.my_belief = request.POST.get('my_belief', '')
        user_profile.save()
        # User Profile ---
        # Advisor Details ----
        advisor_details, created = Advisor.objects.get_or_create(
            user_profile=user_profile)
        user_status = user_profile.status
        if req_type == 'mobile':
            prac_country_obj = Country.objects.filter(
                name=request.POST['practice_country']).first()
            if prac_country_obj:
                advisor_details.practice_country = prac_country_obj
            advisor_details.practice_location = request.POST.get('practice_location', '')
            advisor_details.practice_city = request.POST.get('practice_city', None)
        advisor_details.my_promise = request.POST['my_promise']
        # advisor_details.practice_details = request.POST.get(
        #                                     'hidden_practice_details_input', None)
        advisor_details.save()
        user_status.save()
        logger.info(
            logme("saving advisor registration details(step 1), redirected to \
            personal information page(step 2)", request)
        )
        if req_type == "mobile":
            return "success"
        else:
            return redirect('/signup/business_information/')
        # ==================== User Registration ======================== #
    if request.method == 'GET':
        logger.info(
            logme("GET request- access forbidden to save registration details", request)
        )
        return redirect(settings.LOGIN_REDIRECT_URL)


def save_my_belief(request):
    '''
    Saving My Belief details
    '''
    context = RequestContext(request)
    if request.method == 'POST':
        user = User.objects.get(username=request.user.username)
        user_profile = UserProfile.objects.get(user=user)
        user_profile.my_belief = request.POST.get('my_belief', None)
        user_profile.save()
        logger.info(
            logme("updated my belief", request)
        )
        return HttpResponse("success")


def user_profile_basicdetails(request):
    '''
    Saving/Updating the User Profile in database (second step in Registraion process)
    '''
    if request.method == 'POST':
        user = request.user
        user_profile = user.profile
        advisor = user_profile.advisor
        req_type = request.POST.get('req_type', None)
        user_profile.company_name = request.POST.get('company_name', None)
        user_profile.company_city = request.POST.get('company_city', None)
        user_profile.company_website = request.POST.get('company_website', None)
        user_profile.designation = request.POST.get('designation', None)
        user_profile.annual_income = request.POST.get('annual_income', None)
        user_profile.language_known = request.POST.get('language_known', None)
        user_profile.languages_known_read_write = request.POST.get(
            'languages_known_read_write', None)
        user_profile.company_address1 = request.POST.get('company_address1', None)
        user_profile.company_address2 = request.POST.get('company_address2', None)
        user_profile.company_landmark = request.POST.get('company_landmark', '')
        user_profile.company_locality = request.POST.get('company_locality', '')
        user_profile.company_pincode = request.POST.get('company_pincode', None)
        user_profile.company_state = request.POST.get('company_state', None)
        user_profile.company_country = request.POST.get('company_country', None)
        advisor.practice_details = request.POST.get(
                                            'hidden_practice_details_input', None)
        user_profile.pan_no = request.POST.get('pan_no', '')
        if req_type == "mobile":
            user_profile.mother_tongue = request.POST.get('mother_tongue', None)
        user_profile.save()
        if request.POST.get('is_submitted_all', None) == 'false':
            advisor.is_submitted_all = False
        else:
            advisor.is_submitted_all = True
        if advisor.is_submitted_questions and advisor.is_submitted_all:
            advisor.is_confirmed_advisor = True
        advisor.save()
        logger.info(
            logme('updated personal information(step 2)', request)
        )
        if req_type == "mobile":
            return "success"
        else:
            return HttpResponse('success')


def user_profile_answer(request):
    '''
    Saving/Updating Business Information Questions and Answers
    (third step in user profile)
    '''
    if request.method == 'POST':
        req_type = request.POST.get('req_type', None)
        questions = request.POST.get('questions', None)
        old_domain_names = []  # Creating Empty array for setting old domain names
        new_domain_names = []  # Creating Empty array for setting new domain names
        new_question_list = ''
        new_financial_question_list = ''
        old_question_list = ''
        old_financial_json_data = ''
        old_office_address_json_data = ''
        new_office_address_json_data = ''
        advisor_exist = Advisor.objects.get(user_profile=request.user.profile)
        if advisor_exist.questions:
            old_question_list = json.loads(advisor_exist.questions)
            old_financial_json_data = old_question_list[2]['Remark'][0]['Remark']
            old_office_address_json_data = old_question_list[1]['Remark']
        if questions:
            new_question_list = json.loads(questions)
            new_financial_question_list = new_question_list[2]['Remark'][0]['Remark']
            if new_question_list:
                if new_question_list[0]['Answer'] == 'yes':
                    advisor_exist.total_clients_served = new_question_list[
                        0]['Remark'][1]['Answer']
                    advisor_exist.total_advisors_connected = new_question_list[0][
                        'Remark'][3]['Answer']

        if not questions == advisor_exist.questions:
            if (not old_financial_json_data == new_financial_question_list or
                    not old_office_address_json_data == new_office_address_json_data):
                if old_financial_json_data:
                    count = 1
                    num = 0
                    for i in old_financial_json_data:
                        num = num + 1
                        if num == count:
                            email = old_question_list[2][
                                'Remark'][0]['Remark'][count]['Answer']
                            domain = email.split("//")[-1].split("/")[0]
                            domain = 'http://'+domain
                            domain_name = get_tld(domain)
                            count = count + 4
                            old_domain_names.append(str(domain_name))
                if new_financial_question_list:
                    count = 1
                    num = 0
                    for i in new_financial_question_list:
                        num = num + 1
                        if num == count:
                            email = new_question_list[2][
                                'Remark'][0]['Remark'][count]['Answer']
                            domain = email.split("//")[-1].split("/")[0]
                            domain = 'http://'+domain
                            domain_name = get_tld(domain)
                            count = count + 4
                            new_domain_names.append(str(domain_name))
                # seperating common domain names from existing and new data
                common_domain_names = list(set(old_domain_names) & set(new_domain_names))
                for domain in common_domain_names:
                    new_domain_names.remove(domain)  # removing existing domain
                for domain in common_domain_names:
                    old_domain_names.remove(domain)  # removing existing domain
                if new_domain_names:
                    for new_domain in new_domain_names:
                        company = AffiliatedCompany.objects.filter(
                            domain_name=new_domain)
                        if company:
                            company = company.first()
                            company.users_count = company.users_count + 1
                            company.save()
                        else:
                            email = "contact@" + new_domain
                            company_name = new_domain
                            user = None
                            user_password = get_random_string(length=8)
                            user, created = User.objects.get_or_create(
                                username=email,
                                email=email
                            )
                            if created:
                                user.set_password(user_password)
                                user.is_active = True
                                user.is_staff = True
                                user.save()
                                user_profile = user.profile
                                user_profile.email = email
                                user_profile.is_company = True
                                user_profile.save()
                                company_obj, status = AffiliatedCompany.objects.\
                                    get_or_create(user_profile=user_profile)
                                company_obj.domain_name = company_name
                                company_obj.users_count = company_obj.users_count + 1
                                company_obj.save()
                if old_domain_names:
                    for old_domain in old_domain_names:
                        company = None
                        company = AffiliatedCompany.objects.filter(
                            domain_name=old_domain)
                        if company:
                            company = company.first()
                            if company.users_count > 0:
                                company.users_count = company.users_count-1
                                company.save()
        advisor_exist.questions = questions
        if request.POST['is_submitted_questions'] == 'false':
            advisor_exist.is_submitted_questions = False
        else:
            advisor_exist.is_submitted_questions = True
        if advisor_exist.is_submitted_questions and advisor_exist.is_submitted_all:
            advisor_exist.is_confirmed_advisor = True
        advisor_exist.save()
        logger.info(
            logme('updated business information (step 3)', request)
        )
        if req_type == 'mobile':
            return 'success'
        else:
            return HttpResponse("success")


@login_required()
def upload_file(request):
    '''
    ============================================
    Upload Or replace Documents and save with
    username and Registration Id in the database
    ============================================
    '''
    required_documents = 0
    advisor_obj = None
    document_file_name = None
    uploaded_mandatory_documents = 0
    if request.method == 'POST':
        user_ob = request.user.profile
        if user_ob.is_advisor:
            advisor_obj = Advisor.objects.filter(user_profile=user_ob).first()
        documents_type = request.POST.get('documents_type', None)
        reupload = request.POST.get('reupload', None)
        if documents_type == "Profile Picture":
            profile_pic_document = request.POST.get('profile_pic', None)
            if profile_pic_document:
                picture_path = upload_image_and_get_path(
                    user_ob,
                    documents_type,
                    profile_pic_document
                )
                user_ob.picture = picture_path
                user_ob.save()
        if documents_type == 'pan_card':
            if request.user.profile.nationality:
                pan_details = get_pan_details.apply_async(
                    (request.POST.get('pan_no', None), request.user.profile.id)
                )
                user_ob.pan_no = request.POST.get('pan_no', None)
        if documents_type == 'passport':
            user_ob.passport_no = request.POST.get('passport_no', None)
        chk_document_type = UploadDocuments.objects.filter(
            user_profile=user_ob).filter(
            documents_type=str(documents_type)
        )
        if chk_document_type and reupload == 'true':
            chk_document_type.delete()
        user_profile = UserProfile.objects.get(user=request.user)
        documents_new_upload = UploadDocuments.objects.create(
            user_profile=user_profile
        )
        if documents_type == "Profile Picture":
            documents_new_upload.documents = picture_path
            documents_new_upload.documents_type = documents_type
            documents_new_upload.save()
        else:
            document_file = request.FILES['document']
            document_file_name = document_file.name
            documents_new_upload.documents = request.FILES['document']
            documents_new_upload.documents_type = documents_type
            documents_new_upload.save()
            # setting eipv face capture as profile pic
            if documents_type == 'eipv_face_capture':
                user_ob.picture = documents_new_upload.documents
                user_ob.save()

        if request.user.profile.nationality == "India":
            indian_proof = UploadDocuments.objects.filter(
                user_profile=request.user.profile
            ).filter(documents_type='pan_card')
        else:
            indian_proof = UploadDocuments.objects.filter(
                user_profile=request.user.profile
            ).filter(documents_type='passport')
        if advisor_obj:
            if indian_proof and not advisor_obj.is_document_submited:
                required_documents = 1
                advisor_obj.is_document_submited = required_documents
            advisor_obj.save()
        response = JsonResponse(
            {
                'url': documents_new_upload.documents.url,
                'file_name': document_file_name,
                'id': documents_new_upload.id,
                'required_documents': required_documents,
                'uploaded_mandatory_documents': uploaded_mandatory_documents
            }
        )
        logger.info(
            logme('%s document uploaded' % (documents_type), request)
        )
        return response
    if request.method == 'GET':
        logger.info(
            logme('GET request - access forbidden for document upload', request)
        )
        return HttpResponse("uploaded")


@login_required()
def delete_upload_file(request):
    '''
    Deleting the Documents and saving in the database
    '''
    if request.method == 'POST':
        doc_id = request.POST.get('id', None)
        req_type = request.POST.get('req_type', None)
        if doc_id:
            document = UploadDocumentsFunctions(request, request.user.profile)
            is_doc_deleted = document.remove_document(
                doc_id=doc_id.split(","))
            if is_doc_deleted:
                del(document)
                if req_type == 'mobile':
                   return 'success'
                else:   
                    return HttpResponse('success')
            else:
                del(document)
                if req_type == 'mobile':
                   return 'failed'
                else:
                   return HttpResponse('failed')
        else:
            if req_type == 'mobile':
                   return 'failed'
            else:
               return HttpResponse('failed')
    if request.method == 'GET':
        logger.info(
            logme('GET request - access forbidden for document deletion', request)
        )
        return HttpResponse("Access forbidden")


def check_email(request):
    '''
    Checking Email is Already exists or not in the database
    '''
    if request.method == "POST":
        username = request.POST.get('username', None)
        user = User.objects.filter(username=username).first()
        user_profile = UserProfile.objects.filter(user=user).first()
        try:
            if user and user_profile.is_advisor:
                return HttpResponse(status=200)
            else:
                return HttpResponse(status=204)
            logger.info(
                logme('validation - email exists', request)
            )
        except Exception as e:
            logger.info(
                logme('Error: Checking Emails--%s' % (str(e)), request)
            )
            return HttpResponse(status=500)
    if request.method == "GET":
        logger.info(
            logme('GET request - access forbidden for checking email', request)
        )
        return HttpResponse(status=405)


def check_email_for_business_information(request):
    '''
    Already existing E-Mail in the database for business_information
    '''
    if request.method == "POST":
        username = request.POST.get('username', None)
        user_email = Advisor.objects.filter(questions__contains=username)
        if user_email:
            logger.info(
                logme('validation - email exists in advisor questions', request)
            )
            return HttpResponse('false')
        else:
            logger.info(
                logme('validation - email does not exist in advisor questions', request)
            )
            return HttpResponse('true')
    if request.method == "GET":
        logger.info(
            logme(
                'GET request - access forbidden for checking email in advisor questions',
                request
            )
        )
        return HttpResponse('sorry cannot process')


def send_forgot_password_link(request):
    '''
    Description:
        POST:
            -> Checking Email is register or direct signup or company advisor
            -> Generating activation link and sending to respective email id
        GET:
            -> Navigating to forgot password page(advisor resets the password)
    '''
    if request.method == 'POST':
        add_url_param = ''
        user = User.objects.filter(
            username=request.POST.get('resend_email', None)).first()
        resend_link = request.POST.get('resend_link', None)
        if user:
            user_profile = user.profile
            advisor = user_profile.advisor
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            activation_key = hashlib.sha1(salt+user.email).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)
            if (advisor.is_register_advisor or
                    user_profile.source_media == constants.SIGNUP_WITH_EMAIL or
                    user_profile.is_company):
                    verification, created = EmailVerification.objects.get_or_create(
                        user_profile=user_profile)
                    verification.activation_key = activation_key
                    verification.key_expires = key_expires
                    verification.save()
                    try:
                        communication_email = user_profile.email
                        if user_profile.communication_email_id == 'secondary':
                            communication_email = user_profile.secondary_email
                        if resend_link:
                            mail_template = 'ABOTMI_23'
                            add_url_param = '&pwd_type=signup'
                        else:
                            mail_template = 'ABOTMI_26'
                        send_mandrill_email(
                            mail_template,
                            [communication_email],
                            context={
                                'Name': user_profile.first_name,
                                'Website': settings.DEFAULT_HOST,
                                'Ack': activation_key + add_url_param
                            }
                        )
                        logger.info(
                            logme(
                                'forgot password link sent to the advisor email',
                                request
                            )
                        )
                    except:
                        logger.error(
                            logme(
                                'failed to send email for forgot password link',
                                request
                            )
                        )
                    return JsonResponse(data={'success': '', 'status': 200})
            elif user_profile.is_member:
                return JsonResponse(data={'success': 'not_advisor', 'status': 200})
            else:
                return JsonResponse(data={'success': 'not_registered', 'status': 200})
        else:
            return JsonResponse(data={'success': 'not_registered', 'status': 204})
    else:
        logger.info(
            logme('forgot password page rendered', request)
        )
        return render_to_response('signup/forget_password.html', context_dict, context)


def forgot_password_change(request):
    '''
    Description:
        GET:
            -> Checking activation link and navigating to reset_password html
        POST:
            -> Checking activation link
            -> Setting New password
            -> Deleting the activation link
    '''
    PRODUCT_NAME = settings.PRODUCT_NAME
    title = constants.SET_PASSWORD
    # Setting user obj in session for using the user details in Post
    user = request.session.get('user')
    if request.method == 'GET':
        try:
            verification = EmailVerification.objects.get(
                activation_key=request.GET['ack'])
            logger.info(
                logme('activation key verified for forgot password change', request)
            )
        except:
            logger.info(
                logme('activation link wrong/expired for forgot password change', request)
            )
            return HttpResponse("Activation link may be wrong or expired")
        expiry_date = verification.created_date + timedelta(days=1)
        if expiry_date <= datetime.datetime.now(expiry_date.tzinfo):
            verification.delete()
            return HttpResponse("The Activation link has been expired.")
        user_auth_obj = User.objects.get(username=verification.user_profile.user.username)
        request.session['user'] = user_auth_obj.username
        recaptcha_key = constants.RECAPTCHA_KEY
        logger.info(
            logme('rendered reset password page', request)
        )
        pwd_type = request.GET.get('pwd_type', None)
        return render(request, 'signup/reset_password.html', locals())
    if request.method == 'POST':
        # Receiving session for using the user details in Post
        user = request.session.get('user')
        user_auth_obj = User.objects.get(username=user)
        user_profile = UserProfile.objects.get(user=user_auth_obj)
        new_password = request.POST.get('password_reset', None)
        pwd_type = request.POST.get('pwd_type', None)
        if new_password:
            user_auth_obj.set_password(new_password)
            user_auth_obj.save()
            user_status = user_profile.status
            if (user_profile.source_media == constants.SIGNUP_WITH_EMAIL and 
                    not user_status.email_verified):
                    user_status.email_verified = True
                    user_status.save()
            try:
                verification = EmailVerification.objects.filter(user_profile=user_profile)
                verification.delete()
                if pwd_type:
                    user_auth_obj.backend = 'django.contrib.auth.backends.ModelBackend'
                    user_auth_obj.save()
                    login(request, user_auth_obj)
            except:
                logger.info(
                    logme(
                        'activation link wrong/expired for forgot password change',
                        request
                    )
                )
            logger.info(
                logme('advisor password reset successfully', request)
            )
            return HttpResponse('success')
        else:
            return HttpResponse('failed')


@login_required()
def user_createpassword(request):
    '''
    Changing the password
    '''
    if request.method == "POST":
        oldpassword = request.POST.get('oldpassword', None)
        newpassword = request.POST.get('newpassword', None)
        if request.user.check_password(oldpassword):
            request.user.set_password(newpassword)
            request.user.save()
            logger.info(
                logme('advisor password changed successfully', request)
            )
            return HttpResponse('success')
        else:
            logger.info(
                logme(
                    'advisor entered wrong old password, redirected to change password',
                    request
                )
            )
            return HttpResponseRedirect('/change_password/')
    else:
        logger.info(
            logme('GET request- access forbidden to change password', request)
        )
        return HttpResponse('Access forbidden')


@login_required()
def user_checkpassword(request):
    '''
    Checking Password Matching with User Password
    '''
    if request.method == "POST":
        oldpassword = request.POST['oldpassword']
        if request.user.check_password(oldpassword):
            logger.info(
                logme('validation - entered correct old password', request)
            )
            return HttpResponse("true")
        else:
            logger.info(
                logme('validation - entered wrong old password', request)
            )
            return HttpResponse("false")
    else:
        logger.info(
            logme('GET request- access forbidden for validating password', request)
        )
        return HttpResponse("Access Forbidden")


class SearchPincode(View):
    '''
    Searching the pincode and give results
    '''
    def post(self, request, *args, **kwargs):
        pincode = request.POST.get('s_key', None)
        pin_obj = India_Pincode.objects.filter(
            pin_code__contains=pincode).values('pin_code')[:10]
        return JsonResponse(data={'pincodes': list(pin_obj)}, status=200)


class AdvisorRegistration(View):
    '''
    Navigating to advisor_registration html
    '''

    @method_decorator(allow_advisor)
    def get(self, request, *args, **kwargs):
        title = constants.PERSONAL_INFORMATION
        country_list = Country.objects.all().values('name')
        user = request.user
        user_profile = UserProfile.objects.get(user=user)
        advisor = Advisor.objects.get(user_profile=user_profile)
        user_status = user_profile.status

        '''
        Progress bar
        '''
        result = get_kyc_step_status(request, user, user_profile, advisor)

        '''
        Financial instrument
        '''
        financial_instruments = advisor.financial_instruments
        if not financial_instruments:
            financial_instruments_json = None
        if financial_instruments is None or not financial_instruments:
            financial_instruments = '[{"instruments":"select","experience":""}]'
        if financial_instruments:
            financial_instruments_json = json.loads(financial_instruments)
            all_financial_instrument = constants.ALL_FINANCIAL_INSTRUMENT

        '''
        Rera details
        '''
        if advisor.is_rera and advisor.rera_details:
            rera_result = json.loads(advisor.rera_details)

        '''
        Dsa Details
        '''
        if advisor.dsa_details:
            dsa_result = json.loads(advisor.dsa_details)

        '''
        Mobile Number
        '''
        if user_profile.mobile:
            mobile_number = user_profile.mobile

        '''
        CRISIL Certification valid status (return True or False)
        '''
        crisil_certificate_valid = check_crisil_advisor(advisor)

        '''
        Regulatory Registration Uploaded Documents
        '''
        document = UploadDocumentsFunctions(request, user_profile)
        # SEBI CERTIFICATE STATUS
        sebi_certificate_status = document.check_document(constants.SEBI_CERTIFICATE)
        sebi_renewal_certificate = document.check_document(
            constants.SEBI_RENEWAL_CERTIFICATE)
        # AMFI CERTIFICATE STATUS
        amfi_certificate_status = document.check_document(constants.AMFI_CERTIFICATE)
        amfi_renewal_certificate = document.check_document(
            constants.AMFI_RENEWAL_CERTIFICATE)
        # IRDA CERTIFICATE STATUS
        irda_certificate_status = document.check_document(constants.IRDA_CERTIFICATE)
        irda_renewal_certificate = document.check_document(
            constants.IRDA_RENEWAL_CERTIFICATE)
        # REGULATORY OTHERS STATUS
        others_certificate_status = document.check_document(constants.OTHER_CERTIFICATE)
        others_renewal_certificate = document.check_document(
            constants.OTHER_RENEWAL_CERTIFICATE)
        del(document)
        logger.info(
            logme('rendered advisor registration page(step 1)', request)
        )
        return render(request, "signup/advisor_registration.html", locals())


def show_regulatory_doc_modal(request):
    '''
    Description: Loading Regulatory uploaded documents modal
    '''
    if request.method == 'POST':
        user_profile = request.user.profile
        regulatory_type = request.POST.get('regulatory_type', None)
        document = UploadDocumentsFunctions(request, user_profile)
        '''
        SEBI DOC
        '''
        if regulatory_type == 'sebi':
            certificate = document.get_document(constants.SEBI_CERTIFICATE)
            renewal_certificate = document.get_document(
                constants.SEBI_RENEWAL_CERTIFICATE, many=True)
        '''
        AMFI DOC
        '''
        if regulatory_type == 'amfi':
            certificate = document.get_document(constants.AMFI_CERTIFICATE)
            renewal_certificate = document.get_document(
                constants.AMFI_RENEWAL_CERTIFICATE, many=True)
        '''
        IRDA DOC
        '''
        if regulatory_type == 'irda':
            certificate = document.get_document(constants.IRDA_CERTIFICATE)
            renewal_certificate = document.get_document(
                constants.IRDA_RENEWAL_CERTIFICATE, many=True)

        '''
        Others Doc
        '''
        if regulatory_type == 'reg_others':
            certificate = document.get_document(constants.OTHER_CERTIFICATE)
            renewal_certificate = document.get_document(
                constants.OTHER_RENEWAL_CERTIFICATE, many=True)

        '''
        RERA Doc
        '''
        if regulatory_type == 'rera':
            certificate, renewal_certificate = None, None
            certificate_id = request.POST.get('certificate_id', None)
            renewal_certificate_id = request.POST.get('renewal_certificate_id', None)
            if certificate_id:
                certificate = document.get_document(
                    constants.RERA_CERTIFICATE, doc_id=certificate_id)
            if renewal_certificate_id:
                renewal_certificate_id = renewal_certificate_id.split(",")
                renewal_certificate = document.get_document(
                    constants.RERA_RENEWAL_CERTIFICATE,
                    doc_id=renewal_certificate_id,
                    many=True
                )
        del(document)
        return render(request, 'signup/regulatory_registration_upload.html', locals())
    else:
        return HttpResponse('Access forbidden')


def show_education_qualification(request):
    '''
    Description: Loading certificates
    '''
    if request.method == 'POST':
        user_profile = request.user.profile
        education_qualifications = request.POST.get('education_qualification_type', None)
        document = UploadDocumentsFunctions(request, user_profile)
        if education_qualifications == 'highest_qualification_upload_cert':
            certificate = document.get_document(constants.HIGHEST_QUALIFICATION)
        elif education_qualifications == 'edu_qua_certificate1':
            certificate = document.get_document(constants.ADDITIONAL_EDUC_QUALIFICATION1)
        elif education_qualifications == 'edu_qua_certificate2':
            certificate = document.get_document(constants.ADDITIONAL_EDUC_QUALIFICATION2)
        elif education_qualifications == 'edu_qua_certificate3':
            certificate = document.get_document(constants.ADDITIONAL_EDUC_QUALIFICATION3)
        elif education_qualifications == 'edu_qua_certificate4':
            certificate = document.get_document(constants.ADDITIONAL_EDUC_QUALIFICATION4)
        elif education_qualifications == 'edu_qua_certificate5':
            certificate = document.get_document(constants.ADDITIONAL_EDUC_QUALIFICATION5)
        del(document)
        return render(request, 'signup/educational_upload.html', locals())
    else:
        return HttpResponse('Access forbidden')


def fetch_resources(uri, rel):
    '''
    Loading image while converting into pdf and gave to link_callback
    '''
    if uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
        logger.info(
            logme('getting media url for generating pdf', request)
        )
    elif uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.LOADING_STATIC_FOR_PDF, uri.replace(
            settings.STATIC_URL, ""))
        logger.info(
            logme('getting static url for generating pdf', request)
        )
    return path


def preview_pdf_attachment(username):
    '''
    Generating PDF File and adding attachement to mail to send Preview
    '''
    user_obj = User.objects.get(username=username)
    user_profile = UserProfile.objects.get(user=user_obj)
    user_documents = UploadDocuments.objects.filter(user_profile=user_profile)
    filename = user_profile.first_name
    filename = filename+".pdf"
    advisor = Advisor.objects.get(user_profile=user_profile)
    communication_email = request.user.profile.email
    if user.profile.communication_email_id == 'secondary':
        communication_email = request.user.profile.secondary_email
    question_list = json.loads(advisor.questions)
    context1 = {
        'user': user_obj,
        'user_documents': user_documents,
        'user_profile': user_profile,
        'advisor': advisor,
        'questions': question_list
    }
    template = get_template('signup/preview.html')
    html = template.render(context1)
    filee = open('test.pdf', "w+b")
    pisaStatus = pisa.CreatePDF(
        html.encode('utf-8'),
        dest=filee,
        encoding='utf-8',
        link_callback=fetch_resources
    )
    filee.seek(0)
    pdf = base64.b64encode(filee.read())
    filee.close()
    pdf_attachement = {
        'type': 'application/pdf',
        'content': pdf,
        'name': filename
    }
    context_det = {"name": user_profile.first_name}
    logger.info(
        logme(
            'generated pdf from preview html and attached to the advisor email',
            request
        )
    )
    send_mandrill_email_with_attachement(
        'profile-completed',
        [communication_email],
        pdf_attachement, context_det
    )


def onchange_save_field(request):
    '''
    Onchange saving userprofile details except questions
    '''
    if request.method == 'POST':
        field_name = request.POST['name']
        username = request.POST['username']
        value_un_secure = request.POST.get('value', None)
        value = clean_text(value_un_secure)
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)
        advisor_details = Advisor.objects.get(user_profile=user_profile)
        try:
            if field_name == 'birthdate':
                #  changing birtdate from dd-mm-yyyy to yyyy-mm-dd
                value = datetime.datetime.strptime(value, '%d-%m-%Y').strftime('%Y-%m-%d')
                setattr(user_profile, field_name, value)
                user_profile.save()
            if field_name == 'first_name' or field_name == 'last_name':
                setattr(user, field_name, value)
                setattr(user_profile, field_name, value)
                user.save()
                user_profile.save()
            elif field_name == 'issued_on' or field_name == 'passport_valid_upto':
                value = value.split('-')[2] + "-"+value.split('-')[1] + "-"+value.split('-')[0]
                setattr(user_profile, field_name, value)
                user_profile.save()
            elif field_name == 'practice_country':
                country_obj = Country.objects.get(name=value)
                setattr(advisor_details, field_name, country_obj)
                advisor_details.save()
            elif (field_name == 'sebi_number' or field_name == 'irda_number'
                or field_name == 'amfi_number'
                or field_name == 'other_registered_number'
                or field_name == 'other_registered_organisation'):
                    setattr(advisor_details, field_name, value)
                    is_crisil_valid = check_crisil_advisor(advisor_details)
                    if is_crisil_valid:
                        advisor_details.crisil_application_status = constants.CRISIL_EXPIRED_BY_USER
                        advisor_details.is_crisil_verified = False
                    advisor_details.save()
            elif (field_name == 'sebi_expiry_date'
                or field_name == 'amfi_expiry_date'
                or field_name == 'irda_expiry_date'
                or field_name == 'other_expiry_date'):
                if value != '':
                    value = datetime.datetime.strptime(value, '%d-%m-%Y').strftime(
                        '%Y-%m-%d')
                else:
                    value = None
                setattr(advisor_details, field_name, value)
                is_crisil_valid = check_crisil_advisor(advisor_details)
                if is_crisil_valid:
                    if (field_name == 'sebi_expiry_date' or
                        field_name == 'irda_expiry_date' or
                        field_name == 'amfi_expiry_date' or
                        field_name == 'other_expiry_date'):
                            advisor_details.crisil_application_status = \
                                constants.CRISIL_EXPIRED_BY_USER
                            advisor_details.is_crisil_verified = False
                advisor_details.save()
            elif field_name == 'mobile':
                value = value.replace(" ", "")
                setattr(user_profile, field_name, value)
                user_profile.save()
                is_crisil_valid = check_crisil_advisor(advisor_details)
                if is_crisil_valid:
                    advisor_details.crisil_application_status = \
                        constants.CRISIL_EXPIRED_BY_USER
                    advisor_details.is_crisil_verified = False
                advisor_details.save()
            elif (field_name == 'street_name' or field_name == 'address'
                or field_name == 'landmark' or field_name == 'locality'
                or field_name == 'city' or field_name == 'pincode'
                or field_name == 'state' or field_name == 'country'):
                    setattr(user_profile, field_name, value)
                    if request.user.profile.primary_communication == 'home':
                        is_crisil_valid = check_crisil_advisor(advisor_details)
                        if is_crisil_valid:
                            advisor_details.crisil_application_status = \
                                constants.CRISIL_EXPIRED_BY_USER
                            advisor_details.is_crisil_verified = False
                        advisor_details.save()
                    user_profile.save()
            elif (field_name == 'company_address1' or field_name == 'company_address2'
                or field_name == 'company_landmark' or field_name == 'company_locality'
                or field_name == 'company_city' or field_name == 'company_pincode'
                or field_name == 'company_state' or field_name == 'company_country'):
                    setattr(user_profile, field_name, value)
                    if request.user.profile.primary_communication == 'office':
                        is_crisil_valid = check_crisil_advisor(advisor_details)
                        if is_crisil_valid:
                            advisor_details.crisil_application_status =\
                                constants.CRISIL_EXPIRED_BY_USER
                            advisor_details.is_crisil_verified = False
                        advisor_details.save()
                    user_profile.save()
            elif field_name == 'is_submitted_all':
                if value == 'false':
                    value = False
                else:
                    value = True
                setattr(advisor_details, field_name, value)
                advisor_details.save()
            elif field_name == 'additional_qualification':
                documents = UploadDocumentsFunctions(request, user_profile)
                if not constants.ADDITIONAL_EDUC_QUALIFICATION1 in value:
                    upload_documents = UploadDocuments.objects.filter(
                        user_profile=user_profile,
                        documents_type=constants.ADDITIONAL_EDUC_QUALIFICATION1
                    )
                    upload_documents.delete()
                if not constants.ADDITIONAL_EDUC_QUALIFICATION2 in value:
                    upload_documents = UploadDocuments.objects.filter(
                        user_profile=user_profile, documents_type=constants.ADDITIONAL_EDUC_QUALIFICATION2)
                    upload_documents.delete()
                if not constants.ADDITIONAL_EDUC_QUALIFICATION3 in value:
                    upload_documents = UploadDocuments.objects.filter(
                        user_profile=user_profile,
                        documents_type=constants.ADDITIONAL_EDUC_QUALIFICATION3)
                    upload_documents.delete()
                if not constants.ADDITIONAL_EDUC_QUALIFICATION4 in value:
                    upload_documents = UploadDocuments.objects.filter(
                        user_profile=user_profile,
                        documents_type=constants.ADDITIONAL_EDUC_QUALIFICATION4)
                    upload_documents.delete()
                if not constants.ADDITIONAL_EDUC_QUALIFICATION5 in value:
                    upload_documents = UploadDocuments.objects.filter(
                        user_profile=user_profile,
                        documents_type=constants.ADDITIONAL_EDUC_QUALIFICATION5
                    )
                    upload_documents.delete()
                setattr(user_profile, field_name, value)
                user_profile.save()
                setattr(advisor_details, field_name, value)
                advisor_details.save()
            else:
                setattr(user_profile, field_name, value)
                user_profile.save()
                setattr(advisor_details, field_name, value)
                advisor_details.save()
        except:
            setattr(advisor_details, field_name, value)
            advisor_details.save()
        logger.info(
            logme('onchange %s saved successfully' % (field_name), request)
        )
        return HttpResponse("Sucessfully inserted")
    if request.method == 'GET':
        logger.info(
            logme('GET request -access forbidden for onchange field', request)
        )
        return HttpResponse("falied to insert")


def onchange_save_rera_fields(request):
    '''
    On change saving RERA fields
    '''
    if request.method == 'POST':
        advisor = Advisor.objects.get(user_profile=request.user.profile)
        field_name = request.POST['name']
        value = request.POST['value']
        if field_name == 'is_rera':
            if value == 'False':
                advisor.is_rera = False
                advisor.save()
            else:
                advisor.is_rera = True
        if field_name == 'rera_details':
            if value:
                value = '['+value+']'
                advisor.rera_details = value
            else:
                advisor.rera_details = ''
            advisor.save()
        logger.info(
            logme('onchange RERA data saved successfully', request)
        )
        return HttpResponse('sucessfully inserted')


def onchange_save_questions(request):
    '''
    On change saving userprofile first tab questions
    '''
    if request.method == 'POST':
        username = request.POST['username']
        questions = request.POST['questions']
        advisor_details = Advisor.objects.get(user_profile=request.user.profile)
        is_crisil_valid = check_crisil_advisor(advisor_details)
        if advisor_details.questions and is_crisil_valid:
            new_question_list = json.loads(questions)
            old_json = json.loads(advisor_details.questions)
            old_json_address = old_json[1]['Remark']
            if not old_json_address == new_question_list[1]['Remark']:
                if is_crisil_valid:
                    advisor_details.crisil_application_status = constants.CRISIL_EXPIRED_BY_USER
                    advisor_details.is_crisil_verified = False
        advisor_details.questions = questions
        total_clients_served, total_advisors_connected = None, None
        if request.POST.get('total_client_served', None):
            total_clients_served = request.POST.get('total_client_served', None)
        advisor_details.total_clients_served = total_clients_served
        if request.POST.get('total_advisors_connected', None):
            total_advisors_connected = request.POST.get('total_advisors_connected', None)
        advisor_details.total_advisors_connected = total_advisors_connected
        advisor_details.save()
        logger.info(
            logme('onchange saved question successfully', request)
        )
        return HttpResponse('Sucessfully Saved in database')
    if request.method == 'GET':
        logger.info(
            logme('GET request- access forbidden for onchange save questions', request)
        )
        return HttpResponse('falied to save')


def invite_advisor(request):
    '''
    Navigating to invite_advisor_details html
    '''
    MODAL_NAME = 'Invite Advisor'
    form = InviteAdvisorForm()
    logger.info(
        logme('rendered invite advisor modal', request)
    )
    return render(request, 'signup/invite_advisor_details.html', locals())


def save_invite_advisor(request):
    '''
    Inviting Advisor and Saving the Invite Advisor Details
    '''
    if request.method == 'POST':
        form = InviteAdvisorForm(request.POST)
        if form.is_valid():
            invite_obj = form.save(commit=False)
            invite_obj.referral_user_type = 'advisor'
            invite_obj.referred_by = request.user.profile
            name = request.POST['name']
            email = request.POST['email']
            invite_obj.save()
            referral_code = UserProfile.objects.get(user=request.user)
            info = 'Mail has been sent to your refferer'
            try:
                content_dist = {
                    'name': name,
                    'url': api_constants.REFERRAL_LINK+referral_code.referral_code,
                }
                mail = email
                send_mandrill_email('invite-advisor', [email], context=content_dist)
                logger.info(
                    logme('referral link sent to the referred advisor email',request)
                )
            except:
                logger.error(
                    logme('referral link failed to send to the referred advisor email',request)
                )
                return HttpResponse("Mail failure")
            logger.info(
                logme('rendered thank you page referring advisors',request)
            )
            return render(request, 'signup/thank_view.html',locals())
        logger.info(
            logme('form is not valid to refer advisor',request)
        )
        return render(request, 'signup/invite_advisor_details.html',locals())
    if request.method == 'GET':
        form = InviteAdvisorForm()
        logger.info(
            logme('rendered invite advisor modal',request)
        )
        return render(request, 'signup/invite_advisor_details.html',locals())


def crisal_id_points(request):
    '''
    On change CRISIL ID adding points
    '''
    context = RequestContext(request)
    if request.method == 'POST':
        crisal_id = request.POST['crisal_id']
        if crisal_id:
            referral_object = UserProfile.objects.get(user = request.user)
            if referral_object.referred_by:
                benificary = referral_object.referred_by.profile
                referral_points(
                    benificary,
                    referral_object,
                    constants.CRISAL_VERIFICATION
                )
                return HttpResponse('success')
            else:
                return HttpResponse('failed')
    else:
        return HttpResponse('Access forbidden')


def rate_advisor(request):
    '''
    Navigating to the advisor_rating html to rate the advisor
    '''
    # ====Setting User obj for using the user details in Post
    user = request.session.get('user')
    recaptcha_key = constants.RECAPTCHA_KEY
    if request.method == 'GET':
        logger.info(
            logme('rendered advisor rating page', request)
        )
        return render(request, 'signup/advisor_rating.html', locals())
    else:
        logger.info(
            logme('rendered advisor rating page', request)
        )
        return render(request, 'signup/advisor_rating.html', locals())


def advisor_rating(request, activation_key):
    '''
    Function save advisor rating and sends mail and sms to registered advisor,
    external advisor and member
    '''
    recaptcha_key = constants.RECAPTCHA_KEY
    if request.method == 'GET':
        title = 'Advisor Rating'
        if activation_key:
            try:
                advisor_to_rate = AdvisorRating.objects.get(
                    activation_key=activation_key)
                try:
                    is_user_exist = UserProfile.objects.filter(
                        email=advisor_to_rate.external_user.email).first()
                except Exception as e:
                    is_user_exist = True
                is_user_exist = True if is_user_exist else False
                    
                logger.info(
                    logme('activation key exists for rating advisor',request)
                )
            except ObjectDoesNotExist:
                logger.warning(
                    logme("[rate_advisor] failed because of no \
                    advisor rating object found", request)
                )
                return HttpResponse(
                    "URL is invalid/expired!!!")
            if request.user.is_authenticated():
                if request.user.profile == advisor_to_rate.advisor.user_profile:
                    logger.info(
                        logme('advisor can not rate himself', request)
                    )
                    return HttpResponse('You cannot rate yourself')
            return render(request, 'signup/advisor_rating.html', locals())
    else:
        advisor_to_rate = AdvisorRating.objects.get(
            activation_key=activation_key)
        nf = NotificationFunctions(request)
        advisor_to_rate.trust = request.POST.get('trust')
        advisor_to_rate.financial_knowledge = request.POST.get('financial')
        advisor_to_rate.communication = request.POST.get('communication')
        advisor_to_rate.advisory = request.POST.get('advisory')
        advisor_to_rate.ethics = request.POST.get('ethics')
        advisor_to_rate.customer_care = request.POST.get('customer')
        advisor_to_rate.avg_rating = request.POST.get('average')
        external_user = advisor_to_rate.external_user
        if external_user:
            if advisor_to_rate.user_type == 'advisor':
                if request.POST.get('sebi_certified'):
                    external_user.sebi_number = request.POST.get('sebi_reg_id')
                    if request.POST.get('sebi_date'):
                        external_user.sebi_expiry_date = \
                            datetime.datetime.strptime(
                                request.POST.get('sebi_date'), '%Y/%m/%d')
                if request.POST.get('amfi_certified'):
                    external_user.amfi_number = request.POST.get('amfi_reg_id')
                    if request.POST.get('amfi_date'):
                        external_user.amfi_expiry_date = \
                            datetime.datetime.strptime(
                                request.POST.get('amfi_date'), '%Y/%m/%d')
                if request.POST.get('irda_certified'):
                    external_user.irda_number = request.POST.get('irda_reg_id')
                    if request.POST.get('irda_date'):
                        external_user.irda_expiry_date = \
                            datetime.datetime.strptime(
                                request.POST.get('irda_date'), '%Y/%m/%d')
                if request.POST.get('RERA_certified'):
                    rera_data = \
                        [{"rera_registration_no":request.POST.get('RERA_reg_no'),
                            "rera_state":request.POST.get('RERA_state'),
                            "rera_expire_date":request.POST.get('RERA_date')
                        }]
                    external_user.rera_details = json.dumps(rera_data)
                if request.POST.get('other_certified'):
                    external_user.other_registered_organisation = request.POST.get(
                        'other_reg_name')
                    external_user.other_registered_number = request.POST.get(
                        'other_reg_id')
                    if request.POST.get('other_date'):
                        external_user.other_certificate_expiry_date = \
                            datetime.datetime.strptime(
                                request.POST.get('other_date'), '%Y/%m/%d'
                            )
                peer_name = external_user.name
                external_user.save()
                communication_email = advisor_to_rate.advisor.user_profile.email
                if advisor_to_rate.advisor.user_profile.communication_email_id == \
                    'secondary':
                    communication_email = \
                        advisor_to_rate.advisor.user_profile.secondary_email
                context_dict = {
                    'advisor_name': advisor_to_rate.advisor.user_profile.first_name,
                    'Peer_name': peer_name,
                    'url': settings.DEFAULT_HOST + "/dashboard/"
                }
                send_mandrill_email(
                    'ABOTMI_11',
                    [external_user.email, ],
                    context=context_dict,
                )
            else:
                advisor_to_rate.feedback = request.POST.get('feedback')
                external_user.save()
                context_dict = {
                    'advisor_name':
                    advisor_to_rate.advisor.user_profile.first_name,
                    'Peer_name': external_user.name,
                    'url': settings.DEFAULT_HOST + "/dashboard/"
                }
        else:
            if advisor_to_rate.user_type == 'member':
                advisor_to_rate.feedback = request.POST.get('feedback')
            communication_email = advisor_to_rate.advisor.user_profile.email
            if advisor_to_rate.advisor.user_profile.communication_email_id == 'secondary':
                communication_email = advisor_to_rate.advisor.user_profile.secondary_email
            peer_name = advisor_to_rate.existing_user_profile.first_name
            context_dict = {
                'advisor_name':
                advisor_to_rate.advisor.user_profile.first_name,
                'peer_name': peer_name,
                'url': settings.DEFAULT_HOST + "/dashboard/"
            }
            send_mandrill_email(
                'ABOTMI_09',
                [advisor_to_rate.existing_user_profile.email, ],
                context=context_dict,
            )
            logger.info(
                logme('email sent to the rated advisor', request)
            )
            nf_type = RANK_RES if advisor_to_rate.user_type == 'advisor' else RATE_RES
            nf.save_notification(
                notification_type=nf_type,
                sender=advisor_to_rate.existing_user_profile,
                receive=advisor_to_rate.advisor.user_profile
            )
        advisor_to_rate.activation_key = ''
        advisor_to_rate.save()
        del(nf)
        logger.info(
            logme('advisor rated successfully', request)
        )
        return HttpResponse("success")


def invite_to_rate(request):
    '''
    Navigating to invite_to_rate html
    '''
    logger.info(
        logme('opened invite to rate modal',request)
    )
    return render(request, 'signup/invite_to_rate.html', locals())


def invite_advisor_to_rate(request):
    '''
    Sending Rating link to Invited Emails to Rate
    '''
    if request.method =='POST':
        salt = hashlib.sha1(str(random.random())).hexdigest()[:random.randrange(5)]
        activation_key = hashlib.md5(request.user.username).hexdigest() + salt
        user_profile = UserProfile.objects.filter(email=request.POST['email'])
        if user_profile:
            AdvisorRating(
                advisor=request.user.profile.advisor,
                activation_key=activation_key,
                existing_user_profile=user_profile[0],
            ).save()
        else:
            external_user, created = ExternalUser.objects.get_or_create(
                email=request.POST['email'])
            if created:
                external_user.name = request.POST.get('name')
                external_user.phone = request.POST.get('phone')
                external_user.save()
            AdvisorRating(
                advisor=request.user.profile.advisor,
                activation_key=activation_key,
                external_user=external_user,
            ).save()

        user_data = {}
        user_data['name'] = request.POST['name']
        user_data['url'] = settings.DEFAULT_HOST + \
            '/signup/advisor_rating' + activation_key
        send_mandrill_email(
            'inviting_advisor_to_rate',
            [request.POST['email']],
            context=user_data)
        logger.info(
            logme('invitation email sent to advisor to rate', request)
        )
        return HttpResponse('mail sent')
    else:
        logger.info(
            logme('rendered invite advisor details modal', request)
        )
        return render(
            request, 'signup/invite_advisor_details.html', locals())


def refer_member(request):
    '''
    Reffering member
    '''
    form = memberreferform()
    if request.method == 'POST':
        form = memberreferform(request.POST)
        if form.is_valid():
            content = {}
            content['referrer'] = request.user.profile.first_name
            content['url'] = "www.northfacing.in/login/?referral_code={0}".format(
                request.user.profile.referral_code)
            content['name'] = form.cleaned_data['name']
            try:
                UserReferral(
                    name=form.cleaned_data['name'],
                    email=form.cleaned_data['email'],
                    phone=form.cleaned_data['phone'],
                    referred_by=request.user
                ).save()
                send_mandrill_email(
                    'refer_member',
                    [form.cleaned_data['email'], ],
                    context=content)
                logger.info(
                    logme('invitation email sent to member to rank', request)
                )
                return HttpResponse('success')
            except:
                logger.info(
                    logme('referral to rank for member failed', request)
                )
                return HttpResponse(
                    'Please contact admin at contact@reiaglobal.com')
    logger.info(
        logme('rendered member referal form', request)
    )
    return render(request, 'signup/member_referral_form.html', locals())


@login_required
def business_information(request):
    '''
    Navigating to business_information html
    '''
    title = constants.BUSINESS_INFORMATION
    user = request.user
    user_basic_details = user.profile
    if not user_basic_details.is_admin:
        user_details = user_basic_details.advisor
        if user_details.questions:
            question_list = json.loads(user_details.questions)
            if question_list[1]['Remark']:
                question_list[1]['Remark'] = question_list[1]['Remark'].replace(" ","!")
                question_list[1]['Remark'] = question_list[1]['Remark'].replace("\n","$")
        else:
            question_list = {}
        PRODUCT_NAME = settings.PRODUCT_NAME
        questions_list = question_list
        result = get_kyc_step_status(request, user, user_basic_details, user_details)
        crisil_certificate_valid = check_crisil_advisor(user_details)
        # IP Recognisation
        ip_details = request.session['ip_info']
        user_agent_country = ip_details.get("country", constants.REGION_DEFAULT)
        if user_agent_country == constants.REGION_DEFAULT:
            question1 = 'Are you a Realtor ?'
            question2 = 'Do you have an infrastructure or will you be able to create\
            an infrastructure to handle the clients ?'
            question3 = 'Are you associated with any Financial Organisation ?'
            question4 = 'Will you be interested to undergo any training program about\
            real estate investment advisory ?'
            currency = 'Rs'
            covert_currency1 = "50,000"
            covert_currency2 = "10,00,000"
        else:
            question1 = 'Are you a financial advisor or digital asset advisor ?'
            question2 = 'Do you have an infrastructure or will you be able to create\
            an infrastructure to handle the clients ?'
            question3 = 'Are you associated with any financial organization ?'
            question4 = 'Will you be interested to undergo any training program about\
            digital asset investments and advisory ?'
            currency = '$'
            covert_currency1 = " 50,000"
            covert_currency2 = "1,000,000"
        logger.info(
            logme('redirected to business information page',request)
        )
        return render(request, 'signup/business_information.html',  locals())
    else:
        logger.info(
            logme('admin tried to navigate to business information page',request)
        )
        return HttpResponse("This Page is not For Admin. \
            Login as user <a href='%s'>Click here to return home</a>\
            </h1>" %settings.LOGIN_REDIRECT_URL
        )


@login_required
def submit_eipv_doc(request):
    '''
    Getting Uploaded EIPV Documents
    '''
    req_type = request.POST.get('req_type', None)
    title = constants.EIPV
    recaptcha_key = constants.RECAPTCHA_KEY
    user = request.user
    user_profile = user.profile
    advisor = user_profile.advisor
    submit_documents_mandatory = 0
    personal_info = 0
    m_eipv_face_present = None
    m_eipv_aadhaar_present = None
    m_eipv_passport_present = None
    m_eipv_idcard_present = None
    m_eipv_pancard_present = None
    m_eipv_signature_present = None
    email_signup = None
    # IP Recognisation
    ip_details = request.session['ip_info']
    user_agent_country = ip_details.get("country", constants.REGION_DEFAULT)
    upload_documents = UploadDocuments.objects.filter(user_profile=user_profile)
    country_list = Country.objects.all()
    if user_profile.source_media == constants.SIGNUP_WITH_EMAIL:
        email_signup = True
    eipv_face_capture = upload_documents.filter(
        documents_type='eipv_face_capture').first()
    if eipv_face_capture:
        m_eipv_face_present = True
    eipv_idcard = upload_documents.filter(documents_type='eipv_idcard').first()
    if eipv_idcard:
        m_eipv_idcard_present = True
    if user_profile.first_name and user_profile.mobile and user_profile.email and \
        user_profile.address and user_profile.city and user_profile.pincode:
            personal_info = 0
    user_status = user_profile.status

    if req_type == "mobile":
        data = {
            'email_signup_present': email_signup,
            'eipv_face_capture': m_eipv_face_present,
            'eipv_aadhaar_present': m_eipv_aadhaar_present,
            'eipv_pancard_present': m_eipv_pancard_present,
            'eipv_passport_present': m_eipv_passport_present,
            'eipv_idcard_present': m_eipv_idcard_present,
            'eipv_signature_present': m_eipv_signature_present,
            'person_info_present': personal_info,
            'name': user_profile.first_name,
            'mobile': user_profile.mobile,
            'email': user_profile.email,
            'ipv_status': advisor.ipv_status
        }
        return data
    logger.info(
        logme('redirected to EIPV page', request)
    )
    return render(request, 'signup/eipv_steps_form.html', locals())


def ekyc_step5(request):
    '''
    Description: Function for navigating to submit documents page
    '''
    title = 'Education'
    user = request.user
    user_profile = user.profile
    advisor = user_profile.advisor
    educational_details = None
    certification_details = None
    result = get_kyc_step_status(request, user, user_profile, advisor)
    document = UploadDocumentsFunctions(request, user_profile)
    user_educational_doc = document.get_document('educational_doc', many=True)
    education_obj = EducationAndCertificationDetails.objects.filter(
        user_profile=user_profile).first()
    if education_obj:
        educational_details = json.loads(education_obj.educational_details)[0]
        if education_obj.certification_details:
            certification_details = json.loads(education_obj.certification_details)
    context_dict = {
        'title': title,
        'educational_details': educational_details,
        'certification_details': certification_details,
        'result': result,
        'user_educational_doc': user_educational_doc
    }
    if request.is_ajax():
        if request.method == 'POST':
            page_type = request.POST.get('page_type', None)
            if page_type == 'education_edit_modal':
                template_name = 'my_identity/edit_education.html'
                del(context_dict['certification_details'])
                del(context_dict['result'])
            else:
                del(context_dict['educational_details'])
                del(context_dict['user_educational_doc'])
                del(context_dict['result'])
                template_name = 'my_identity/edit_certification.html'
    else:
        template_name = 'signup/ekyc/ekyc_step5.html'
    return render(request, template_name, context=context_dict)


@allow_advisor
def personal_information(request):
    '''
    Navigating to personal_information html
    '''
    title = constants.BUSINESS_INFORMATION
    mobileno = None
    user = request.user
    user_profile = user.profile
    advisor = user_profile.advisor
    result = get_kyc_step_status(request, user, user_profile, advisor)
    country_list = Country.objects.all().values('name')
    user_profile.is_advisor = True
    user_profile.save()
    # IP Recognisation
    user_agent_country = get_ip_region(request)
    document = UploadDocumentsFunctions(request, user_profile)
    user_documents_indian_proof = None
    if user_agent_country == constants.REGION_IN:
        user_documents_indian_proof = document.get_document(constants.PAN_CARD, many=True)
    highest_qualification_status = document.check_document(
        constants.HIGHEST_QUALIFICATION)
    # deleting object
    del(document)
    LOGIN_URL = settings.LOGIN_URL
    if advisor.questions:
        question_list = json.loads(advisor.questions)
        if question_list[1]['Remark']:
            question_list[1]['Remark'] = question_list[1]['Remark'].replace(" ", "!")
            question_list[1]['Remark'] = question_list[1]['Remark'].replace("\n", "$")
    else:
        question_list = {}
    questions_list = question_list
    if user_agent_country == constants.REGION_DEFAULT:
        question1 = 'Are you a Realtor ?'
        question2 = 'Do you have an infrastructure or will you be able to create\
        an infrastructure to handle the clients ?'
        question3 = 'Are you associated with any Financial Organisation ?'
        question4 = 'Will you be interested to undergo any training program about\
        real estate investment advisory ?'
        currency = 'Rs'
        covert_currency1 = "50,000"
        covert_currency2 = "10,00,000"
    else:
        question1 = 'Are you a financial advisor or digital asset advisor ?'
        question2 = 'Do you have an infrastructure or will you be able to create\
        an infrastructure to handle the clients ?'
        question3 = 'Are you associated with any financial organization ?'
        question4 = 'Will you be interested to undergo any training program about\
        digital asset investments and advisory ?'
        currency = '$'
        covert_currency1 = "50k+"
        covert_currency2 = "1m+"
    digi_links = DigitalFootPrint.objects.filter(user_profile=user_profile)
    '''
    Advisor Practice Details Json
    '''
    advisor_practice_details = advisor.practice_details if advisor.practice_details else None
    if advisor_practice_details is None and advisor.practice_country \
            and advisor.practice_city and advisor.practice_location:
            advisor_practice_details = get_practice_contry_details_json(
                advisor)
            advisor_practice_details_json = json.loads(
                advisor_practice_details)
    if advisor_practice_details is None:
        advisor_practice_details = [
            {
                "practice_country": "select",
                "practice_city": "",
                "practice_location": "",
                "practice_pincode": ""
            }
        ]
        advisor_practice_details = json.dumps(advisor_practice_details)
    if advisor_practice_details and advisor_practice_details != "":
        advisor_practice_details_json = json.loads(advisor_practice_details)
    logger.info(
        logme('redirected to personal information page', request)
    )
    return render(request, 'signup/personal_information.html', locals())


def download_advisor_profile(request):
    '''
    Downloding advisor profile as a PDF
    '''
    user = User.objects.get(username=request.user.username)
    filename = user.first_name
    user_profile = UserProfile.objects.get(user=request.user)
    advisor = Advisor.objects.get(user_profile=request.user.profile)
    questions = advisor.questions
    financial_instruments = advisor.financial_instruments
    user_documents = UploadDocuments.objects.filter(user_profile=request.user.profile)
    my_sale_accomplishments = advisor.my_sales
    if user_profile.additional_qualification:
        additional_qualification_list = json.loads(user_profile.additional_qualification)
    else:
        additional_qualification_list = ''
    if financial_instruments:
        financial_instruments = json.loads(financial_instruments)
    else:
        financial_instruments = ''
    office_address =''
    if questions:
        questions = json.loads(questions)
        if questions[1]['Remark']:
            office_address = json.loads(advisor.questions)[1]['Remark'].replace("!"," ")
            office_address = office_address.replace("$","\n")
            office_address = office_address
    else:
        questions = ''
    rera_result = ''
    if advisor.is_rera and advisor.rera_details:
        rera_result = json.loads(advisor.rera_details)
    dsa_result = ''
    if advisor.dsa_details:
        dsa_result = json.loads(advisor.dsa_details)
    advisor_rate_invites = AdvisorRating.objects.filter(
        advisor=request.user.profile.advisor,
        user_type='advisor'
    )
    total_advisor_rates = 0
    peer_rating = advisor_rate_invites.exclude(
                avg_rating__lte=0.0).aggregate(
                Avg('avg_rating'))['avg_rating__avg']
    advisor_member_ratings = AdvisorRating.objects.filter(
        advisor=request.user.profile.advisor,
        user_type='member'
    )

    total_member_ranks = 0
    ranked_invites = 0
    member_rating = 0

    if advisor_member_ratings:
        total_member_ranks += advisor_member_ratings.count()
        ranked_invites += advisor_member_ratings.exclude(
            avg_rating__lte=0.0).count()
        if advisor_member_ratings.exclude(avg_rating__lte=0.0):
            new_rating = (
                member_rating + advisor_member_ratings.exclude(
                    avg_rating__lte=0.0).aggregate(Avg(
                        'avg_rating'))['avg_rating__avg']
            )
            if new_rating > member_rating and member_rating != 0:
                member_rating = new_rating / 2
            else:
                member_rating = new_rating

    '''
        Displaying advisor recent post and comments in profile page
    '''
    '''-- Posts --'''

    WP_USER_ID = request.user.profile.advisor.wordpress_user_id
    url      = settings.ICORE_API_URL+'/posts/author/'+ WP_USER_ID
    headers  = {'Content-Type': 'application/json'}
    req      = requests.get(url, headers=headers)
    json_res = req.content.encode('UTF-8')
    recent_post = json.loads(json_res)
    three_recent_posts = []
    for post in recent_post[::-1]:
        three_recent_posts.append(post)
    recent_post_length = len(recent_post)

    '''-- Comments --'''
    url_comment = settings.ICORE_API_URL+'/comments/'+request.user.profile.email
    req_comment = requests.get(url_comment, headers=headers)
    json_res_comment = req_comment.content.encode('UTF-8')
    recent_comments = json.loads(json_res_comment)
    recent_comments_length = len(recent_comments)
    total_count = recent_post_length + recent_comments_length
    comment_count = 0
    if(recent_post_length < 3):
        comment_count = 3-recent_post_length

    server_url = settings.DEFAULT_DOMAIN_URL
    feedbacks = None
    feedbacks = AdvisorRating.objects.filter(
        advisor=advisor,
        user_type='member').exclude(feedback__isnull=True)
    # Fetching all Company profiles who all are approved
    company_obj = CompanyAdvisorMapping.objects.filter(
        advisor_user_profile=request.user.profile,
        status=constants.APPROVED).values('company_user_profile')
    company_profile = UserProfile.objects.filter(id__in=company_obj)
    aprroved_companies = AffiliatedCompany.objects.filter(
        user_profile__in=company_profile)
    # Giving Position to the Advisor according to their gole
    advisor_level = ''
    clients_level = ''
    level_advisor = ''
    advisor = request.user.profile.advisor
    # Fetching Referred registered advisors
    refered_members = Advisor.objects.filter(
        is_register_advisor=True,
        user_profile__referred_by=request.user).count()
    # Fetching count who rated minimum avg rating with 3.0
    rating_count = AdvisorRating.objects.filter(
        avg_rating__gte=constants.MINIMUM_AVG_RATING,
        advisor=advisor,
        user_type="advisor").count()
    # Fetching count who ranked minimum avg rating with 3.0
    ranking_count = AdvisorRating.objects.filter(
        avg_rating__gte=constants.MINIMUM_AVG_RATING,
        advisor=advisor,
        user_type="member").count()
    # if advisor refer 100 registered advisors than that advisor is CONNECTED
    if refered_members >= constants.FIRST_LEVEL_MINIMUM_ADVISOR_COUNT \
        and refered_members <= constants.SECOND_LEVEL_MINIMUM_ADVISOR_COUNT:
            advisor_level = constants.CONNECTED
    # if advisor refer >=500 registered advisors than that advisor is WELL_CONNECTED
    if refered_members >= constants.SECOND_LEVEL_MINIMUM_ADVISOR_COUNT:
        advisor_level = constants.WELL_CONNECTED
        level_advisor = constants.WELL_CONNECTED
    # if advisor rated by 500+ advisors with minimum avg 3.0 than that advisor is HIGHLY_CONNECTED
    if rating_count >= constants.SECOND_LEVEL_MINIMUM_ADVISOR_COUNT:
        advisor_level = constants.HIGHLY_CONNECTED
    # if advisor add >=500 members with minimum advisors avg rating 3.0 and rated advisors are 500+ than that advisor is TRUSTED
    if rating_count >= constants.SECOND_LEVEL_MINIMUM_ADVISOR_COUNT \
        and refered_members >= constants.SECOND_LEVEL_MINIMUM_ADVISOR_COUNT:
            advisor_level = constants.TRUSTED
    # if advisor is ranked by >=500 members with minimum 3.0 rating then that advisor is LARGE_CLIENT_BASED
    if ranking_count >= constants.SECOND_LEVEL_MINIMUM_ADVISOR_COUNT:
        clients_level = constants.LARGE_CLIENT_BASED
    # if advisor is HIGHLY_CONNECTED and LARGE_CLIENT_BASED than that advisor is MOST_TRUSTED
    if rating_count >= constants.SECOND_LEVEL_MINIMUM_ADVISOR_COUNT \
        and clients_level == constants.LARGE_CLIENT_BASED:
            clients_level = constants.MOST_TRUSTED
    # if advisor is MOST_TRUSTED and CRISIL verified than that advisor is TEA
    if clients_level == constants.MOST_TRUSTED:
        if request.user.profile.advisor.is_crisil_verified:
            advisor_level = constants.TRUSTED_ECONOMIC_ADVISOR
    if user.profile.picture:
        profile_pic = get_binary_image(user_profile)
    else:
        profile_pic = ''
    context = {
        'user'      : user,
        'questions' : questions,
        'office_address' : office_address,
        'additional_qualification_list' : additional_qualification_list,
        'financial_instruments' : financial_instruments,
        'user_documents' : user_documents,
        'rera_result' : rera_result,
        'dsa_result' :dsa_result,
        'peer_rating' : peer_rating,
        'member_rating':member_rating,
        'recent_post' :recent_post,
        'server_url' : server_url,
        'three_recent_posts' : three_recent_posts,
        'feedbacks': feedbacks,
        'my_sale_accomplishments' : my_sale_accomplishments,
        'recent_comments' : recent_comments,
        'recent_post' : recent_post,
        'comment_count' : comment_count,
        'aprroved_companies': aprroved_companies,
        'advisor_level': advisor_level,
        'clients_level' : clients_level,
        'level_advisor' : level_advisor,
        'profile_pic': profile_pic
    }
    response = generate_pdf(request, "signup/profile_pdf.html", context, True, filename)
    logger.info(
        logme('converted advisor profile to pdf for download',request)
    )
    return response


@login_required
def onchange_save_nationality(request):
    '''
    save nationality identity number in the user profile table
    when on change the pan or passport number.
    '''
    if request.method == 'POST':
        doc_no = request.POST['doc_no']
        doc_type = request.POST['doc_type']
        user_profile_obj = UserProfile.objects.get(user =  request.user)
        if doc_type == "pan_card":
            user_profile_obj.pan_no = doc_no
        elif doc_type == "passport":
            user_profile_obj.passport_no = doc_no
        user_profile_obj.save()
        ip_details = request.session['ip_info']
        user_agent_country = ip_details.get("country", constants.REGION_DEFAULT)
        # fetching all documents which are mandatory
        submit_documents_mandatory = 0
        if request.user.profile.advisor.is_document_submited:
            if request.user.profile.pan_no or request.user.profile.passport_no:
                submit_documents_mandatory = 1

        if request.user.profile.advisor.is_document_submited:
            if request.user.profile.pan_no or request.user.profile.passport_no:
                if user_agent_country == constants.REGION_IN:
                    if request.user.profile.mobile:
                        mobile_number=request.user.profile.mobile
                        sms_status = get_sms_status(request.user.profile)
                        if sms_status == True:
                            # sending sms to user
                            message = 'Dear '+request.user.profile.first_name+\
                                ' ('+request.user.profile.registration_id+'), \
                                Registration completed. Our verification team will \
                                contact you shortly.'
                            sms_response = send_sms_alert(
                                mobile_number=mobile_number,message_template=message)
                communication = request.user.profile.communication_email_id
                if communication == 'primary':
                    user_email = request.user.profile.email
                else:
                    user_email = request.user.profile.secondary_email
        logger.info(
            logme('saved %s '%(doc_type),request)
        )
        return HttpResponse(submit_documents_mandatory)
    if request.method == 'GET':
        logger.info(
            logme('GET request - access forbidden to save passport/pan',request)
        )
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)


def check_and_save_secondary_email(request):
    '''
    Checking Email is exists as Primary/Secondary Email in Database
    '''
    value = request.POST.get('value', None)
    if request.user.profile.secondary_email == value:
        email_exists = constants.OLD_SECONDARY_EMAIL
    else:
        existing_email_id = UserProfile.objects.filter(
            (Q(email=value) | Q(secondary_email=value)) & Q(is_advisor=True))
        email_exists = 1
        if not existing_email_id:
            email_exists = 0
    logger.info(
        logme('validation - secondary email exists %s : %s'%(value, (
            'Yes' if email_exists == 1 else 'No')),request)
    )
    return HttpResponse(email_exists)


def preview_pdf_kyc(request):
    '''
    Navigating to profile_pdf_kyc html
    Description: Showing Preview before downloading profile as PDF
    '''
    context = RequestContext(request)
    user_documents_list = []
    if request.method == 'GET':
        user = User.objects.get(username=request.user.username)
        user_profile = UserProfile.objects.get(user=user)
        user_documents = UploadDocuments.objects.filter(user_profile=user_profile)
        filename = user_profile.first_name
        advisor = Advisor.objects.get(user_profile=user_profile)
        if advisor.questions:
            business_information_json = json.loads(advisor.questions)
        else:
            business_information_json = None
        financial_instruments_data = advisor.financial_instruments
        financial_instruments = []
        if financial_instruments_data:
            financial_instruments = json.loads(advisor.financial_instruments)
        rera_data = advisor.rera_details
        dsa_data = advisor.dsa_details
        rera_result= []
        if rera_data:
            rera_result = json.loads(advisor.rera_details)
        dsa_details= []
        if dsa_data:
            dsa_details = json.loads(advisor.dsa_details)
        for i in user_documents:
            user_documents_list.append(i.documents_type)
        if user_profile.additional_qualification:
            additional_qualification_list = json.loads(
                user_profile.additional_qualification)
        else:
            additional_qualification_list = ''
        if business_information_json :
            if business_information_json[1]['Remark']:
                office_address = business_information_json[1]['Remark'].replace("!"," ")
                office_address = office_address.replace("$","\n")
                office_address = office_address
            else:
                office_address = ''
        else:
            office_address = ''
        context = {
            'user': user,
            'user_documents': user_documents,
            'user_profile': user_profile,
            'advisor': advisor,
            'additional_qualification_list': additional_qualification_list,
            'questions': business_information_json,
            'office_address':   office_address,
            'user_documents_list': user_documents_list,
            'business_information_json': business_information_json,
            'financial_instruments': financial_instruments,
            'rera_result': rera_result,
            'dsa_details': dsa_details
        }
        response = generate_pdf(
            request, "signup/profile_pdf_kyc.html", context, False, filename)
        logger.info(
            logme('converted preview kyc to pdf', request)
        )
        return response


def add_sales_acomplishments(request):
    '''
    Descrption:Advisor is Adding Accomplishments from Advisor Profile/My Track.
    '''
    if request.method == 'POST':
        advisor = Advisor.objects.get(user_profile = request.user.profile)
        if request.POST['sales_content']:
            advisor.my_sales = request.POST['sales_content']
            advisor.save()
            logger.info(
                logme('onchange saved sales accomplishments', request)
            )
            return HttpResponse('success')
        else:
            logger.error(
                logme('onchange failed to save sales accomplishments', request)
            )
            return HttpResponse('failed')
    else:
        logger.info(
            logme('GET request - access forbidden to save sales accomplishments', request)
        )
        return HttpResponse('Access Forbidden')


def edit_profile(request):
    '''
    Navigting to edit_profile html to Edit users details
    '''
    if request.method == "POST":
        user = request.user
        user_profile = user.profile
        advisor = user_profile.advisor
        doc_profile_picture = UploadDocuments.objects.filter(
            user_profile=user_profile, documents_type="Profile Picture")
        if doc_profile_picture:
            doc_profile_picture = doc_profile_picture.first()
        financial_instruments = advisor.financial_instruments
        if not financial_instruments:
            financial_instruments_json = None
        if financial_instruments == None or not financial_instruments:
            financial_instruments = '[{"instruments":"select","experience":""}]'
        if financial_instruments:
            financial_instruments_json = json.loads(financial_instruments)
            all_financial_instrument = constants.ALL_FINANCIAL_INSTRUMENT
        if advisor.is_rera and advisor.rera_details:
            rera_result = json.loads(advisor.rera_details)
        if advisor.dsa_details:
            dsa_result = json.loads(advisor.dsa_details)
        mobileno = None
        if user_profile.mobile:
            mobile_number = user_profile.mobile
        accomplishments = ''
        if advisor.my_sales:
            accomplishments = advisor.my_sales
        logger.info(
            logme('opened edit profile modal', request)
        )
        return render(request, "signup/edit_profile.html", locals())
    else:
        logger.info(
            logme('GET request - access forbidden to open edit profile modal', request)
        )
        return HttpResponse('Access forbidden')


def save_profile(request):
    '''
    Saving the Edit Profile form
    '''
    context = RequestContext(request)
    if request.method == 'POST':
        user = User.objects.get(username = request.user.username)
        # Auth User ---
        user.first_name = request.POST['first_name']
        user.last_name  = request.POST['last_name']
        user.save()
        # Auth User ---
        # User Profile ---
        user_profile = UserProfile.objects.get(user=user)
        advisor_details = Advisor.objects.get(user_profile = user_profile)
        old_rera_json = advisor_details.rera_details
        old_dsa_json = advisor_details.dsa_details
        if not old_dsa_json:
            old_dsa_json = ''
        is_crisil_valid = check_crisil_advisor(advisor_details)
        user_profile.first_name = request.POST['first_name']
        user_profile.middle_name = request.POST['middle_name']
        user_profile.last_name  = request.POST['last_name']
        if is_crisil_valid:
            if not user_profile.mobile.replace(" ", "") == request.POST['mobile'].replace(
                " ", ""):
                advisor_details.crisil_application_status = constants.CRISIL_EXPIRED_BY_USER
                advisor_details.is_crisil_verified = False
        else:
            user_profile.mobile = request.POST['mobile']
        user_profile.locality = request.POST.get('locality','')
        user_profile.city = request.POST['city']
        user_profile.language_known = request.POST['language_known']
        user_profile.languages_known_read_write = request.POST[
            'languages_known_read_write']
        user_profile.my_belief = request.POST['my_belief']
        user_profile.qualification = request.POST['highest_qualification']
        user_profile.year_passout = request.POST['year_passout']
        user_profile.college_name = request.POST['college_name']
        user_profile.save()
        # User Profile ---
        # Advisor Details ----
        old_sebi_number = ''
        old_irda_number = ''
        old_amfi_number = ''
        old_other_registered_organisation = ''
        old_other_registered_number = ''
        sebi_number = ''
        irda_number = ''
        amfi_number = ''
        other_organisation = ''
        other_registered_number = ''
        if advisor_details.sebi_number:
            old_sebi_number = advisor_details.sebi_number
        if advisor_details.irda_number:
            old_irda_number = advisor_details.irda_number
        if advisor_details.amfi_number:
            old_amfi_number = advisor_details.amfi_number
        if advisor_details.other_registered_organisation:
            old_other_registered_organisation = advisor_details.other_registered_organisation
        if advisor_details.other_registered_number:
            old_other_registered_number = advisor_details.other_registered_number
        if request.POST.get('sebi_registration_no', None):
            sebi_number = request.POST['sebi_registration_no']
        if request.POST.get('irda_registration_no', None):
            irda_number = request.POST['irda_registration_no']
        if request.POST.get('amfi_registration_no', None):
            amfi_number = request.POST['amfi_registration_no']
        if request.POST.get('other_organisation', None):
            other_organisation = request.POST['other_organisation']
        if request.POST.get('other_registration_no', None):
            other_registered_number = request.POST['other_registration_no']
        sebi_expiry_date = None
        amfi_expiry_date = None
        irda_expiry_date = None
        other_expiry_date = None
        if request.POST['sebi_expiry_date']:
            sebi_expiry_date = datetime.datetime.strptime(
                request.POST['sebi_expiry_date'], '%d-%m-%Y').strftime('%Y-%m-%d')
        if request.POST['amfi_expiry_date']:
            amfi_expiry_date = datetime.datetime.strptime(
                request.POST['amfi_expiry_date'], '%d-%m-%Y').strftime('%Y-%m-%d')
        if request.POST['irda_expiry_date']:
            irda_expiry_date = datetime.datetime.strptime(
                request.POST['irda_expiry_date'], '%d-%m-%Y').strftime('%Y-%m-%d')
        if request.POST['other_expiry_date']:
            other_expiry_date = datetime.datetime.strptime(
                request.POST['other_expiry_date'], '%d-%m-%Y').strftime('%Y-%m-%d')
        # Changing CRISIL certificate to expired when advisor try to change IRDA or SEBI Details after getting CRISIL Certificate
        if is_crisil_valid:
            if (not old_sebi_number == sebi_number
                or not old_irda_number == irda_number
                or not old_amfi_number == amfi_number
                or not old_other_registered_number == other_registered_number
                or not old_other_registered_organisation == other_organisation):
                    advisor_details.crisil_application_status = constants.CRISIL_EXPIRED_BY_USER
                    advisor_details.is_crisil_verified = False
            if not advisor_details.sebi_expiry_date:
                if sebi_expiry_date:
                    advisor_details.crisil_application_status = constants.CRISIL_EXPIRED_BY_USER
                    advisor_details.is_crisil_verified = False
            else:
                if not advisor_details.sebi_expiry_date.isoformat() == sebi_expiry_date:
                    advisor_details.crisil_application_status = constants.CRISIL_EXPIRED_BY_USER
                    advisor_details.is_crisil_verified = False
            if not advisor_details.irda_expiry_date:
                if irda_expiry_date:
                    advisor_details.crisil_application_status = constants.CRISIL_EXPIRED_BY_USER
                    advisor_details.is_crisil_verified = False
            else:
                if not advisor_details.irda_expiry_date.isoformat() == irda_expiry_date:
                    advisor_details.crisil_application_status = constants.CRISIL_EXPIRED_BY_USER
                    advisor_details.is_crisil_verified = False
            if not advisor_details.amfi_expiry_date:
                if amfi_expiry_date:
                    advisor_details.crisil_application_status = constants.CRISIL_EXPIRED_BY_USER
                    advisor_details.is_crisil_verified = False
            else:
                if not advisor_details.amfi_expiry_date.isoformat() == amfi_expiry_date:
                    advisor_details.crisil_application_status = constants.CRISIL_EXPIRED_BY_USER
                    advisor_details.is_crisil_verified = False
            if not advisor_details.other_expiry_date:
                if other_expiry_date:
                    advisor_details.crisil_application_status = constants.CRISIL_EXPIRED_BY_USER
                    advisor_details.is_crisil_verified = False
            else:
                if not advisor_details.other_expiry_date.isoformat() == other_expiry_date:
                    advisor_details.crisil_application_status = constants.CRISIL_EXPIRED_BY_USER
                    advisor_details.is_crisil_verified = False

        advisor_details.sebi_number = sebi_number
        advisor_details.sebi_expiry_date = sebi_expiry_date
        advisor_details.amfi_number = amfi_number
        advisor_details.amfi_expiry_date = amfi_expiry_date
        advisor_details.irda_number = irda_number
        advisor_details.irda_expiry_date = irda_expiry_date
        advisor_details.other_registered_organisation = other_organisation
        advisor_details.other_registered_number = other_registered_number
        advisor_details.other_expiry_date = other_expiry_date
        if (request.POST['sebi_registration_no']
            or request.POST['amfi_registration_no']
            or request.POST['irda_registration_no']
            or request.POST['other_organisation']
            or request.POST['hidden_value']
            or request.POST['dsa_hidden_input_field']):
                advisor_details.is_registered_advisor = True
        advisor_details.my_promise = request.POST['my_promise']
        advisor_details.my_sales = request.POST['my_accomplishment']
        advisor_details.total_clients_served = request.POST['total_client_served']
        if not advisor_details.total_clients_served:
            advisor_details.total_clients_served = None
        advisor_details.total_advisors_connected = request.POST['advisor_is_connected_with']
        if not advisor_details.total_advisors_connected:
            advisor_details.total_advisors_connected = None
        advisor_details.financial_instruments = request.POST['hidden_input']
        advisor_details.practice_details = request.POST.get(
            'hidden_practice_details_input', None)
        if request.POST['hidden_value']:
            rera_values = '['+request.POST['hidden_value']+']'
            advisor_details.is_rera = True
        else:
            rera_values = ''
            advisor_details.is_rera = False
        advisor_details.rera_details = rera_values
        if not rera_values == old_rera_json:
            if is_crisil_valid:
                advisor_details.crisil_application_status = constants.CRISIL_EXPIRED_BY_USER
                advisor_details.is_crisil_verified = False
        if request.POST['dsa_hidden_input_field']:
            dsa_values = request.POST['dsa_hidden_input_field']
            dsa_json = '['+dsa_values+']'
        else:
            dsa_json = ''
        advisor_details.dsa_details = dsa_json
        if not dsa_json == old_dsa_json:
            if is_crisil_valid:
                advisor_details.crisil_application_status = constants.CRISIL_EXPIRED_BY_USER
                advisor_details.is_crisil_verified = False
        advisor_details.save()
        # Advisor Details ----
        logger.info(
            logme('updated profile details from edit profile modal', request)
        )
        return HttpResponse('success')
        ## ==================== User Registration ======================== ##
    if request.method == 'GET':
        logger.error(
            logme('GET request - access forbidden to save profile information', request)
        )
        return redirect(settings.LOGIN_REDIRECT_URL)


def setpassword(request):
    '''
    Resetting the Password
    GET:
        -> Checking and Delete the Activation Link and Navaigating to set_password html
    POST:
        -> Setting New Password for User
    '''
    context_dict = { 'PRODUCT_NAME' : settings.PRODUCT_NAME }
    context = RequestContext(request)
    # Setting User obj in session for using the user details in Post Request of this func
    user = request.session.get('user')
    if request.method == 'GET':
        try:
            verification = EmailVerification.objects.get(
                activation_key=request.GET['ack'])
            verification.delete()
            logger.info(
                logme('verification key esists for set password', request)
            )
        except:
            logger.info(
                logme('activation link may be wrong/expired for set password', request)
            )
            return HttpResponse("Activation link may be wrong or expired")
        user_auth_obj= User.objects.get(username=verification.user_profile.user.username)
        request.session['user'] = user_auth_obj.username
        logger.info(
            logme('redirected to set password page', request)
        )
        return render_to_response('signup/set_password.html', context_dict,context)
    if request.method == 'POST':
        # Receiving User object from session
        user = request.session.get('user')
        user_auth_obj= User.objects.get(username=user)
        user_auth_obj.set_password(request.POST['password_set'])
        user_auth_obj.save()
        logger.info(
            logme('changed password', request)
        )
        return HttpResponse('success')


def check_valid_domain(request):
    '''
    Checking Domain is valid or not
    '''
    if request.method == 'POST':
        try:
            email=request.POST['comapny_url']
            domain = email.split("//")[-1].split("/")[0]
            domain = 'http://'+domain
            domain_name=get_tld(domain)
            logger.info(
                logme('validation- checked domain is valid for questions', request)
            )
            return HttpResponse('success')
        except:
            logger.info(
                logme('validation- checked domain is invalid for questions', request)
            )
            return HttpResponse('failed')
    if request.method == 'GET':
        return HttpResponse('Access forbidden')


class crisil_certificate_pdf(DetailView):
    '''
    Descrption: Generating CRISIL Certificate as PDF
    '''

    def get(self, request, *args, **kwargs):
        advisor = request.user.profile.advisor
        advisor_name = request.user.profile.first_name
        advisor_name1 = request.user.profile.last_name
        crisil_details = CrisilCertifications.objects.filter(advisor_id = advisor).first()
        filename = request.user.profile.first_name
        context = {
            'advisor_name':advisor_name,
            'advisor_name1':advisor_name1,
            'advisor' : advisor,
            'crisil_details' : crisil_details
        }
        template = 'signup/crisil_certificate.html'
        response = PDFTemplateResponse(
            request=request,
            template=template,
            filename=filename,
            context=context,
            show_content_in_browser=False,
            cmd_options={
                'orientation': 'landscape',
                'page-size': 'a5'
            }
        )
        logger.info(
            logme('generated CRISIL certificate as pdf', request)
        )
        return response


def upload_eipv_documents(request):
    '''
    Descrption: Uploading eIpv documents(face capture, aadhar, pancard, signature images)
    '''
    if request.method == 'POST':
        req_type = request.POST.get('req_type',None)
        user_profile = request.user.profile
        user_ob = request.user.profile
        advisor = user_profile.advisor
        documents_type = request.POST.get('document_type', None)
        eipv_image = request.POST.get('image', None)
        picture_path = upload_image_and_get_path(user_profile, documents_type, eipv_image)
        if picture_path:
            chk_document_type = UploadDocuments.objects.filter(user_profile= user_profile).filter(documents_type=str(documents_type))
            if chk_document_type:
               user_profile = UserProfile.objects.get(user=request.user)
               documents_new_upload = UploadDocuments.objects.create(user_profile=user_profile)
            else:
                documents_new_upload, status = UploadDocuments.objects.get_or_create(
                user_profile=user_profile, documents_type = documents_type)
            documents_new_upload.documents = picture_path
            documents_new_upload.documents_type = documents_type
            documents_new_upload.save()
            if documents_type == 'eipv_face_capture':
                user_profile.picture = picture_path
                user_profile.save()
            eipv_documents = get_eipv_documents(request, user_profile)
            eipv_completed = 0
            ip_details = request.session['ip_info']
            user_agent_country = ip_details.get("country", constants.REGION_DEFAULT)
            if eipv_documents['eipv_face_capture']:
                    eipv_completed = 1
                   
            data = {
                'document_url' : documents_new_upload.documents.url,
                'id': documents_new_upload.id,
                'eipv_completed' : eipv_completed,
                'document_type': documents_type,
                'result' : 'success'
            }
        logger.info(
            logme('%s EIPV documents submitted sucessfully'%(documents_type), request)
        )
        if req_type == "mobile":
           return data
        else:
            return JsonResponse(data)
    logger.info(
        logme('GET request - access forbidden for submitting EIPV docs', request)
    )
    return HttpResponse('Access forbidden')


def submit_eipv(request):
    '''
    Descrption: Making EIPV status True by checking mandatory documents uploaded or not
    '''
    if request.method == 'POST':
        req_type = request.POST.get('req_type',None)
        user_profile = request.user.profile
        advisor = user_profile.advisor
        eipv_documents = get_eipv_documents(request, user_profile)
        if eipv_documents['eipv_aadhaar'] and eipv_documents['eipv_face_capture']:
            advisor.ipv_status = True
        advisor.save()
        logger.info(
            logme('EIPV completed, status changed', request)
        )
        if req_type == "mobile":
            return "success"
        else:
            return HttpResponse(status=200)
    else:
        logger.info(
            logme('GET request - access forbidden for changing eipv status', request)
        )
        return HttpResponse('Access forbidden')


def user_repput(request):
    '''
    Navigating to my_reppute html
    '''
    PAGE_TITLE = 'my_repput'
    url = settings.DEFAULT_DOMAIN_URL+'/my_repput/'
    logger.info(
        logme("redirected to the REIA main page", request)
    )
    return render(request, 'signup/my_repput.html', locals())


def personal_info_forms(request):
    '''
    Description: Method saves details from registration form
    '''
    if request.method == 'POST':
        req_type = request.POST.get('req_type', None)
        user = request.user
        user_profile = user.profile
        advisor = user_profile.advisor
        name = request.POST.get('name', None)
        user_profile.suffix = request.POST.get('suffix', None)
        user.first_name = name
        user_profile.first_name = name
        user_profile.last_name = request.POST.get('last_name', '')
        user_profile.mobile  = request.POST.get('mobile', None)
        user_profile.address = request.POST.get('address1', None)
        user_profile.city = request.POST.get('city', None)
        user_profile.country = request.POST.get('country', None)
        # ip_details gets the advisor's country
        ip_details = request.session['ip_info']
        user_agent_country = ip_details.get("country", constants.REGION_DEFAULT)
        if not user_agent_country == constants.REGION_IN and not req_type == "mobile":
            user_profile.pincode = request.POST.get('zipcode', None)
        else:
            user_profile.pincode = request.POST.get('pincode', None)
        logout_status = ''
        user_profile.is_advisor = True
        eipv_documents = get_eipv_documents(request, user_profile)
        document = UploadDocumentsFunctions(request, user_profile)
        eipv_doc_status = document.check_document('eipv_doc')
        # constants.REGION_IN: eipv_doc
        # if user_agent_country is not "US":
        if ((eipv_documents['eipv_aadhaar']
            # and eipv_documents['eipv_pancard']
            # and eipv_documents['eipv_signature']
            and eipv_documents['eipv_face_capture']) or (
                eipv_doc_status and eipv_documents['eipv_face_capture'])):
                advisor.ipv_status = True
        # else:
        #     if (
                # eipv_documents['eipv_passport']
                # and eipv_documents['eipv_idcard']
                # and eipv_documents['eipv_signature']
                # eipv_documents['eipv_aadhaar']
                # and eipv_documents['eipv_face_capture']):
                #     advisor.ipv_status = True
        if not advisor.is_register_advisor:
            advisor.is_register_advisor = True
            advisor_type = AdvisorType.objects.filter(
                name = constants.REGULAR_ADVISOR).first()
            if advisor_type:
                advisor.type_of_advisor = advisor_type
            promo_code, created = PromoCodes.objects.get_or_create(
                user_profile = user_profile)
            dynamic_promo_code = get_random_string(length=6)
            if created == True:
                promo_code.promo_code = dynamic_promo_code
                promo_code.save()
            if user_agent_country == constants.REGION_IN:
                if user_profile.mobile:
                    mobile_number=user_profile.mobile
                    sms_status = get_sms_status(user_profile.status)
                    if sms_status == True:
                        # sending sms to user
                        message = 'Dear '+name+' ('+user_profile.registration_id+'),\
                        Congrats! You are now a Registered ABOTMI advisor. Check your \
                        E-mail to activate your account.'
                        sms_response = send_sms_alert(
                            mobile_number=mobile_number, message_template=message)
            communication_email = user_profile.email
            if user_profile.communication_email_id == 'secondary':
                communication_email = user_profile.secondary_email
            logger.info(
                logme('aadhaar:aadhaar details stored in user profile', request)
            )
            try:
                #-------------------Registered Advisor Mail--------
                if (user_profile.source_media == 'signup_with_email'
                    and advisor.is_register_advisor):
                    logout_status = True
                    # filename="Code of Business Conduct and Ethics.pdf"
                    # filepath = settings.LOADING_STATIC_FOR_PDF+\
                    #     "/pdf/CodeofBusinessConductandEthics.pdf"
                    # fo = open(filepath, "rb")
                    # filecontent = fo.read()
                    # pdf = base64.b64encode(filecontent)
                    # pdf_attachement = {
                    #     'type':'application/pdf',
                    #     'content':pdf,
                    #     'name':filename
                    # }
                    # send_mandrill_email(
                    #     'REIA_16_02',
                    #     [communication_email],
                    #     context={'username': name, 'promocode':dynamic_promo_code }
                    # )
                    # logger.info(
                    #     logme('aadhaar:email sent successfully to social signup user', request)
                    # )
                # else:
                    send_mandrill_email(
                        'ABOTMI_05',
                        [communication_email],
                        context={'name': user.profile.first_name}
                    )
                    logger.info(
                        logme('EIPV Registration:email sent successfully to  direct signup user', request)
                    )
                context_dict = {
                    'Name': name
                }
                send_mandrill_email(
                    'ABOTMI_04',
                    [communication_email],
                    context=context_dict
                )
                if user_profile.source_media != 'signup_with_email':
                    user_password = get_random_string(length=8)
                    user.set_password(user_password)
                    user.save()
                    try:
                        send_mandrill_email(
                            'ABOTMI_02',
                            [communication_email],
                            context={
                                'name':user.profile.first_name,
                                'url': NEXT_URL_LINK,
                                'username': user.profile.email,
                                'password': user_password
                            }
                        )
                        logger.info(
                            logme('sent login credentials to advisor for social signup', request)
                        )
                    except:
                        logger.info(
                            logme('failed to send login credentials to advisor for social signup', request)
                        )
                    logout_status = True
                # trigger mail to support team with the few details of advisor
                context_dict = {
                    'name': user.profile.first_name,
                    'user_email': user.profile.email,
                    'mobile_number': user.profile.mobile,
                    'city' : user.profile.city
                }
                send_mandrill_email(
                    'ABOTMI_20',
                    [constants.UPWRDZ_SUPPORT],
                    context=context_dict
                )

            except Exception as e:
                logger.info(
                    logme('EIPV Registeration:failed to send mail for EIPV Register fucntion Exception: {}'.format(e), request)
                )
            if user_profile.source_media == 'FASIA' and advisor.is_register_advisor:
                salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
                activation_key = hashlib.sha1(salt + user.email).hexdigest()
                key_expires = datetime.datetime.today() + datetime.timedelta(2)
                verification, created = EmailVerification.objects.get_or_create(
                    user_profile=user_profile)
                verification.activation_key = activation_key
                verification.key_expires = key_expires
                verification.save()
                communication_email = user_profile.email
                try:
                    send_mandrill_email(
                        'ABOTMI_23',
                        [user_profile.email],
                        context={
                            'Name': user_profile.first_name,
                            'Website': settings.DEFAULT_HOST,
                            'Ack': activation_key
                        }
                    )
                except:
                    logger.error(
                        logme(
                            'failed to send email for set password link', request)
                    )
                advisor.save()
                user_profile.save()
                user.save()
                return HttpResponse(logout_status)
        advisor.save()
        user_profile.save()
        user.save()
        '''
        Adding refferal points and creating notification
        '''
        if user_profile.referred_by:
            beneficiary_obj = user_profile.referred_by.profile
            referral_obj = user_profile
            if beneficiary_obj.referral_code:
                referral_points(beneficiary_obj, referral_obj, constants.REGISTERED_ADVISOR)
        # temporary commented, once blockchain settup is done, it will be enabled
        # create_user_blockchain_account_and_transaction.apply_async((user_profile.id,))
        if req_type == "mobile":
           return "success"
        else:
            return HttpResponse(logout_status)


def send_otp(request):
    '''
    Description: Send otp to email and mobile phone
    '''
    if request.method == 'POST':
        req_type = request.POST.get('req_type',None)
        mobile = request.POST.get('mobile', None)
        email = request.POST.get('email', None)
        medium = request.POST.get('medium', None)
        name = request.POST.get('name', None)
        user = request.user
        user_profile = user.profile
        mobile_otp = random.randint(100000, 999999)
        ip_details = request.session['ip_info']
        user_agent_country = ip_details.get("country", constants.REGION_DEFAULT)
        if mobile and user_agent_country == constants.REGION_IN:
            if medium == constants.OTP_TO_MOBILE or medium == None:
                user_otp, created = UserMobileOtp.objects.get_or_create(
                    otp_source = constants.OTP_MOBILE,
                    user_profile_id = user_profile.id,
                    mobile = mobile
                )
                user_otp.otp = mobile_otp
                user_otp.mobile = mobile
                user_data = {}
                user_data['mobile'] = mobile
                user_data['name'] = name
                name = name.split(" ")[0]
                user_otp.verify_data = json.dumps(user_data)
                user_otp.save()
                message = 'Dear '+name+', Your OTP is '+str(mobile_otp)+'.'
                try:
                    sms_response = send_sms_alert(mobile_number=mobile,
                        message_template=message)
                except:
                    msg="Unable to send"

        if (user_profile.email == email
            and user_profile.source_media != constants.SIGNUP_WITH_EMAIL):
            if medium == constants.OTP_TO_EMAIL or medium == None:
                num = uuid.uuid4().hex[:6]
                user_otp, created = UserMobileOtp.objects.get_or_create(
                    otp_source = constants.OTP_EMAIL,
                    user_profile_id = user_profile.id
                )
                user_otp.otp = num
                user_otp.mobile = mobile
                user_data = {}
                user_data['email'] = email
                user_data['name'] = name
                user_otp.verify_data = json.dumps(user_data)
                user_otp.save()
                try:
                    data = {
                        'member_name' : name,
                        'otp' : num
                    }
                    send_mandrill_email(
                        'ABOTMI_19',
                        [email],
                        context = data
                    )
                except:
                    message="Unable to send"
        if req_type =="mobile":
           return "sucess"
        else:
           return HttpResponse(status=200)


def verify_otp(request):
    '''
    Description: Verify otp
    '''
    if request.method == 'POST':
        user_profile = request.user.profile
        req_type = request.POST.get('req_type', None)
        mobile_otp = request.POST.get('otp', None)
        email_otp = request.POST.get('email_otp', None)
        user_mobile_otp, user_email_otp = None, None
        email_otp_verified, mobile_otp_verified =  None, None
        user_status = user_profile.status
        ip_details = request.session['ip_info']
        user_agent_country = ip_details.get("country", constants.REGION_DEFAULT)
        if user_agent_country != constants.REGION_IN:
            mobile_otp_verified = True
        if user_agent_country == constants.REGION_IN:
            if mobile_otp:
                user_mobile_otp = UserMobileOtp.objects.filter(
                    otp = mobile_otp,
                    user_profile_id = user_profile.id,
                    otp_source = constants.OTP_MOBILE
                ).first()
                if user_mobile_otp:
                    mobile_otp_verified = True
                    user_status.mobile_verified = True
            else:
                return JsonResponse({'status':204})
        if not user_profile.source_media == constants.SIGNUP_WITH_EMAIL:
            if email_otp:
                user_email_otp = UserMobileOtp.objects.filter(
                    otp = email_otp,
                    user_profile_id = user_profile.id,
                    otp_source = constants.OTP_EMAIL
                ).first()
                if user_email_otp:
                    email_otp_verified = True
                    user_status.email_verified = True
            else:
                return JsonResponse({'status':204})
        if user_profile.source_media == constants.SIGNUP_WITH_EMAIL and user_mobile_otp:
            user_mobile_otp.delete()
        else:
            if user_mobile_otp and user_email_otp:
                user_email_otp.delete()
                user_mobile_otp.delete()
        data = {
            'status' : 200,
            'is_email_otp' : email_otp_verified,
            'is_mobile_otp' : mobile_otp_verified
        }
        user_status.save()
        if req_type == "mobile":
            return data
        else:
            return JsonResponse(data)


@allow_advisor
def aadhaar_verification(request):
    '''
    Description: Navigating to aadhaar verification page
    '''
    ip_region = get_ip_region(request)
    if ip_region == 'IN':
        title = constants.EKYC_AADHAAR
    else:
        title = 'Verification Process'

    user = request.user
    user_profile = user.profile
    advisor = user_profile.advisor
    result = get_kyc_step_status(request, user, user_profile, advisor)
    country = Country.objects.all().values('name', 'code')
    ip_region = get_ip_region(request)
    if ip_region == 'US':
        passport = UploadDocuments.objects.filter(
            user_profile=user_profile,
            documents_type='passport'
        )
        is_passport = map(int, passport.values_list('id', flat=True))
        driving_licence = UploadDocuments.objects.filter(
            user_profile=user_profile,
            documents_type='driving_licence'
        )
        is_dl = map(int, driving_licence.values_list('id', flat=True))
        id_card = UploadDocuments.objects.filter(
            user_profile=user_profile,
            documents_type='id_card'
        )
        is_id_card = map(int, id_card.values_list('id', flat=True))
    return render(request, 'signup/ekyc_aadhaar.html', locals())


def save_foot_print_verification(request):
    '''
    Description: Foot print verification in step 5 form
    '''
    if request.method =='POST':
        user_profile = request.user.profile
        req_type = request.POST.get('req_type', None)
        digital_links = request.POST.get('digital_links', None)
        if digital_links:
            digital, created = DigitalFootPrint.objects.get_or_create(
                digital_links=digital_links)
            if created:
                digital.user_profile = user_profile
                digital.save()
                logger.info(
                    logme("Sucessfully saved the DigitalFootPrint", request)
                )
            res = 'success'
        else:
            logger.info(
                logme("Unable to save the DigitalFootPrint", request)
            )
            res = 'failed'
        if req_type == 'mobile':
            return res
        else:
            return HttpResponse(res)
    else:
        logger.info(
            logme("Get Reuquest - Access forbidden to save the DigitalFootPrint", request)
        )
        return HttpResponse('Access forbidden')


def delete_foot_print_verification(request):
    '''
    Description: Deleting the records
    '''
    if request.method =='POST':
        user_profile = request.user.profile
        req_type = request.POST.get('req_type', None)
        digital_links = request.POST.get('digital_links', None)
        if digital_links:
            digital = DigitalFootPrint.objects.filter(digital_links=digital_links)
            if digital:
                digital.delete()
                logger.info(
                    logme("Sucessfully Deleted DigitalFootPrint", request)
                )
            res = 'success'
        else:
            logger.info(
                logme("Unable Delete DigitalFootPrint", request)
            )
            res = 'failed'
        if req_type == 'mobile':
            return res
        else:
            return HttpResponse(res)
    else:
        logger.info(
            logme("Get Reuquest - Access forbidden to Delete the DigitalFootPrint", request)
        )
        return HttpResponse('Access forbidden')


def check_irda_registration_no(request):
    '''
    Description: onchange function for checking IRDA data.
    '''
    irda_reg_number = request.POST['irda_registration_number']
    kwargs = {}
    if irda_reg_number:
        kwargs['license_no__icontains'] = irda_reg_number
        check_irda_obj = IrdaData.objects.filter(**kwargs)
        if check_irda_obj:
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=204)


def check_registration_data_exists(request):
    '''
    Description: onchange function for checking IRDA data.
    '''
    red_data_document_type = request.POST['document_data_type']
    kwargs = {}

    if red_data_document_type == 'irda_registration_no':
        irda_reg_number = request.POST['doc_registration_number']
        if irda_reg_number:
            kwargs['irda_urn__icontains'] = irda_reg_number
            check_irda_obj = IrdaData.objects.filter(**kwargs)
            if check_irda_obj:
                return HttpResponse(status=200)
            else:
                return HttpResponse(status=204)
        else:
            return HttpResponse(status=204)
    elif red_data_document_type == 'sebi_registration_no':
        sebi_reg_number = request.POST['doc_registration_number']
        if sebi_reg_number:
            kwargs['reg_no__icontains'] = sebi_reg_number
            check_sebi_obj = SebiData.objects.filter(**kwargs)
            if check_sebi_obj:
                return HttpResponse(status=200)
            else:
                return HttpResponse(status=204)
        else:
            return HttpResponse(status=204)
    elif red_data_document_type == 'amfi_registration_no':
        amfi_reg_number = request.POST['doc_registration_number']
        if amfi_reg_number:
            kwargs['arn__icontains'] = amfi_reg_number
            check_amfi_obj = AmfiData.objects.filter(**kwargs)
            if check_amfi_obj:
                return HttpResponse(status=200)
            else:
                return HttpResponse(status=204)
        else:
            return HttpResponse(status=204)
    else:
        return HttpResponse(status=204)


def save_adhaar(request):
    '''
    Description: It saves the aadhaar number from ekyc aadhaar page
    '''
    aadhaar_number = request.POST.get('aadhaar_number', None)
    if aadhaar_number:
        user_profile = request.user.profile
        user_profile.adhaar_card = aadhaar_number
        user_profile.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)


def submit_verification(request):
    '''
    Submitting the Verfication form(KYC step1)
    '''
    if request.method == 'POST':
        passport_no = request.POST.get('passport_no', None)
        adhaar_no = request.POST.get('adhaar_no', None)
        u_p = request.user.profile
        if passport_no: u_p.passport_no = passport_no
        if adhaar_no: u_p.adhaar_card = adhaar_no
        u_p.save()
        return HttpResponse(200)
    else:
        return HttpResponse('Access Forbidden')


def update_verification_type(request):
    if request.method == 'POST':
        documents_type = request.POST.get('documents_type', None)
        user_profile = request.user.profile
        user_profile.proof_of_identity = documents_type
        user_profile.save()
        return HttpResponse('success')
    else:
        return HttpResponse('Access forbidden')   


@allow_advisor
def face_capture(request):
    title = 'Profile Picture'
    user = request.user
    user_profile = user.profile
    advisor = user_profile.advisor
    result = get_kyc_step_status(request, user, user_profile, advisor)
    eipv_face_capture = UploadDocuments.objects.filter(
        documents_type='eipv_face_capture',
        user_profile=user_profile
    ).first()
    res_context = {
        'result': result,
        'title': title,
        'eipv_face_capture': eipv_face_capture
    }
    return render(request, 'signup/ekyc/ekyc_step1.html', context=res_context)


def check_user_exist(request):
    '''
    Checking User is Already exists or not in the database
    '''
    if request.method == "POST":
        username = request.POST.get('username', None)
        user = User.objects.filter(username=username).first()
        try:
            if user:
                return HttpResponse(status=200)
            else:
                return HttpResponse(status=204)
            logger.info(
                logme('validation - email exists', request)
            )
        except Exception as e:
            logger.info(
                logme('Error: Checking Emails--%s' % (str(e)), request)
            )
            return HttpResponse(status=500)
    if request.method == "GET":
        logger.info(
            logme('GET request - access forbidden for checking email', request)
        )
        return HttpResponse(status=405)


@allow_advisor
def educational_qualification(request):

    '''
    Function saves the education and certification details of the advisor
    '''
    if request.method == 'POST':

        user = request.user
        user_profile = user.profile
        advisor = user_profile.advisor
        certification_detail = request.POST.get('certification_details', None)
        educational_detail = request.POST.get('educational_details', None)
        if educational_detail:
            educational_detail= json.loads(educational_detail)
            educational_detail = [{
                'qualification': educational_detail['qualification'],
                'school': educational_detail['school'],
                'field_of_study': educational_detail['field_of_study'],
                'grade': educational_detail.get('grade', None),
                'activities': educational_detail['activities'],
                'from_year': educational_detail['from_year'],
                'to_year': educational_detail['to_year']
            }]

        if certification_detail:
            certification_detail = json.loads(certification_detail)
            certification_loop = [{

                'certification_name': certification.get('certification_name',""),
                'certi_authority': certification.get('certi_authority',""),
                'licence_number': certification.get('licence_number',""),
                'time_period_from': certification.get('time_period_from',""),
                'certi_url': certification.get('certi_url',""),
                'certi_credibility': certification.get('certi_credibility',""),
                'from_year': certification.get('from_year',""),
                'to_year': certification.get('to_year',""),
                'is_expire': certification.get('is_expire',""),
                'certificate_doc': certification.get('certificate_doc', ""),
                'certificate_doc_id': certification.get('certificate_doc_id', "")
            } for certification in certification_detail if certification_detail]

        education_obj,status = EducationAndCertificationDetails.objects.get_or_create(user_profile=user_profile)
        if education_obj:
            education_obj.educational_details = json.dumps(educational_detail)
            education_obj.certification_details = json.dumps(certification_loop)
            education_obj.save()
            result = get_kyc_step_status(request, user, user_profile, advisor)
            if not ('partial' and 'not_filled') in result:
                if not advisor.is_register_advisor:
                    advisor.is_register_advisor = True
                    advisor.save()
                    # Notification class object
                    nf = NotificationFunctions(
                        request=request, receive=user_profile)
                    nf.save_notification(
                        notification_type=REGISTRATION_TEMPLATE
                    )
                    if user_profile.referred_by:
                        refer_obj = user_profile.referred_by
                        nf.save_notification(
                            data=[refer_obj.get_full_name()],
                            receive=refer_obj,
                            sender=user_profile,
                            notification_type=REFER_REGISTRATION
                        )
                    context_dict = {
                        'Name': user_profile.first_name
                    }
                    send_mandrill_email(
                        'ABOTMI_04',
                        [user_profile.email],
                        context=context_dict
                    )
                    # Send Calendly registration intimation to Advisor
                    context_dict = {
                        'User_name': user_profile.first_name
                    }
                    send_mandrill_email(
                        'ABOTMI_30',
                        [user_profile.email],
                        context=context_dict
                    )
            return JsonResponse({
                'kyc_status' : result,
            }, status=200)
        else:

            return HttpResponse(400)
    else:
        return HttpResponse(405)


@login_required()
def investor_identity(request, slug=None):
    '''
    Navigting to edit_profile html to Edit users details
    '''

    if request.method == "GET":
        if slug:
            investor_user_profile = UserProfile.objects.filter(
                batch_code=slug).first()
            investor_user = investor_user_profile.user
            is_own_profile = False
        else:
            investor_user = request.user
            investor_user_profile = investor_user.profile
            is_own_profile = True
        # advisor = user_profile.advisor
        profile_pic = ''
        if investor_user_profile.picture:
            profile_pic = investor_user_profile.picture.url
        logger.info(
            logme('opened edit profile modal', request)
        )
        return render(request, "member/investor_identity.html", locals())

    if request.method == "POST":
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        email = request.POST.get('email', None)
        mobile = request.POST.get('mobile', None)
        city = request.POST.get('city', None)
        gender = request.POST.get('gender', None)
        pincode = request.POST.get('pincode', None)
        user = User.objects.get(username = request.user.username)
        user.first_name = first_name
        user.last_name  = last_name
        user.save()
        user_profile = UserProfile.objects.get(user=user)
        user_profile.first_name = first_name
        user_profile.last_name = last_name
        user_profile.mobile = mobile
        user_profile.city = city
        user_profile.gender = gender
        user_profile.pincode = pincode
        birthdate = request.POST.get('birthdate', None)
        if birthdate:
            birthdate_parse = dateutil.parser.parse(birthdate)
            user_profile.birthdate = birthdate_parse
        user_profile.save()
        return HttpResponse(status=200)
