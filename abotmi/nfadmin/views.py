# python lib
import base64
import cStringIO as StringIO
import datetime
import json
import hashlib
import logging
import os
import pandas as pd
import random
import requests

# Django modules
from django.conf import settings
from django.contrib.auth.models import User
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.utils.crypto import get_random_string
from django.utils.dateparse import parse_date
from django.views.generic import View

# Third party lib
from itertools import chain
from itertools import groupby
from num2words import num2words
from tld import get_tld
from xhtml2pdf import pisa

# Database Models
from datacenter.models import (
    UserProfile, Advisor, UploadDocuments, ReferralPointsType,
    ReferralPoints, India_Pincode, Country, CrisilCertifications, TransactionsDetails,
    PromoCodes, AdvisorType, EmailVerification, AffiliatedCompany, AdvisorVideoRequest,
    AdvisorPublishedVideo, SubscriptionPackageMaster, FeatureListMaster,Testimonial,
    SubscriptionCategoryMaster, UserStatus, NoticeBoard)

# Local imports
from .forms import (
    Userprofile_Firsttab, User_Form, AdvisorCredibilityForm,
    CrisilCertificateForm)
from blog.views import create_word_press_user
from common import constants, api_constants
from common.views import (
    referral_points, invoice_gen, get_sms_status, invoice_bill_pdf,
    UploadDocumentsFunctions, auth_token, upload_image_and_get_path)
from common.utils import (
    send_sms_alert, generate_key, send_sms_alert,
    calculate_discount_amount)
from login.decorators import allow_nfadmin, allow_crisil_admin
from nfadmin.serializers import GetNotApprovedRegulatory, GetAdditionalQualificationDocs
from signup.djmail import send_mandrill_email, send_mandrill_email_with_attachement

# Constatns
from common.api_constants import USER_UPLOAD_DOCUMENTS_LINK, NEXT_URL_LINK

logger = logging.getLogger(__name__)


@allow_nfadmin
def index(request):
    '''
    Listing Social media signup, Register, Certified and Total Advisors count and 
        navigating to admin_index html
    '''
    context = RequestContext(request)
    google_signup_count = UserProfile.objects.filter(
        source_media='google'
    ).values('id').count()
    facebook_signup_count = UserProfile.objects.filter(
        source_media='facebook'
    ).values('id').count()
    linkedin_signup_count = UserProfile.objects.filter(
        source_media='linkedin'
    ).values('id').count()
    twitter_signup_count = UserProfile.objects.filter(
        source_media='twitter'
    ).values('id').count()
    total_advisor_count = UserProfile.objects.filter(
        is_advisor=True).values('id').count()
    total_registered_advisors = Advisor.objects.filter(
        is_register_advisor=True).values('id').count()
    total_certified_advisors = Advisor.objects.filter(
        is_certified_advisor=True).values('id').count()
    context_dict = {
        'PRODUCT_NAME': settings.PRODUCT_NAME,
        'LOGIN_URL': settings.LOGIN_URL,
        'LOGOUT_URL': settings.LOGOUT_URL,
        'LOGIN_REDIRECT_URL': settings.LOGIN_URL,
        'google_signup': google_signup_count,
        'facebook_signup': facebook_signup_count,
        'linkedin_signup': linkedin_signup_count,
        'twitter_signup': twitter_signup_count,
        'total_advisors': total_advisor_count,
        'total_registered_advisors': total_registered_advisors,
        'total_certified_advisors': total_certified_advisors,
    }
    return render_to_response('nfadmin/admin_index.html', context_dict, context)


@allow_nfadmin
def advisor_list(request):
    '''
    Getting only Advisors list(excepting admin, nfadmin, clients/members, CRISIL admin, 
    company admin Ids) and navigating to advisor_list_view html
    '''
    context = RequestContext(request)
    nfadmin_ids = UserProfile.objects.filter(is_admin=True).values('user')
    clients_basic_details = UserProfile.objects.filter(is_member=True).values('user')
    company_obj = UserProfile.objects.filter(is_company=True).values('user')
    crisil_admin_obj = UserProfile.objects.filter(is_crisil_admin=True).values('user')
    user_basic_details = User.objects.filter(is_superuser=False).exclude(
        Q(id__in=nfadmin_ids) 
        | Q(id__in=company_obj) 
        | Q(id__in=clients_basic_details) 
        | Q(id__in=crisil_admin_obj)
    )

    context_dict = {
        'PRODUCT_NAME': settings.PRODUCT_NAME,
        'LOGIN_URL': settings.LOGIN_URL,
        'LOGOUT_URL': settings.LOGOUT_URL,
        'LOGIN_REDIRECT_URL': settings.LOGIN_URL,
        'user_basic_details': user_basic_details,
    }
    return render_to_response('nfadmin/advisor_list_view.html', context_dict, context)


@allow_nfadmin
def add_client_list(request):
    '''
    Listing Client/Member list in add_client_list html
    '''
    context = RequestContext(request)
    user_basic_details = UserProfile.objects.filter(is_member=True)
    context_dict = {
        'PRODUCT_NAME':settings.PRODUCT_NAME,
        'LOGIN_URL':settings.LOGIN_URL,
        'LOGOUT_URL': settings.LOGOUT_URL,
        'LOGIN_REDIRECT_URL':settings.LOGIN_URL,
        'user_basic_details':user_basic_details,
    }
    return render_to_response('nfadmin/add_client_list.html', context_dict, context)


@allow_nfadmin
def view_advisor_modal(request):
    '''
    Fetching the Advisor details and showing in view_advisor_modal html
    '''
    context = RequestContext(request)
    if request.method == 'POST':
        ids = request.POST['user_id']
        advisor_details = UserProfile.objects.get(user_id=ids)
        advisor = Advisor.objects.get(user_profile=advisor_details)
        if advisor_details.additional_qualification:
            additional_qualification_list = json.loads(
                advisor_details.additional_qualification)
        else:
            additional_qualification_list = ''
        if advisor.questions:
            question_list = json.loads(advisor.questions)
            if question_list[1]['Answer'] == 'yes':
                office_address = json.loads(
                    advisor.questions)[1]['Remark'].replace("!"," ")
                office_address = office_address.replace("$","\n")
                office_address = office_address
            else:
                office_address = ''
        else:
            question_list = ''
            office_address = ''
        user_documents  = UploadDocuments.objects.filter(user_profile=advisor_details)
        financial_instruments = ''
        if advisor_details.advisor.financial_instruments:
            financial_instruments = json.loads(
                advisor_details.advisor.financial_instruments)
        rera_details = ''
        if advisor_details.advisor.rera_details:
            rera_details = json.loads(advisor_details.advisor.rera_details)
        context_dict    = {
            'PRODUCT_NAME': settings.PRODUCT_NAME,
            'advisor_details': advisor_details,
            'user_documents': user_documents,
            'additional_qualification_list': additional_qualification_list,
            'questions': question_list,
            'office_address': office_address,
            'financial_instruments': financial_instruments,
            'rera_details': rera_details
        }
        return render_to_response(
            'nfadmin/view_advisor_modal.html', context_dict, context)
    else:
        return HttpResponse('you dont have access <a href="/nfadmin/">click here</a>')


@allow_nfadmin
def view_member_modal(request):
    '''
    Loading Member details in to view_member_modal html
    '''
    context = RequestContext(request)
    if request.method == 'POST':
        try:
            ids = request.POST['user_id']
            member_details = UserProfile.objects.get(id=ids)
            context_dict = {
                'PRODUCT_NAME': settings.PRODUCT_NAME,
                'member_details':member_details,
            }
            return render(request,'nfadmin/view_member_modal.html',locals())
        except Exception as e:
            pass
    else:
        return HttpResponse('you dont have access <a href="/nfadmin/">click here</a>')


@allow_nfadmin
def edit_user_profile_modal(request):
    '''
    Loading Advisor details into edit_advisor_modal html for Edit 
    '''
    context = RequestContext(request)
    if request.method == 'POST':
        user_id = request.POST['user_id']
        user = User.objects.get(id = user_id)
        advisor_details = UserProfile.objects.get(user_id = user_id)
        advisor = Advisor.objects.get(user_profile = advisor_details)
        credibility_advisor_details = Advisor.objects.get(user_profile = advisor_details)
        if advisor_details.additional_qualification:
            additional_qualification_list = json.loads(
                advisor_details.additional_qualification)
        else:
            additional_qualification_list = ''
        user_documents  = UploadDocuments.objects.filter(user_profile = advisor_details)
        user_form = User_Form(instance = user)
        profile_form = Userprofile_Firsttab(instance = advisor_details)
        credibility_form = AdvisorCredibilityForm(instance = credibility_advisor_details)
        context_dict = {'country_list': Country.objects.all()}
        return render(request,'nfadmin/edit_advisor_modal.html',locals())
    else:
        return HttpResponse('you dont have access <a href="/nfadmin/">click here</a>')


@allow_nfadmin
def edit_member_profile_modal(request):
    '''
    Loading Member details into edit_member_modal html to edit
    '''
    context = RequestContext(request)
    if request.method == 'POST':
        user_id = request.POST['user_id']
        user = User.objects.get(id = user_id)
        member_details = UserProfile.objects.get(user_id = user_id)
        member = UserProfile.objects.get(user_profile = member_details)
        user_form = User_Form(instance = user)
        context_dict = {'country_list': Country.objects.all()}
        return render(request,'nfadmin/edit_member_modal.html',locals())
    else:
        return HttpResponse('you dont have access <a href="/nfadmin/">click here</a>')


@allow_nfadmin
def save_user_profile_model(request):
    '''
    Validating the Edit form and Saving the edited Advisor details
    '''
    if request.method == 'POST':
        user_form = User_Form(request.POST)
        profile_form = Userprofile_Firsttab(request.POST)
        credibility_form = AdvisorCredibilityForm(request.POST)
        if user_form.is_valid() \
            and profile_form.is_valid() and credibility_form.is_valid():
            user = User.objects.get(username = request.POST['email'])
            user_form = User_Form(
                request.POST, 
                instance=User.objects.get(username=user)
            )
            user_form.save()
            profile = Userprofile_Firsttab(request.POST)
            profile_form = Userprofile_Firsttab(
                request.POST, 
                instance=UserProfile.objects.get(user_id=user.id)
            )
            user_profile = profile_form.save(commit=False)
            user_profile.first_name = request.POST['first_name']
            user_profile.last_name = request.POST['last_name']
            user_profile.save()
            credibility_form = AdvisorCredibilityForm(
                request.POST,
                instance=Advisor.objects.get(user_profile=user.profile.id)
            )
            credibility_profile = credibility_form.save(commit=False)
            json_financial_instruments = []
            json_financial_dict = {}
            try:
                if request.POST['id_exp_equity']:
                    equity_dict = {}
                    equity_dict['instruments'] = 'Equity'
                    equity_dict['experience'] = request.POST['id_exp_equity']
                    json_financial_instruments.append(equity_dict)
            except Exception:
                pass
            try:
                if request.POST['id_exp_wealth_advisory']:
                    wealth_advisory_dict = {}
                    wealth_advisory_dict['instruments'] = 'Wealth Advisory'
                    wealth_advisory_dict['experience'] = request.POST[
                        'id_exp_wealth_advisory']
                    json_financial_instruments.append(wealth_advisory_dict)
            except Exception:
                pass
            try:
                if request.POST['id_exp_mutual_fund']:
                    mutual_fund_dict = {}
                    mutual_fund_dict['instruments'] = 'Mutual Fund'
                    mutual_fund_dict['experience'] = request.POST['id_exp_mutual_fund']
                    json_financial_instruments.append(mutual_fund_dict)
            except Exception:
                pass
            try:
                if request.POST['id_insurance']:
                    insurance_dict = {}
                    insurance_dict['instruments'] = 'Insurance'
                    insurance_dict['experience'] = request.POST['id_insurance']
                    json_financial_instruments.append(insurance_dict)
            except Exception:
                pass
            try:
                if request.POST['id_real_estate']:
                    real_estate_dict = {}
                    real_estate_dict['instruments'] = 'Real Estate'
                    real_estate_dict['experience'] = request.POST['id_real_estate']
                    json_financial_instruments.append(real_estate_dict)
            except Exception:
                pass
            try:
                if request.POST['id_portfolio_management']:
                    portfolio_management_dict = {}
                    portfolio_management_dict['instruments'] = 'Portfolio Management'
                    portfolio_management_dict['experience'] = request.POST[
                        'id_portfolio_management']
                    json_financial_instruments.append(portfolio_management_dict)
            except Exception:
                pass
            financial_instruments_json = json.dumps(json_financial_instruments)
            credibility_profile.financial_instruments = financial_instruments_json
            if request.POST['others_qualification']:
                credibility_profile.credibility_declaration_qualification = request.POST[
                    'others_qualification']
            else:
                credibility_profile.credibility_declaration_qualification = request.POST[
                    'credibility_declaration_qualification']
            credibility_form.save()
            return HttpResponse('success')
        return render(request, 'nfadmin/edit_advisor_modal.html', locals())
    else:
        return render(request, 'nfadmin/edit_advisor_modal.html', locals())


@allow_nfadmin
def user_checkpin(request):
    '''
    Checking pincode is exist or not
    '''
    if request.method == 'POST':
        pincode = request.POST['pincode']
        pincode_object = India_Pincode.objects.filter(pin_code = pincode)
        if pincode_object:
            state = pincode_object[0].state_name
            return HttpResponse(state)
    else:
        return HttpResponse("Access forbidden")


@allow_nfadmin
def remove_upload_file(request):
    '''
    Removing the Upload file from database
    '''
    if request.method == 'POST':
        user_id = request.POST['id']
        result_document = UploadDocuments.objects.get(id = user_id)
        if result_document :
            if result_document.documents_type == "Profile Picture":
                user = User.objects.get(username = result_document.user_profile)
                user_profile_obj = UserProfile.objects.get(user = user)
                user_profile_obj.picture=''
                user_profile_obj.save()
            result_document.delete()
            return HttpResponse('Sucess')
    if request.method == 'GET':
        return HttpResponse("Access forbidden")


@allow_nfadmin
def activate_user(request):
    '''
    Activating the User
    '''
    context = RequestContext(request)
    if request.method == 'POST':
        ids = request.POST['id']
        status = 1
        user_details = User.objects.get(id=ids)
        user_details.is_active = status
        user_details.save()
        communication_email = user_details.profile.email
        if user_details.profile.communication_email_id == "secondary":
            communication_email = user_details.profile.secondary_email
        context_dict = {
            "first_name": user_details.first_name
        }
        send_mandrill_email('ABOTMI_18', [communication_email], context_dict)
        return render_to_response('nfadmin/advisor_list_view.html',context)
    else:
        return HttpResponse('you dont have access <a href="/nfadmin/">click here</a>')


@allow_nfadmin
def de_activate_user(request):
    '''
    Deactivating the User
    '''
    context = RequestContext(request)
    if request.method == 'POST':
        ids = request.POST['id']
        status = 0
        user_details = User.objects.get(id=ids)
        user_details.is_active = status
        user_details.save()
        communication_email = user_details.profile.email
        if user_details.profile.communication_email_id == "secondary":
            communication_email = user_details.profile.secondary_email
        context_dict = {
            "first_name": user_details.first_name
        }
        send_mandrill_email('ABOTMI_17', [communication_email], context_dict)
        return render_to_response('nfadmin/advisor_list_view.html',context)
    else:
        return HttpResponse('you dont have access <a href="/nfadmin/">click here</a>')


@allow_nfadmin
def grand_advisor(request):
    '''
    Making user as Advisor
    '''
    context = RequestContext(request)
    if request.method == 'POST':
        user_id = request.POST['user_id']
        user_profile = UserProfile.objects.get(user_id=user_id)
        user_profile.is_advisor = True
        user_profile.save()
        return render_to_response('nfadmin/advisor_list_view.html',context)
    else :
        return HttpResponse('you dont have access <a href="/nfadmin/">click here</a>')


@allow_nfadmin
def revoke_advisor(request):
    '''
    Revoking Advisor Access
    '''
    context = RequestContext(request)
    if request.method == 'POST':
        user_id = request.POST['user_id']
        user_profile = UserProfile.objects.get(user_id=user_id)
        user_profile.is_advisor = False
        user_profile.save()
        return HttpResponse('success')
    else:
        return HttpResponse('you dont have access <a href="/nfadmin/">click here</a>')


@allow_nfadmin
def make_confirmed_advisor(request):
    '''
    Confirming the Advisor
    '''
    context=RequestContext(request)
    if request.method == 'POST':
        user_id = request.POST['user_id']
        user_profile = UserProfile.objects.get(user_id = user_id)
        advisor = Advisor.objects.get(user_profile = user_profile)
        advisor.is_confirmed_advisor = True
        advisor.save()
        if user_profile.mobile:
            mobile_number=user_profile.mobile
            sms_status = get_sms_status(user_profile.status)
            if sms_status == True:
                # sending sms to user
                message = 'Dear '+user_profile.first_name+' ('\
                +user_profile.registration_id+'),Your application has been approved. \
                Check E-mail to complete registration'
                sms_response = send_sms_alert(
                    mobile_number=mobile_number,
                    message_template=message
                )
        context = {
            'name' : user_profile.first_name,
            'url' : USER_UPLOAD_DOCUMENTS_LINK
        }
        communication_email = user_profile.email
        if user_profile.communication_email_id == 'secondary':
            communication_email = user_profile.secondary_email
        return HttpResponse('success')
    else:
        HttpResponse('Access forbidden')


@allow_nfadmin
def make_not_confirmed_advisor(request):
    '''
    Revoking confirm advisor access
    '''
    context = RequestContext(request)
    if request.method == 'POST':
        user_id = request.POST['user_id']
        user_profile = UserProfile.objects.get(user_id = user_id)
        advisor = Advisor.objects.get(user_profile = user_profile)
        advisor.is_confirmed_advisor = False
        advisor.save()
        return HttpResponse('success')
    else:
        return HttpResponse('failed')


def registered_advisor_email(user_id):
    '''
    -> Making user as Register advisor.
    -> setting advisor as confirm advisor. 
    -> Generating Promocode for advisor
    -> Adding points to refered advisor if advisor is got refered by some advisor
    -> Sending Registration credentails mail to advisor email id
    '''
    user = User.objects.get(id = user_id)
    user_profile = user.profile
    advisor = user_profile.advisor
    advisor_type = AdvisorType.objects.filter(name = constants.REGULAR_ADVISOR)
    user_profile.is_advisor = True
    advisor.is_register_advisor = True
    advisor.is_confirmed_advisor = True
    if advisor_type:
        advisor.type_of_advisor = advisor_type[0]
    if not user.profile.source_media == 'signup_with_email':
        user_password = get_random_string(length=8)
        user.set_password(user_password)
    # Generating Promocode one time for Advisor
    promo_code,created = PromoCodes.objects.get_or_create(user_profile = user_profile)
    dynamic_promo_code = get_random_string(length=6)
    if created == True:
        promo_code.promo_code = dynamic_promo_code
        promo_code.save()
    # Level 2 Referral Points
    if user.profile.referred_by:
        beneficiary_obj = user.profile.referred_by.profile
        referral_obj = user.profile
        if beneficiary_obj.referral_code:
            referral_points(beneficiary_obj, referral_obj, constants.REGISTERED_ADVISOR)

    if user_profile.mobile:
        mobile_number=user_profile.mobile
        sms_status = get_sms_status(user_profile.status)
        if sms_status == True:
            # sending sms to user
            message = 'Dear '+user_profile.first_name+' ('+user_profile.registration_id+'),Congrats! You are now a Registered UPWRDZ advisor. Check your E-mail to activate your account.'
            sms_response = send_sms_alert(mobile_number=mobile_number,message_template=message)
    # mail sending using communication Email ID
    communication_email = user_profile.email
    if user_profile.communication_email_id == 'secondary':
        communication_email = user_profile.secondary_email
    is_mail_sent = True
    try:
        #-------------------Registered Advisor Mail--------
        if not user.profile.source_media == 'signup_with_email':
            filename="Code of Business Conduct and Ethics.pdf"
            filepath = settings.LOADING_STATIC_FOR_PDF\
                +"/pdf/CodeofBusinessConductandEthics.pdf"
            fo = open(filepath, "rb")
            filecontent = fo.read()
            pdf = base64.b64encode(filecontent)
            pdf_attachement = {
            'type':'application/pdf',
            'content':pdf,
            'name':filename
            }
            context_dict = {
                'Name': user.profile.first_name,
                'Url':NEXT_URL_LINK,
                'Username': user.profile.email,
                'Password': user_password
            }
            send_mandrill_email_with_attachement(
                'ABOTMI_04', 
                [communication_email],
                pdf_attachement, 
                context=context_dict
            )
            send_mandrill_email(
                'REIA_16_02', 
                [communication_email], 
                context={
                    'username': user.profile.first_name, 
                    'promocode':dynamic_promo_code 
                }
            )
        else:
            send_mandrill_email(
                'ABOTMI_05', 
                [communication_email], 
                context={'name': user.profile.first_name}
            )
    except:
        is_mail_sent = False
    user.save()
    user_profile.save()
    advisor.save()
    return is_mail_sent


@allow_nfadmin
def make_as_registered_advisor(request):
    '''
        Admin is Making Advisor as a Register Advisor
    '''
    if request.method == 'POST':
        user_id = request.POST['user_id']
        is_mail_sent = registered_advisor_email(user_id)
        if is_mail_sent:
            return HttpResponse('success')
        else:
            return HttpResponse('Mail Failure')
    else:
        return HttpResponse('you dont have access <a href="/nfadmin/">click here</a>')


@allow_nfadmin
def make_as_unregistered_advisor(request):
    '''
    Makgin advisor as Un-registered advisor
    '''
    if request.method == 'POST':
        user_id = request.POST['user_id']
        user_profile = UserProfile.objects.get(user_id = user_id)
        advisor_details = Advisor.objects.get(user_profile = user_profile)
        advisor_details.is_register_advisor = False
        advisor_details.save()
        return HttpResponse('success')
    else:
        return HttpResponse('you dont have access <a href="/nfadmin/">click here</a>')


@allow_nfadmin
def make_as_certified_advisor(request):
    '''
    Making advisor as Certified advisor
    '''
    if request.method == 'POST':
        user_id = request.POST['user_id']
        user_profile = UserProfile.objects.filter(
            user_id=user_id).select_related('advisor').first()
        advisor_details = user_profile.advisor
        if not advisor_details.wordpress_user_id:
            icore_wp_user_id = create_word_press_user(request)
            advisor_details.wordpress_user_id = icore_wp_user_id
        advisor_details.is_certified_advisor = True
        advisor_details.reia_level = constants.REIA_LEVEL_2
        advisor_details.save()
        # Level 3 Referral Points
        if user_profile.referred_by:
            beneficiary_obj = user_profile.referred_by.profile
            referral_obj = user_profile
            referral_points(beneficiary_obj,referral_obj,constants.CERTIFIED_ADVISOR)

        if user_profile.mobile:
            mobile_number=user_profile.mobile
            sms_status = get_sms_status(user_profile.status)
            if sms_status == True:
                # sending sms to user
                message = 'Dear '+user_profile.first_name+' ('\
                +user_profile.registration_id+'),Congrats! You are now a Certified UPWRDZ\
                 advisor. View your Digital Profile in www.upwrdz.com'
                sms_response = send_sms_alert(
                    mobile_number=mobile_number,
                    message_template=message
                )
        # sending email using communication email id
        communication_email = user_profile.email
        if user_profile.communication_email_id == 'secondary':
            communication_email = user_profile.secondary_email
        try:
            #-------------------Registered Advisor Mail--------
            send_mandrill_email(
                'ABOTMI_06', 
                [communication_email], 
                context={'Name': user_profile.first_name}
            )
        except:
            return HttpResponse('Mail Failure')

        return HttpResponse('success')
    else:
        return HttpResponse('you dont have access <a href="/nfadmin/">click here</a>')


@allow_nfadmin
def make_as_uncertified_advisor(request):
    '''
    Makgin advisor as Uncertified advisor
    '''
    if request.method == 'POST':
        user_id = request.POST['user_id']
        user_profile = UserProfile.objects.get(user_id = user_id)
        advisor_details = Advisor.objects.get(user_profile = user_profile)
        advisor_details.is_certified_advisor = False
        advisor_details.save()
        return HttpResponse('success')
    else:
        return HttpResponse('you dont have access <a href="/nfadmin/">click here</a>')


@allow_nfadmin
def certified_advisor(request):
    '''
    Making user as certified advisor and updating upwrdz/reia level
    '''
    if request.method == 'POST':
        ids = request.POST['id']
        status = 1
        user_profile = UserProfile.objects.get(user_id = ids)
        advisor_details = Advisor.objects.get(user_profile = user_profile)
        advisor_details.is_certified_advisor = status
        advisor_details.reia_level = constants.REIA_LEVEL_2
        advisor_details.save()
        return render_to_response('nfadmin/advisor_list_view.html',context)
    else:
        return HttpResponse('you dont have access <a href="/nfadmin/">click here</a>')


@allow_nfadmin
def make_aggrigate_advisor(request):
    '''
        Converting Advisor to Honorary Advisor
    '''
    if request.method == 'POST':
        user_id = request.POST['user_id']
        user_profile = UserProfile.objects.get(user_id = user_id)
        advisor = Advisor.objects.get(user_profile = user_profile)
        advisor.is_honorable_advisor = True
        advisor.save()
        if user_profile.mobile:
            mobile_number=user_profile.mobile
            sms_status = get_sms_status(user_profile.status)
            if sms_status == True:
                # sending sms to user
                message = 'Dear '+user_profile.first_name+' ('\
                +user_profile.registration_id+'),Congrats! You are now an Honorary UPWRDZ\
                 advisor. View your Digital Profile in www.upwrdz.com'
                sms_response = send_sms_alert(
                    mobile_number=mobile_number,
                    message_template=message
                )
        context = {
            'name' : user_profile.first_name
        }
        communication_email = user_profile.email
        if user_profile.communication_email_id == 'secondary':
            communication_email = user_profile.secondary_email
        try:
            send_mandrill_email('ABOTMI_07', [communication_email], context)
        except:
            return HttpResponse('Mail Failure')
        return HttpResponse('success')
    else:
        return HttpResponse('Access forbidden')


# CRISIL Application Process --------------------------------------------
@allow_nfadmin
def crisil_advisor_list(request):
    '''
    Loading CRISIL Applied advisors into crisil_advisor_list_view html
    '''
    context = RequestContext(request)
    crisil_advisor_list = Advisor.objects.filter(
            Q(is_register_advisor=True)
        ).exclude(
            Q(crisil_application_status__contains=constants.CRISIL_NOT_APPLIED) 
            | Q(crisil_application_status__contains=0)
        )
    context_dict = {
        'PRODUCT_NAME':settings.PRODUCT_NAME,
        'LOGIN_URL':settings.LOGIN_URL,
        'LOGOUT_URL': settings.LOGOUT_URL,
        'LOGIN_REDIRECT_URL':settings.LOGIN_URL,
        'crisil_advisor_list':crisil_advisor_list,
    }
    return render_to_response(
        'nfadmin/crisil_advisor_list_view.html', context_dict, context)


@allow_crisil_admin
def crisil_admin_panel(request):
    '''
    Loading CRISIL admin pannel
    '''
    context = RequestContext(request)
    crisil_advisor_list = Advisor.objects.filter(
            Q(is_register_advisor=True)
        ).exclude(
            Q(crisil_application_status__contains=constants.CRISIL_NOT_APPLIED)
            |Q(crisil_application_status__contains=constants.CRISIL_PAYMENT_SUBMITTED)
            |Q(crisil_application_status__contains=constants.CRISIL_GOT_CERTIFICATE)
            |Q(crisil_application_status__contains=constants.
                CRISIL_CERTIFICATE_IN_PROCESS)
            |Q(crisil_application_status__contains=constants
                .CRISIL_RENEWAL_CERTIFICATE_IN_PROCESS)
            |Q(crisil_application_status__contains=constants.CRISIL_VERIFICATION_FAILED)
            |Q(crisil_application_status__contains=constants.CRISIL_PAYMENT_RE_SUBMIT)
            |Q(crisil_application_status__contains=constants.CRISIL_EXPIRED)
            |Q(crisil_application_status__contains=constants.CRISIL_EXPIRED_BY_USER)
            |Q(crisil_application_status__contains=constants
                .CRISIL_RENEWAL_PAYMENT_SUBMITTED)
            |Q(crisil_application_status__contains=constants.CRISIL_RENEWAL)
            |Q(crisil_application_status__contains=0)
        )
    title = constants.APPLIED_ADVISORS
    context_dict = {
        'PRODUCT_NAME':settings.PRODUCT_NAME,
        'LOGIN_URL':settings.LOGIN_URL,
        'LOGOUT_URL': settings.LOGOUT_URL,
        'LOGIN_REDIRECT_URL':settings.LOGIN_URL,
        'crisil_advisor_list':crisil_advisor_list,
        'title':title
    }
    return render_to_response('nfadmin/crisil_admin_panel.html', context_dict, context)


@allow_crisil_admin
def crisil_payment_details(request):
    '''
    Loading Renewal Crisil advisors into crisil_admin_panel html
    '''
    context = RequestContext(request)
    crisil_advisor_list = Advisor.objects.filter(
            Q(is_register_advisor=True)
        ).exclude(
            Q(crisil_application_status__contains=constants.CRISIL_NOT_APPLIED)
            |Q(crisil_application_status__contains=constants.CRISIL_APPLIED)
            |Q(crisil_application_status__contains=constants.CRISIL_GOT_CERTIFICATE)
            |Q(crisil_application_status__contains=constants
                .CRISIL_CERTIFICATE_IN_PROCESS)
            |Q(crisil_application_status__contains=constants
                .CRISIL_RENEWAL_CERTIFICATE_IN_PROCESS)
            |Q(crisil_application_status__contains=constants.CRISIL_EXPIRED)
            |Q(crisil_application_status__contains=constants.CRISIL_EXPIRED_BY_USER)
            |Q(crisil_application_status__contains=constants.CRISIL_RENEWAL)
            |Q(crisil_application_status__contains=0)
            |Q(crisil_application_status = 'renewal_re_submit_details')
        )
    title = constants.CRISIL_PAYMENT_DETAILS
    context_dict = {
        'PRODUCT_NAME':settings.PRODUCT_NAME,
        'LOGIN_URL':settings.LOGIN_URL,
        'LOGOUT_URL': settings.LOGOUT_URL,
        'LOGIN_REDIRECT_URL':settings.LOGIN_URL,
        'crisil_advisor_list':crisil_advisor_list,
        'title':title
    }
    return render_to_response('nfadmin/crisil_admin_panel.html',context_dict,context)


@allow_crisil_admin
def crisil_verified(request):
    '''
    Loading CRISIL Verified advisors into crisil_admin_panel html
    '''
    context = RequestContext(request)
    crisil_advisor_list = Advisor.objects.filter(
            Q(is_register_advisor=True)
        ).exclude(
            Q(crisil_application_status__contains=constants.CRISIL_NOT_APPLIED)
            |Q(crisil_application_status__contains=constants.CRISIL_APPLIED)
            |Q(crisil_application_status__contains=constants.CRISIL_PAYMENT_SUBMITTED)
            |Q(crisil_application_status__contains=constants.CRISIL_VERIFICATION_FAILED)
            |Q(crisil_application_status__contains=constants.CRISIL_PAYMENT_RE_SUBMIT)
            |Q(crisil_application_status__contains=constants
                .CRISIL_RENEWAL_PAYMENT_SUBMITTED)
            |Q(crisil_application_status__contains=constants.CRISIL_EXPIRED)
            |Q(crisil_application_status__contains=constants.CRISIL_EXPIRED_BY_USER)
            |Q(crisil_application_status__contains=constants.CRISIL_RENEWAL)
            |Q(crisil_application_status__contains=0)
        )
    title = constants.CRISIL_VERIFIED_ADVISORS
    context_dict = {
        'PRODUCT_NAME':settings.PRODUCT_NAME,
        'LOGIN_URL':settings.LOGIN_URL,
        'LOGOUT_URL': settings.LOGOUT_URL,
        'LOGIN_REDIRECT_URL':settings.LOGIN_URL,
        'crisil_advisor_list':crisil_advisor_list,
        'title':title
    }
    return render_to_response('nfadmin/crisil_admin_panel.html',context_dict,context)


@allow_crisil_admin
def crisil_expired(request):
    '''
    Loading CRISIL Expired advisors into crisil_admin_panel html
    '''
    context = RequestContext(request)
    crisil_advisor_list = Advisor.objects.filter(
            Q(crisil_application_status__contains=constants.CRISIL_EXPIRED)).exclude(
            Q(crisil_application_status__contains=constants.CRISIL_EXPIRED_BY_USER)
        )
    title = constants.CRISIL_EXPIRED_ADVISORS
    context_dict = {
        'PRODUCT_NAME':settings.PRODUCT_NAME,
        'LOGIN_URL':settings.LOGIN_URL,
        'LOGOUT_URL': settings.LOGOUT_URL,
        'LOGIN_REDIRECT_URL':settings.LOGIN_URL,
        'crisil_advisor_list':crisil_advisor_list,
        'title':title
    }
    return render_to_response('nfadmin/crisil_admin_panel.html',context_dict,context)


@allow_crisil_admin
def crisil_renewal(request):
    '''
    Loading CRISIL Renewal advisors into crisil_admin_panel html
    '''
    context = RequestContext(request)
    crisil_advisor_list = Advisor.objects.filter(
        Q(crisil_application_status = constants.CRISIL_EXPIRED_BY_USER)
        |Q(crisil_application_status = constants.CRISIL_RENEWAL_PAYMENT_RE_SUBMIT)
    )
    title = constants.CRISIL_RENEWAL_ADVISORS
    context_dict = {
        'PRODUCT_NAME':settings.PRODUCT_NAME,
        'LOGIN_URL':settings.LOGIN_URL,
        'LOGOUT_URL': settings.LOGOUT_URL,
        'LOGIN_REDIRECT_URL':settings.LOGIN_URL,
        'crisil_advisor_list':crisil_advisor_list,
        'title':title
    }
    return render_to_response('nfadmin/crisil_admin_panel.html',context_dict,context)


def view_crisil_advisor_modal(request):
    '''
    Loading transaction details of CRISIL advisor into crisil_advisor_modal_view to view
    '''
    context = RequestContext(request)
    if request.method == 'POST':
        user_profile_id = request.POST['user_profile_id']
        user_profile_details = UserProfile.objects.get(pk=user_profile_id)
        transaction_details = TransactionsDetails.objects.get(
            user_profile = user_profile_id
        )
        description = ''
        if transaction_details.description:
            description = json.loads(transaction_details.description)
        upload_documents = UploadDocuments.objects.filter(
            user_profile_id=user_profile_id,
            documents_type='bank_details'
        ).order_by('id').reverse()[0]
        uploaded_documents = ''
        if upload_documents:
            uploaded_documents = upload_documents.documents
        context_dict = {
            'PRODUCT_NAME':settings.PRODUCT_NAME,
            'LOGIN_URL':settings.LOGIN_URL,
            'LOGOUT_URL': settings.LOGOUT_URL,
            'LOGIN_REDIRECT_URL':settings.LOGIN_URL,
            'user_profile_details':user_profile_details,
            'uploaded_documents' : uploaded_documents,
            'description' : description
        }
        return render_to_response(
            'nfadmin/crisil_advisor_modal_view.html', context_dict, context)


def edit_crisil_advisor_modal(request):
    '''
    Edit and save crisil applied user payment status
    '''
    context = RequestContext(request)
    if request.method == 'POST':
        user_profile_id = request.POST['username']
        invoice_id = request.POST['invoice_no']
        bank_name = request.POST['bank_name']
        cheque_dd_no = request.POST['cheque_dd_no']
        cheque_dd_date = request.POST['cheque_dd_date']
        amount = request.POST['amount']
        payment_received_date = request.POST['payment_received_date']
        payment_status = request.POST['payment_status']
        remark = request.POST['remarks']
        user_profile_obj = UserProfile.objects.get(email=user_profile_id)
        advisor_obj = Advisor.objects.get(user_profile = user_profile_obj)
        #===========Send mail information=============
        communication_email = user_profile_obj.email
        name = user_profile_obj.first_name+" "+user_profile_obj.last_name
        if user_profile_obj.communication_email_id == 'secondary':
            communication_email = user_profile_obj.secondary_email
        amount_in_words = num2words(float(amount), lang='en_IN')
        context_dict = {
            'advisor_name': name,
            'final_amount': amount,
            'final_amount_in_words': amount_in_words,
            'bank_name': bank_name,
            'reference_number': cheque_dd_no,
            'date_of_payment': cheque_dd_date,
            'amount': amount,
            'URL':settings.LOGIN_URL
        }
        if payment_status != "--Selected--":
            transaction_obj = TransactionsDetails.objects.get(invoice_number=invoice_id)
            transaction_obj.bank_name = bank_name
            transaction_obj.cheque_dd_no = cheque_dd_no
            transaction_obj.cheque_dd_date = cheque_dd_date
            transaction_obj.discounted_amount = amount
            # Checking the crisil application status
            if payment_status == constants.TR_RENEWAL_BOUNCED \
                or payment_status == constants.TR_RENEWAL_INVALID:
                    application_status = constants.CRISIL_RENEWAL_PAYMENT_RE_SUBMIT
            elif payment_status == constants.TR_BOUNCED \
                or payment_status == constants.TR_INVALID:
                    application_status = constants.CRISIL_PAYMENT_RE_SUBMIT
            elif payment_status == constants.TR_RENEWAL_PAID:
                application_status = constants.CRISIL_RENEWAL_CERTIFICATE_IN_PROCESS
            else:
                application_status = constants.CRISIL_CERTIFICATE_IN_PROCESS
            # using payment status saving data and sending mail, messages
            if payment_status == constants.TR_PAID \
                or payment_status == constants.TR_RENEWAL_PAID:
                new_invoice_no = invoice_id
                if payment_status == constants.TR_RENEWAL_PAID:
                    new_invoice_no = invoice_gen(advisor_obj,transaction_obj)
                advisor_obj.crisil_application_status = application_status
                transaction_obj.status = payment_status
                transaction_obj.credited_date = payment_received_date
                transaction_obj.invoice_number = new_invoice_no
                transaction_obj.serial_no = int(new_invoice_no.split('-')[-1])
                MESSAGE = 'Dear '+user_profile_obj.first_name+' ('\
                +user_profile_obj.registration_id+'),Thanks for the payment towards \
                CRISIL verification'
                transaction_obj.save()
                # invoice genaration
                invoice_bill_pdf(
                    user_profile_obj,
                    new_invoice_no,
                    'REIA_17_04',
                    context_dict
                )
            if payment_status == constants.TR_BOUNCED \
                or payment_status == constants.TR_RENEWAL_BOUNCED:
                advisor_obj.crisil_application_status = application_status
                transaction_obj.status = payment_status
                description = {
                    "transaction_type":"Bank Details",
                    "remark":remark,
                    "no_of_years_selected":request.POST['hidden_years_selected'],
                    "offered_years":request.POST['hidden_offered_years']
                }
                description = json.dumps(description)
                transaction_obj.description = description
                MESSAGE = 'Dear '+user_profile_obj.first_name+' ('\
                +user_profile_obj.registration_id+'),We regret to inform that your cheque\
                 has returned. Make new payment and confirm.'
                mail_template = 'REIA_17_05'
                send_mandrill_email(
                    mail_template, [communication_email], context=context_dict)

            if payment_status == constants.TR_INVALID or payment_status == constants.TR_RENEWAL_INVALID:
                advisor_obj.crisil_application_status = application_status
                transaction_obj.status = payment_status
                description = {
                    "transaction_type":"Bank Details",
                    "remark":remark,
                    "no_of_years_selected":request.POST['hidden_years_selected'],
                    "offered_years":request.POST['hidden_offered_years']
                }
                description = json.dumps(description)
                transaction_obj.description = description
                MESSAGE = 'We regret to inform that the payment details you entered are \
                not matching with our bank entries. Request you to upload the documents \
                again.'
                mail_template = 'REIA_17_06'
                send_mandrill_email(
                    mail_template, [communication_email], context=context_dict)
            transaction_obj.save()
            # sending alert sms
            if user_profile_obj.mobile and not payment_status == constants.TR_INVALID:
                mobile_number=user_profile_obj.mobile
                sms_status = get_sms_status(user_profile_obj)
                if sms_status == True:
                    # sending sms to logedin user
                    url = settings.SMS_URL
                    sms_response = send_sms_alert(
                        mobile_number=mobile_number, message_template=MESSAGE)
            advisor_obj.save()
        return HttpResponse('success')
    else:
        return HttpResponse('you dont have access <a href="/nfadmin/">click here</a>')


def crisil_certificate_modal(request):
    '''
    Show the crisil certificate modal
    '''
    crisil_form = CrisilCertificateForm()
    if request.method == 'POST':
        advisor_obj = Advisor.objects.get(pk=request.POST['advisor_id'])
        advisor_id = advisor_obj.id
        transaction_obj = TransactionsDetails.objects.get(
            user_profile = advisor_obj.user_profile
        )
        description = transaction_obj.description
        if description:
            description = json.loads(description)
            no_of_years_selected = description['no_of_years_selected']
            offered_years = description['offered_years']
        '''
            upload certificate and report of crisil document view
        '''
        try:
            user_upload_doc_obj1 = UploadDocuments.objects.filter(
                user_profile=advisor_obj.user_profile, 
                documents_type='crisil_report'
            ).order_by('-created_date')[0]
            crisil_report = user_upload_doc_obj1.documents
        except:
            crisil_report = ''
        '''
            crisil registration number and expire date view
        '''
        try:
            crisil_registration_number = \
                advisor_obj.crisil_certificate.crisil_registration_number
        except:
            crisil_registration_number = ''
        try:
            crisil_issued_date = advisor_obj.crisil_certificate.crisil_issued_date
        except:
            crisil_issued_date=''
        try:
            crisil_expiry_date = advisor_obj.crisil_certificate.crisil_expiry_date
        except:
            crisil_expiry_date=''

        initial_data = {
            'advisor_id': advisor_obj,
            'crisil_registration_number': crisil_registration_number,
            'crisil_issued_date' : crisil_issued_date,
            'crisil_expiry_date' : crisil_expiry_date,
            'no_of_years_selected' : no_of_years_selected,
            'offered_years' : offered_years
        }
        crisil_form = CrisilCertificateForm(initial_data)
        '''
        Load Modal Body with this form
        '''
        return render(request, 'nfadmin/crisil_certificate_modal.html', locals())


@allow_crisil_admin
def edit_crisil_certificate_modal(request):
    '''
    Edit and save crisil certificate.
    '''
    if request.method == 'POST':
        cr_advisor = Advisor.objects.get(pk=request.POST['advisor_id'])
        cr_transcation = TransactionsDetails.objects.filter(
            user_profile=cr_advisor.user_profile
        ).first()
        crisil_instance, tr_status = CrisilCertifications.objects.get_or_create(
            advisor_id=cr_advisor, 
            transcation_id=cr_transcation
        )
        crisil_form = CrisilCertificateForm(
            request.POST,
            request.FILES, 
            instance=crisil_instance
        )
        user_profile_obj = cr_advisor.user_profile
        #===========Send mail information=============
        communication_email = user_profile_obj.email
        name = user_profile_obj.first_name+" "+user_profile_obj.last_name
        if user_profile_obj.communication_email_id == 'secondary':
            communication_email = user_profile_obj.secondary_email

        if crisil_form.is_valid():
            #============Creating Crisil record=====================
            crs_instance = crisil_form.save(commit=False)
            crisil_registration_number = request.POST['crisil_registration_number']
            crisil_expiry_date = crisil_form.cleaned_data['crisil_expiry_date']
            crisil_issued_date = crisil_form.cleaned_data['crisil_issued_date']
            crs_instance.save()
            #============upload crisil certificate and report=======
            crisil_report = request.FILES['crisil_report']

            documents_new_upload, status = UploadDocuments.objects.get_or_create(
                user_profile=cr_advisor.user_profile,
                registration_number=crisil_registration_number, 
                documents_type="crisil_report"
            )
            documents_new_upload.documents = request.FILES['crisil_report']
            documents_new_upload.documents_type = "crisil_report"
            documents_new_upload.save()

            #============Advisor crisil status update==============
            cr_advisor.crisil_application_status = constants.CRISIL_GOT_CERTIFICATE
            cr_advisor.crisil_registration_number = crisil_registration_number
            cr_advisor.crisil_expiry_date = crisil_expiry_date
            cr_advisor.is_crisil_verified = True
            cr_advisor.save()

            #==============Sending sms==================
            MESSAGE = 'Dear '+user_profile_obj.first_name+' ('\
            +user_profile_obj.registration_id+'), Your CRISIL verification is complete. \
            You may view your certificate in your dashboard in www.upwrdz.com'
            if user_profile_obj.mobile:
                mobile_number=user_profile_obj.mobile
                url = settings.SMS_URL
                sms_status = get_sms_status(user_profile_obj)
                if sms_status == True:
                    sms_response = send_sms_alert(
                        mobile_number=mobile_number, message_template=MESSAGE)
            #==============Sending mail==================
            context_dict = {
                'advisor_name': name
            }
            mail_template = 'REIA_17_07'
            send_mandrill_email(
                mail_template, [communication_email], context=context_dict)
            return HttpResponse('success')
        else:
            return HttpResponse('failure')


def save_crisil_feedback(request):
    '''
    Description: Saving CRISIL feedback when Advisors CRISIL Verification is failed.
    '''
    if request.method == 'POST':
        advisor = Advisor.objects.get(pk = request.POST['advisor_id'])
        if advisor.crisil_application_status == \
            constants.CRISIL_RENEWAL_CERTIFICATE_IN_PROCESS:
            advisor.crisil_application_status = constants.CRISIL_EXPIRED_BY_USER
        else:
            advisor.crisil_application_status = constants.CRISIL_NOT_APPLIED
        advisor.save()
        transaction_details = TransactionsDetails.objects.get(
            user_profile = advisor.user_profile)
        no_of_years_selected = ''
        offered_years = ''
        if transaction_details.description:
            tran_description = json.loads(transaction_details.description)
            no_of_years_selected = tran_description['no_of_years_selected']
            offered_years = tran_description['offered_years']
        description = {
            "transaction_type":"Bank Details",
            "remark":request.POST['advisors_crisil_feedback'],
            "no_of_years_selected":no_of_years_selected,
            "offered_years":offered_years
        }
        description = json.dumps(description)
        transaction_details.description = description
        transaction_details.save()
        context={
            'Advisor_name':advisor.user_profile.first_name
        }
        send_mandrill_email('REIA_17_10', [advisor.user_profile.email], context)
        return HttpResponse('success')
    else:
        return HttpResponse('Access forbidden')


def view_crisil_failed_feedback(request):
    '''
    Description: Sending feedback to the nfadmin for view
    '''
    if request.method == 'POST':
        advisor = Advisor.objects.get(pk=request.POST['advisor_id'])
        transaction_obj = TransactionsDetails.objects.get(
            user_profile = advisor.user_profile
        )
        feedback = ''
        if transaction_obj.description:
            description = json.loads(transaction_obj.description)
            feedback = description['remark']
        return HttpResponse(feedback)


@allow_nfadmin
def affiliated_companies(request):
    '''
    description: sending invitation mail for registering a company
    '''
    LOGOUT_URL = settings.LOGOUT_URL
    company_obj = AffiliatedCompany.objects.all()
    return render(request, 'nfadmin/affiliated_companies_list_view.html', locals())


@allow_nfadmin
def send_mail_to_company(request):
    '''
    description: sending invitation mail for registering a company
    '''
    if request.method == 'POST':
        email = request.POST['email_id']
        company_name = request.POST['company_name']
        company_id = request.POST['company_id']
        company = AffiliatedCompany.objects.filter(id = company_id)
        if company:
            company[0].company_name = company_name
            company[0].save()
            user_profile = UserProfile.objects.filter(id = company[0].user_profile_id)
            if user_profile:
                user_profile[0].email = email
                user_profile[0].save()
                user = User.objects.filter(id = user_profile[0].user_id)
                if user:
                    user[0].username = email
                    user[0].email = email
                    user[0].save()
                else:
                    HttpResponse('failed')
            else:
                return HttpResponse('failed')
        else:
            return HttpResponse('failed')
        '''
            Generating Activaton Link
        '''
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        activation_key = hashlib.sha1(salt+user_profile[0].email).hexdigest()
        key_expires = datetime.datetime.today() + datetime.timedelta(2)
        try:
            verification = EmailVerification.objects.get(user_profile=user[0].profile)
            verification.activation_key=activation_key
            verification.key_expires=key_expires
            verification.save()
        except ObjectDoesNotExist:
            verification = EmailVerification(
                user_profile=user_profile[0], 
                activation_key=activation_key, 
                key_expires=key_expires
            )
            verification.save()
        '''
            Activaton Link mail
        '''
        try:
            send_mandrill_email(
                'REIA_19_01', 
                [user_profile[0].email], 
                context={
                    'company_name':company_name, 
                    'url':settings.DEFAULT_DOMAIN_URL+"/company/?ack="+activation_key
                }
            )
        except:
            return HttpResponse('mailfailed')
        return HttpResponse('success')
    else:
        return HttpResponse('Access forbidden')


@allow_nfadmin
def resend_mail_to_company(request):
    '''
    Resending activation link to Company email
    '''
    if request.method == 'POST':
        email = request.POST['email_id']
        company_name = request.POST['company_name']
        company_id = request.POST['company_id']
        company = AffiliatedCompany.objects.filter(id = company_id)
        if company:
            user_profile = UserProfile.objects.filter(id = company[0].user_profile_id)
            if user_profile:
                user = User.objects.filter(id = user_profile[0].user_id)
            else:
                return HttpResponse('failed')
        else:
            return HttpResponse('failed')
        '''
            Generating Activaton Link
        '''
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        activation_key = hashlib.sha1(salt+user_profile[0].email).hexdigest()
        key_expires = datetime.datetime.today() + datetime.timedelta(2)
        try:
            verification = EmailVerification.objects.get(user_profile=user[0].profile)
            verification.activation_key=activation_key
            verification.key_expires=key_expires
            verification.save()
        except ObjectDoesNotExist:
            verification = EmailVerification(
                user_profile=user_profile[0], 
                activation_key=activation_key, 
                key_expires=key_expires
            )
            verification.save()
        '''
            Activaton Link mail
        '''
        try:
            send_mandrill_email(
                'REIA_19_01', 
                [user_profile[0].email], 
                context={
                    'company_name':company_name, 
                    'url':settings.DEFAULT_DOMAIN_URL+"/company/?ack="+activation_key
                }
            )
        except:
            return HttpResponse('mailfailed')
        return HttpResponse('success')
    else:
        return HttpResponse('Access forbidden')


def view_company_details(request):
    '''
    Descrption: Fetching Company Details
    '''
    if request.method == 'POST':
        user_profile_id = request.POST['id']
        company = ''
        if user_profile_id:
            company = AffiliatedCompany.objects.filter(user_profile_id = user_profile_id)
            user_profile = UserProfile.objects.filter(id = user_profile_id)
            if company:
                company_obj = company[0]
                awards_or_rewards = ''
                if company_obj.awards_or_rewards:
                    awards_or_rewards = json.loads(company_obj.awards_or_rewards)
                user_profile = user_profile[0]
        return render(request, 'nfadmin/view_company_details.html', locals())
    else:
        return HttpResponse('Access forbidden')


def view_company_details_resend(request):
    '''
    Descrption: Fetching Company Details
    '''
    if request.method == 'POST':
        user_profile_id = request.POST['id']
        company = ''
        if user_profile_id:
            company = AffiliatedCompany.objects.filter(user_profile_id = user_profile_id)
            user_profile = UserProfile.objects.filter(id = user_profile_id)
            company_details ={
                'email':user_profile[0].email,
                'company_name':company[0].company_name
            }
        return JsonResponse(company_details)
    else:
        return HttpResponse('Access forbidden')


def get_company_activation(request):
    '''
    Checking activation link is exists or not
    '''
    if request.method == 'POST':
        company_id = request.POST['company_id']
        company = AffiliatedCompany.objects.filter(id = company_id)
        if company:
            user_profile = UserProfile.objects.filter(id = company[0].user_profile_id)
            verification = EmailVerification.objects.filter(user_profile=user_profile[0])
            result=''
            if verification:
                result='success'
            return HttpResponse(result)
        else:
            return HttpResponse('Access forbidden')


def create_company(request):
    '''
    Creating company in database using company url
    '''
    if request.method == 'POST':
        company_url = request.POST['company_url']
        domain = company_url.split("//")[-1].split("/")[0]
        domain = 'http://'+domain
        domain_name=get_tld(domain)
        company_name = domain_name
        domain_name = 'contact@'+domain_name
        user_password = get_random_string(length=8)
        user,created = User.objects.get_or_create(username = domain_name)
        if created:
            user.email  = domain_name
            user.set_password = user_password
            user.is_active = True
            user.is_staff = True
            user.save()
        user_profile = user.profile
        user_profile.email = domain_name
        user_profile.is_company = True
        user_profile.save()
        company_obj,status = AffiliatedCompany.objects.get_or_create(
            user_profile = user_profile)
        if status:
            company_obj.contact = company_name
            company_obj.save()
        return HttpResponse('success')
    else:
        return HttpResponse('Access forbidden')


@allow_nfadmin
def company_spoc(request):
    '''
    Loading Companies into company_spoc_list html
    '''
    LOGOUT_URL = settings.LOGOUT_URL
    company_obj = AffiliatedCompany.objects.all().values('user_profile')
    user_basic_details = UserProfile.objects.filter(id__in = company_obj)
    return render(request, 'nfadmin/company_spoc_list.html', locals())


@allow_nfadmin
def advisor_video_request(request):
    '''
    Get list of all advisors who requests for video shoot
    '''
    context = RequestContext(request)
    video_request = AdvisorVideoRequest.objects.all()
    context_dict = {
        'PRODUCT_NAME':settings.PRODUCT_NAME,
        'LOGIN_URL':settings.LOGIN_URL,
        'LOGOUT_URL': settings.LOGOUT_URL,
        'LOGIN_REDIRECT_URL':settings.LOGIN_URL,
        'VIDEO_REQUEST_STATUS':constants.VIDEO_REQUEST_STATUS,
        'VIDEO_REQUEST_APPROVED':constants.VIDEO_REQUEST_APPROVED,
        'video_request':video_request,
    }
    return render_to_response(
        'nfadmin/advisor_videorequest_list_view.html', context_dict, context)


@allow_nfadmin
def view_video_request_details(request):
    '''
    Get details video requests for shoot
    '''
    context = RequestContext(request)
    if request.method == 'POST':
        user_profile_id = request.POST.get('advisor_id', None)
        video_id = request.POST.get('video_id', None)
        video_request_details = AdvisorVideoRequest.objects.filter(
            user_profile = user_profile_id, 
            id=video_id
        ).first()
        return render(request, 'nfadmin/view_video_request_details.html', locals())
    else:
        return HttpResponse('Access forbidden')


@allow_nfadmin
def approve_video_request(request):
    '''
    Approve advisor video request
    '''
    if request.method == "POST":
        advisor_id = request.POST.get('advisor_id', None)
        update_status = AdvisorVideoRequest.objects.filter(id=advisor_id).first()
        if update_status:
            update_status.status = constants.VIDEO_REQUEST_APPROVED
            update_status.save()
    return HttpResponse('success')


@allow_nfadmin
def advisor_video_publish(request):
    '''
    Get all the list of advisor who uploaded published youtube video
    '''
    context = RequestContext(request)
    video_publish_details = AdvisorPublishedVideo.objects.all()
    context_dict = {
        'PRODUCT_NAME':settings.PRODUCT_NAME,
        'LOGIN_URL':settings.LOGIN_URL,
        'LOGOUT_URL': settings.LOGOUT_URL,
        'LOGIN_REDIRECT_URL':settings.LOGIN_URL,
        'VIDEO_PUBLISH_STATUS':constants.VIDEO_PUBLISH_STATUS,
        'VIDEO_PUBLISH_APPROVED':constants.VIDEO_PUBLISH_APPROVED,
        'VIDEO_PUBLISH_REJECTED':constants.VIDEO_PUBLISH_REJECTED,
        'video_publish_details':video_publish_details,
    }
    return render_to_response(
        'nfadmin/advisor_video_published_list_view.html', context_dict, context)


def video_publish_approved(request):
    '''
    Approve Video published by advisor
    '''
    id = request.POST.get("id", None)
    video_publish_approved = AdvisorPublishedVideo.objects.filter(id=id).first()
    if video_publish_approved:
        video_publish_approved.status = constants.VIDEO_PUBLISH_APPROVED
        video_publish_approved.save()
    return HttpResponse('success')


def video_publish_reject(request):
    '''
    Reject Video published by advisor
    '''
    id = request.POST.get("id", None)
    video_publish_reject = AdvisorPublishedVideo.objects.filter(id=id).first()
    if video_publish_reject:
        video_publish_reject.status = constants.VIDEO_PUBLISH_REJECTED
        video_publish_reject.save()
    return HttpResponse('success')


@allow_nfadmin
def upload_company_excel_file(request):
    '''
    Upload Company Excel File and creating companies
    '''
    file_to_upload = request.FILES['company_data_file']
    file_name = file_to_upload.name
    try:
        with open(file_name, "wb") as fh:
            fh.write(file_to_upload.read())
            fh.close()
        # reading the excel file
        company_data = pd.read_excel(file_name)
        for company_instance in range(len(company_data)):
            company_email = company_data.loc[company_instance].email.strip()
            if str(company_email) == "nan" or str(company_email) == "":
                company_email = None
            if company_email:
                company_email = company_email.split(",")[0]
                user,status = User.objects.get_or_create(
                    username=company_email, 
                    email=company_email
                )
                user.is_active = True
                user.is_staff = True
                user_profile = user.profile
                user_profile.email = company_email
                user_profile.is_company = True

                company_name = str(company_data.loc[company_instance].user_name).strip()
                source = str(company_data.loc[company_instance].source).strip()
                membership_type = str(
                    company_data.loc[company_instance].membership_type).strip()
                segment = str(company_data.loc[company_instance].segment).strip()
                corprate_identity_no = str(company_data.loc[company_instance].cin).strip()
                registered_location = str(company_data.loc[company_instance].roc).strip()
                registration_no = str(
                    company_data.loc[company_instance].registration_number).strip()
                company_category = str(
                    company_data.loc[company_instance].company_category).strip()
                company_sub_category = str(
                    company_data.loc[company_instance].company_sub_category).strip()
                class_of_company = str(
                    company_data.loc[company_instance].class_of_company).strip()
                date_of_incorporation = \
                    company_data.loc[company_instance].date_of_incorporation
                try:
                    date_of_incorporation =  date_of_incorporation.date()
                except Exception as e:
                    date_of_incorporation = None
                activity = str(company_data.loc[company_instance].activity).strip()
                board_of_directors = str(
                    company_data.loc[company_instance].board_of_directors).strip()
                description = company_data.loc[company_instance].company_brief
                rbi_no = str(company_data.loc[company_instance].rbi_no).strip()
                if rbi_no == "nan" or rbi_no == "":
                    rbi_no = ""
                nse_no = str(company_data.loc[company_instance].nse_no).strip()
                if nse_no == "nan" or nse_no == "":
                    nse_no = ""
                bse_no = str(company_data.loc[company_instance].bse_no).strip()
                if bse_no == "nan" or bse_no == "":
                    bse_no = ""
                irda_no = str(company_data.loc[company_instance].irda_no).strip()
                if irda_no == "nan" or irda_no == "":
                    irda_no = ""
                reg_office = company_data.loc[company_instance].reg_office
                corporate_office = company_data.loc[company_instance].corporate_office
                contact_number = str(
                    company_data.loc[company_instance].contact_no).strip()
                branches_office_establishment = str(
                    company_data.loc[company_instance].branch_office)
                if branches_office_establishment == "nan" \
                    or branches_office_establishment == "":
                    branches_office_establishment = None
                if branches_office_establishment:
                    branches_office_establishment = int(
                        branches_office_establishment
                            .split("-")[-1]
                            .strip()
                            .replace(",", "")
                            .strip("+")
                            .split(".")[0]
                    )
                franchisee_office_establishment = str(
                    company_data.loc[company_instance].franchisee_office)
                if franchisee_office_establishment == "nan" \
                    or franchisee_office_establishment == "":
                    franchisee_office_establishment = None
                if franchisee_office_establishment:
                    franchisee_office_establishment = int(
                        franchisee_office_establishment.split("-")[-1]
                            .strip()
                            .replace(",", "")
                            .strip("+")
                            .split(".")[0]
                    )
                authorized_capital = str(
                    company_data.loc[company_instance].authorised_capital).strip()
                if authorized_capital == "nan" or authorized_capital == "":
                    authorized_capital = None
                if authorized_capital:
                    authorized_capital = float(
                        authorized_capital.split("-")[0]
                            .strip()
                            .replace(",", "")
                            .strip("+")
                    )
                paid_up_capital = str(
                    company_data.loc[company_instance].paidup_capital).strip()
                if paid_up_capital == "nan" or paid_up_capital == "":
                    paid_up_capital = None
                if paid_up_capital:
                    paid_up_capital = float(
                        paid_up_capital
                            .split("-")[0]
                            .strip()
                            .replace(",", "")
                            .strip("+")
                    )
                number_of_clients = str(
                    company_data.loc[company_instance].number_of_clients).strip()
                if number_of_clients == "nan" or number_of_clients == "":
                    number_of_clients = None
                if number_of_clients:
                    number_of_clients = int(
                        number_of_clients
                            .split("-")[-1]
                            .strip()
                            .replace(",", "")
                            .strip("+")
                            .split(".")[0]
                    )
                number_of_employee = str(
                    company_data.loc[company_instance].number_of_employees).strip()
                if number_of_employee == "nan" or number_of_employee == "":
                    number_of_employee = None
                if number_of_employee:
                    number_of_employee = int(
                        number_of_employee
                            .split("-")[-1]
                            .strip()
                            .replace(",", "")
                            .strip("+")
                            .split(".")[0]
                    )
                awards_or_rewards = company_data.loc[company_instance].awards_or_rewards
                if str(awards_or_rewards) == "nan" or str(awards_or_rewards) == "":
                    awards_or_rewards = None
                registration_details = {
                    "rbi":rbi_no,
                    "sebi_nse":nse_no,
                    "sebi_bse":bse_no,
                    "irda":irda_no
                }
                registration_details = json.dumps(registration_details)
                address = {
                    "registration_office":reg_office,
                    "corporate_office":corporate_office
                }
                address = json.dumps(address)
                if awards_or_rewards:
                    awards_or_rewards_json = {
                        "awards_or_rewards":awards_or_rewards
                    }
                affliated_company,status_af = AffiliatedCompany.objects.get_or_create(
                    user_profile=user_profile)
                affliated_company.company_name = company_name
                affliated_company.website_url = source
                affliated_company.domain_name = get_tld(source)
                affliated_company.membership_type = membership_type
                affliated_company.segment = segment
                affliated_company.corprate_identity_no = corprate_identity_no
                affliated_company.registered_location = registered_location
                affliated_company.registration_no = registration_no
                affliated_company.company_category = company_category
                affliated_company.company_sub_category = company_sub_category
                affliated_company.class_of_company = class_of_company
                if date_of_incorporation:
                    affliated_company.date_of_incorporation = date_of_incorporation
                affliated_company.activity = activity
                affliated_company.board_of_directors = board_of_directors
                affliated_company.description = description
                affliated_company.registered_under_and_no = registration_details
                affliated_company.address = address

                affliated_company.contact_number = contact_number
                if branches_office_establishment:
                    affliated_company.branches_office_establishment = branches_office_establishment
                if franchisee_office_establishment:
                    affliated_company.franchisee_office_establishment = franchisee_office_establishment
                if authorized_capital:
                    affliated_company.authorized_capital = authorized_capital
                if paid_up_capital:
                    affliated_company.paid_up_capital = paid_up_capital
                if number_of_clients:
                    affliated_company.number_clients = number_of_clients
                if number_of_employee:
                    affliated_company.number_of_employee = number_of_employee

                if affliated_company.awards_or_rewards:
                    awards_rewards_list = json.loads(affliated_company.awards_or_rewards)
                    awards_rewards_list.append(awards_or_rewards_json)
                    awards_or_rewards = json.dumps(awards_rewards_list)
                else:
                    awards_or_rewards = []
                    awards_or_rewards.append(awards_or_rewards_json)
                    affliated_company.awards_or_rewards = json.dumps(awards_or_rewards)
                user.save()
                user_profile.save()
                affliated_company.save()
        os.remove(os.path.realpath(file_name))
        return HttpResponse('success')
    except Exception as e:
        os.remove(os.path.realpath(file_name))
        return HttpResponse('failed, try again!!')


@allow_nfadmin
def subscription_package(request):
    '''
    Listing/Adding Features into Packages
    GET:
        -> Loading all subscription packages into subscription_package_list html
    POST:
        -> Adding the feature in to package
    '''
    if request.method == 'GET':
        pkg_list = SubscriptionPackageMaster.objects.all()
        return render(request, 'nfadmin/subscription_package_list.html', locals())

    if request.method == 'POST':
        category =  request.POST.get('category',None)
        price = request.POST.get('price',None)
        feature_data = request.POST.get('feature_data',None)
        category = category.split('---')
        category_id = category[0]
        pack_type = category[1][:3]
        obj= SubscriptionPackageMaster.objects.all().order_by('-id')[0]
        seq = int(obj.package_code.split('_')[3])+1
        category_obj = SubscriptionCategoryMaster.objects.filter(id = category_id).first()
        formt = category_obj.category_name[:2]+"_PKG_"+pack_type
        seq_id = formt+"_"+str(seq)
        packs, created = SubscriptionPackageMaster.objects.get_or_create(
            package_code = seq_id
        )
        packs.package_name = formt
        if price:
            packs.package_amount = price
        packs.package_duration = 1
        packs.package_type = category[1]
        packs.subscription_category = category_obj
        packs.feature_data = feature_data
        packs.save()
    return HttpResponse("success")


@allow_nfadmin
def get_feature_list(request):
    '''
    Getting features under catogery
    '''
    if request.method == 'POST':
        category = request.POST.get('category', None)
        category = category.split('---')[0]
        feature_obj = FeatureListMaster.objects.filter(subscription_category=category)
        feature_list = []
        for content in feature_obj:
            feature_data = {}
            feature_data['feature_name'] = content.feature_name
            feature_data['short_name'] = content.feature_short_name
            feature_list.append(feature_data)
        feature_list = json.dumps(feature_list)
        return HttpResponse(feature_list)
    else:
        return HttpResponse("Access Forbidden")


@allow_nfadmin
def list_regulatory_registration_docs_uploaded(request):
    '''
    Loading the Regulatory Registration details in registration_doc_uploaded_advisor_list
    html
    '''
    if request.method == 'GET':
        sebi_doc_uploaded_list = UploadDocuments.objects.filter(
            documents_type='sebi_certificate').values('user_profile')
        amfi_doc_uploaded_list = UploadDocuments.objects.filter(
            documents_type='amfi_certificate').values('user_profile')
        irda_doc_uploaded_list = UploadDocuments.objects.filter(
            documents_type='irda_certificate').values('user_profile')
        others_doc_uploaded_list = UploadDocuments.objects.filter(
            documents_type='others_certificate').values('user_profile')
        rera_doc_uploaded_list = UploadDocuments.objects.filter(
            documents_type='rera_certificate').values('user_profile')

        sebi_profile = UserProfile.objects.filter(id__in = sebi_doc_uploaded_list)
        amfi_profile = UserProfile.objects.filter(id__in = amfi_doc_uploaded_list)
        irda_profile = UserProfile.objects.filter(id__in = irda_doc_uploaded_list)
        others_profile = UserProfile.objects.filter(id__in = others_doc_uploaded_list)
        rera_profile = UserProfile.objects.filter(id__in = rera_doc_uploaded_list)

        sebi_data = GetNotApprovedRegulatory(
            sebi_profile, many=True, context={'reg_type':'SEBI'}
        ).data
        amfi_data = GetNotApprovedRegulatory(
            amfi_profile, many=True, context={'reg_type':'AMFI'}
        ).data
        irda_data = GetNotApprovedRegulatory(
            irda_profile, many=True, context={'reg_type':'IRDA'}
        ).data
        regulatory_others_data = GetNotApprovedRegulatory(
            others_profile, many=True, context={'reg_type':'others'}
        ).data
        regulatory_rera_data = GetNotApprovedRegulatory(
            rera_profile, many=True, context={'reg_type':'rera'}
        ).data

        return render(
            request, 'nfadmin/registration_doc_uploaded_advisor_list.html', locals())


@allow_nfadmin
def verify_uploaded_regulatory_document(request):
    '''
    Verifying the advisors Regulatory registration documents
    '''
    if request.method == 'POST':
        advisor_email = request.POST.get("adv_email", None)
        reg_doc_type = request.POST.get("doc_type", None)
        user_profile_obj = UserProfile.objects.filter(email = advisor_email)
        if advisor_email:
            user_status_obj = UserStatus.objects.filter(
                user_profile = user_profile_obj
            ).first()
            if user_status_obj:
                if reg_doc_type == 'sebi':
                    user_status_obj.sebi_status = 'verified'
                elif reg_doc_type == 'amfi':
                    user_status_obj.amfi_status = 'verified'
                elif reg_doc_type == 'irda':
                    user_status_obj.irda_status = 'verified'
                elif reg_doc_type == 'others':
                    user_status_obj.regulatory_other_status = 'verified'
                else:
                    return HttpResponse('failure')
                user_status_obj.save()
                return HttpResponse('success')
            else:
                return HttpResponse('failure')
        return HttpResponse('failure')


@allow_nfadmin
def verify_uploaded_regulatory_renewal_document(request):
    '''
    Verifying the advisors Regulatory registration renewal documents
    '''
    regulatory_renewal_certificate = request.POST.get("regulatory_document", None)
    user_email = request.POST.get("email_id", None)
    reg_renewal_doc_type = request.POST.get("renewal_doc_type", None)
    reg_renewal_doc_status = request.POST.get("renewal_doc_status", None)
    user_profile_obj = UserProfile.objects.filter(email = user_email)
    if regulatory_renewal_certificate:
        upload_obj = UploadDocuments.objects.filter(
            user_profile = user_profile_obj, 
            documents=regulatory_renewal_certificate
        ).first()
        if upload_obj:
            upload_obj.status = reg_renewal_doc_status
            upload_obj.save()
            return HttpResponse('success')
        else:
            return HttpResponse('failure')
    return HttpResponse('failure')


@allow_nfadmin
def reject_uploaded_regulatory_document(request):
    '''
    Rejecting the uploaded advisors Regulatory registraion documents
    '''
    if request.method == 'POST':
        advisor_email = request.POST.get("adv_email", None)
        reg_doc_type = request.POST.get("doc_type", None)
        user_profile_obj = UserProfile.objects.filter(email = advisor_email)
        if advisor_email:
            user_status_obj = UserStatus.objects.filter(
                user_profile = user_profile_obj
            ).first()
            if user_status_obj:
                if reg_doc_type == 'sebi':
                    user_status_obj.sebi_status = 'rejected'
                elif reg_doc_type == 'amfi':
                    user_status_obj.amfi_status = 'rejected'
                elif reg_doc_type == 'irda':
                    user_status_obj.irda_status = 'rejected'
                elif reg_doc_type == 'others':
                    user_status_obj.regulatory_other_status = 'rejected'
                else:
                    return HttpResponse('failure')
                user_status_obj.save()
                return HttpResponse('success')
            else:
                return HttpResponse('failure')
        return HttpResponse('failure')


@allow_nfadmin
def educational_authentication(request):
    '''
    Listing users with uploaded educational documents
    '''
    if request.method == 'GET':
        heighest_edu_doc_url = None
        updoc_obj = UploadDocuments.objects.filter(
            documents_type='highest_qualification_upload').values('user_profile')
        user_profile_obj = UserProfile.objects.filter(id__in = updoc_obj)
        education_data = GetAdditionalQualificationDocs(
            user_profile_obj, many=True).data
        return render(request, 'nfadmin/educational_certification_list.html', locals())


@allow_nfadmin
def load_additional_qual_list(request):
    '''
    Loading advisors additional qualification json
    '''
    if request.method == 'POST':
        user_email = request.POST.get('user_email', None)
        add_edu_qua_list = None
        if user_email:
            user_prof = UserProfile.objects.filter(email = user_email).first()
            email_user = user_prof.email
            add_edu_qua_list = json.loads(user_prof.additional_qualification)
            for add in add_edu_qua_list:
                if add['documents_upload']:
                    upload_obj = UploadDocuments.objects.filter(
                        id=add['documents_upload']
                    ).first()
                    add['doc_status'] = upload_obj.status
        else:
           add_edu_qua_list = ''
        return render(
            request, 'nfadmin/view_additional_qualification_modal.html', locals())
    else:
        return HttpResponse('you dont have access <a href="/nfadmin/">click here</a>')


@allow_nfadmin
def get_additional_qual_doc_url(request):
    '''
    Getting additional qualification documents
    '''
    if request.method == 'POST':
        docu_name = request.POST.get('doc_name', None)
        edu_qua_user_email = request.POST.get('edu_qua_user_email', None)
        additional_doc_url = None
        if docu_name:
            user_profile = UserProfile.objects.get(email = edu_qua_user_email)
            document = UploadDocumentsFunctions(request, user_profile)
            addi_doc = document.get_document(document_type=docu_name)
            if addi_doc:
                additional_doc_url = addi_doc.documents.url
            return HttpResponse(additional_doc_url)
        else:
            return HttpResponse('failure')
    else:
        return HttpResponse('you dont have access <a href="/nfadmin/">click here</a>')


@allow_nfadmin
def verify_heighest_qua_doc(request):
    '''
    Verifying the Highest educational qualification documents
    '''
    if request.method == 'POST':
        user_email = request.POST.get('user_email', None)
        heighest_qua_doc_status = request.POST.get('doc_status', None)
        user_profile_obj = UserProfile.objects.filter(email = user_email)
        if user_profile_obj: 
            userstatus_obj = UserStatus.objects.filter(
                user_profile = user_profile_obj
            ).first()
            if userstatus_obj:
                userstatus_obj.highest_qualification_status = heighest_qua_doc_status
                userstatus_obj.save()
        return HttpResponse('success')


@allow_nfadmin
def verify_additional_qua_document(request):
    '''
    Verifing the additional qualification documents
    '''
    if request.method == 'POST':
        additional_doc_name = request.POST.get('add_doc_name', None)
        additional_doc_status = request.POST.get('doc_status', None)
        edu_qua_user_email = request.POST.get('email_id', None)
        user_profile = UserProfile.objects.get(email = edu_qua_user_email)
        userstatus_obj = UserStatus.objects.filter(user_profile = user_profile).first()
        if userstatus_obj.highest_qualification_status == 'verified':
            if additional_doc_name:
                doc_obj = UploadDocuments.objects.filter(
                    user_profile = user_profile, 
                    documents_type=additional_doc_name
                )
                if doc_obj:
                    doc_obj[0].status = additional_doc_status
                    doc_obj[0].save()
                return HttpResponse('success')
            else:
                return HttpResponse('failure')
        else:
            return HttpResponse('false')
    else:
        return HttpResponse('you dont have access <a href="/nfadmin/">click here</a>')


@allow_nfadmin
def load_rera_regulatory_list(request):
    '''
    Loading the RERA Regulatory registration details
    '''
    if request.method == 'POST':
        user_email = request.POST.get('user_email', None)
        add_edu_qua_list = None
        rera_renewal_doc_arr = []
        create_renewal_docs = []
        if user_email:
            user_prof = UserProfile.objects.filter(email = user_email).first()
            document = UploadDocumentsFunctions(request, user_prof)
            rera_advisor = user_prof.advisor
            rera_details = rera_advisor.rera_details
            json_rera_details = json.loads(rera_details)
            for arr in json_rera_details:
                upload_obj = document.get_document(
                    doc_id=arr['rera_certificate']
                )
                arr['certification_document'] = upload_obj
                renewal_doc_ids = arr.get('rera_renewal_certificate', None)
                if renewal_doc_ids:
                    renewal_upload_objects = document.get_document(
                        doc_id=renewal_doc_ids.split(","), 
                        many=True
                    )
                else:
                    renewal_upload_objects = None
                arr['rera_renewal_records'] = renewal_upload_objects
            del(document)
        else:
           add_edu_qua_list = ''
        return render(request, 'nfadmin/view_rera_regulatory_modal.html', locals())
    else:
        return HttpResponse('you dont have access <a href="/nfadmin/">click here</a>')

@allow_nfadmin
def publish_newsletter(request):

    if request.method == 'GET':
        noticeBoard_list = NoticeBoard.objects.all()
        return render(request, 'nfadmin/newsletter_form_list.html', locals())

    if request.method == 'POST':
        news_type = request.POST.get('news_type')
        notice_date = request.POST.get('notice_date')
        headline = request.POST.get('headline')
        notice = request.POST.get('notice')
        notice_date_parsed = parse_date(notice_date)
        noticeboard = NoticeBoard(news_type=news_type
                                  , notice_date=notice_date_parsed,
                                  headline=headline, notice=notice)
        noticeboard.save()
        return redirect('/nfadmin/publish_newsletter')


@allow_nfadmin
def publish_testimonial(request):

    if request.method == 'GET':
        testimonial_list = Testimonial.objects.all()
        return render(request, 'nfadmin/testimonial_form_list.html', locals())
    if request.method == 'POST':
        picture_path = None
        testimonial_id = request.POST.get('testimonial_id', None)
        headlines =  request.POST.get('headlines', None)
        description = request.POST.get('description', None)
        documents_type = request.POST.get('documents_type', None)
        picture = request.POST.get('id_pic', None)
        if picture:
            picture_path = upload_image_and_get_path(
                request.user.profile, documents_type, picture)
        endorser = request.POST.get('endorser', None)
        designation = request.POST.get('designation', None)
        company = request.POST.get('company', None)
        if not testimonial_id:
            testimonial_insert = Testimonial(
                ## <<<<<< Commented for future purpose >>>>>

                #headline=headlines,
                # endorser_designation=designation,
                description=description,
                picture=picture_path,
                endorser=endorser,
                endorser_company=company
            )
            testimonial_insert.save()
        else:
            testimonial_insert = Testimonial.objects.filter(id=testimonial_id).first()
            if testimonial_insert:
                # testimonial_insert.headline = headlines
                testimonial_insert.description = description
                testimonial_insert.endorser = endorser
                # testimonial_insert.endorser_designation = designation
                testimonial_insert.endorser_company = company
                if picture_path:
                    testimonial_insert.picture = picture_path
                testimonial_insert.save()
        return redirect('/nfadmin/publish_testimonial')


@allow_nfadmin
def delete_testimonial(request):
    if request.method == 'POST':
        testi_id = request.POST.get('ts_m_id', None)
        if testi_id:
            tes_ob = Testimonial.objects.filter(id=int(testi_id)).first()
            if tes_ob:
                tes_ob.delete()
                return HttpResponse(200)
            else:
                return HttpResponse(204)
        else:
            return HttpResponse(400)
    else:
        return HttpResponse(405)



@allow_nfadmin
def nfadmins_edit_or_view_form(request):

    '''
    edit the form
    '''


    if request.method == 'GET':
        return render(
            request, 'nfadmin/edit_or_create_testimonial.html', context={})
    
    if request.method == "POST":
        id =  request.POST.get('id', None)
        testimonial_obj = Testimonial.objects.filter(id=id).first()
        context_dict={
            "testimonial_obj": testimonial_obj
        }
        return render(
            request, 'nfadmin/edit_or_create_testimonial.html', context=context_dict)
