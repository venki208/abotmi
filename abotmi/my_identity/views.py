# Python lib
import datetime
import json
import logging
import requests
import random
import sys
from datetime import date
from time import gmtime, strftime

# django libs
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Count, Sum, Avg, Q
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.views.generic import View

# Database Models
from datacenter.models import (
    Advisor, EmailVerification, UserProfile,
    CrisilCertifications, UploadDocuments, India_Pincode, UserReferral, Country,
    ExternalUser, AdvisorRating, NoticeBoard, AffiliatedCompany, CompanyAdvisorMapping,
    PanNumberVerfication, GuestUser, DigitalFootPrint, UserStatus, AdvisorProfileShare,
    ProfileShareMapping, EducationAndCertificationDetails)
from advisor_check.models import IrdaData, SebiData, AmfiData

# Common Modules
from common.views import (
    check_crisil_advisor, logme, get_binary_image,
    Otp, get_advisor_level, UploadDocumentsFunctions, get_remove_rera_doc,
    EducationQualificationFunctions, get_ipinfo)
from common import constants
from common.notification.constants import VIEWED_PROFILE_NOTIFICATION, VIEWED_PROFILE
from advisor_check.common_views import AdvisorCheckCommonFunctions

# Dashboard Modules
from common.notification.views import NotificationFunctions
from api.serializers import ComapnySerializer

# Login Modules
from login.decorators import check_member_or_advisor
# signup app modules
from signup.djmail import send_mandrill_email_admin_subject, send_mandrill_email

logger = logging.getLogger(__name__)


@login_required()
@check_member_or_advisor()
def index(request, slug=None):
    '''
    Description: Rendering My identity page.
        Advisor can render this page with login or without login
    '''
    req_type = request.POST.get('req_type', None)
    profile_pic = None
    try:
        if request.user.is_authenticated() and not slug:
            user_data = request.user
            advisor_user_profile = user_data.profile
            advisor_obj = advisor_user_profile.advisor
            advisor_user_status = advisor_user_profile.status
            is_advisor_own_profile = True
            if advisor_user_profile.picture:
                profile_pic = advisor_user_profile.picture.url
        else:
            advisor_user_profile = UserProfile.objects.filter(
                batch_code=slug).first()
            if advisor_user_profile:
                advisor_obj = advisor_user_profile.advisor
                user_data = advisor_user_profile.user
                advisor_user_status = advisor_user_profile.status
                is_advisor_own_profile = False
                if advisor_user_profile.picture:
                    profile_pic = get_binary_image(advisor_user_profile)
            else:
                return HttpResponse('<center><h2>Profile match not found</h2></center>')
        title = constants.MY_IDENTITY
        DEFAULT_DOMAIN_URL = settings.DEFAULT_DOMAIN_URL
        recaptcha_key = constants.RECAPTCHA_KEY
        skills = ''

        '''
        Financial instrument/s
        '''
        fin_ins = advisor_obj.financial_instruments
        fin_ins = json.loads(fin_ins) if fin_ins else None

        '''
        Feedbacks
        '''
        feedbacks = ''
        feedbacks_list = []
        feedbacks = AdvisorRating.objects.filter(
            advisor=advisor_obj,
            user_type='member').exclude(Q(feedback='') | Q(feedback=None))[:2]
        if req_type == "mobile" and feedbacks:
            for feedback in feedbacks:
                temp = {}
                temp['feedback'] = feedback.feedback
                if feedback.existing_user_profile:
                    temp['name'] = feedback.existing_user_profile.first_name
                else:
                    temp['name'] = feedback.external_user.name
                feedbacks_list.append(temp)
        '''
        Advisor Rating and Ranking
        '''
        # Advisor Rating
        total_no_rated = 0
        total_no_invites_to_rate = 0
        final_peer_avg_rating = 0
        advisor_rate_invites = AdvisorRating.objects.filter(
            advisor=advisor_obj,
            user_type='advisor'
        )
        if advisor_rate_invites:
            total_no_invites_to_rate = advisor_rate_invites.count()
            total_no_rated = advisor_rate_invites.exclude(
                avg_rating__lte=0.0).count()
            final_peer_avg_rating = advisor_rate_invites.exclude(
                avg_rating__lte=0.0).aggregate(
                Avg('avg_rating'))['avg_rating__avg']

        # Member Ranking
        total_member_ranks = 0
        total_ranked_invites = 0
        final_consumer_avg_ranking = 0
        advisor_member_ratings = AdvisorRating.objects.filter(
            advisor=advisor_obj,
            user_type='member'
        )
        if advisor_member_ratings:
            total_ranked_invites += advisor_member_ratings.count()
            total_member_ranks += advisor_member_ratings.exclude(
                avg_rating__lte=0.0).count()
            if advisor_member_ratings.exclude(avg_rating__lte=0.0):
                new_rating = (
                    final_consumer_avg_ranking + advisor_member_ratings.exclude(
                        avg_rating__lte=0.0).aggregate(Avg(
                            'avg_rating'))['avg_rating__avg']
                )
                if new_rating > final_consumer_avg_ranking and final_consumer_avg_ranking != 0:
                    final_consumer_avg_ranking = new_rating / 2
                else:
                    final_consumer_avg_ranking = new_rating
        '''
        Advisor Skills
        '''
        if advisor_obj.skills:
            skills = advisor_obj.skills.split(',')
        advisor_obj.save()
        '''
        Digital Footprints
        '''
        digital_links = DigitalFootPrint.objects\
            .filter(user_profile=advisor_user_profile)\
            .order_by('-created_date')\
            .values('digital_links')[:3]
        logger.info(
            logme('rendered profile page',request)
        )
        '''
        Logged in users userprofile, user status objects
        '''
        user_profile = request.user.profile
        user_status = user_profile.status
        advisor_user_profile.save()
        '''
        Updating Profile Share viewd date and creating mapping
        '''
        if not is_advisor_own_profile:
            profile_share = AdvisorProfileShare.objects\
                .filter(advisor=advisor_obj, email=user_profile.email)\
                .order_by('-created_date').first()
            if profile_share:
                profile_share.viewed_date = \
                    datetime.datetime.now() if not profile_share.viewed_date else None
                profile_share.save()
            ProfileShareMapping.objects.create(
                viewed_page=constants.MY_IDENTITY,
                advisor=advisor_obj,
                viewed_user_profile=user_profile
            )
            try:
                description = user_profile.first_name + 'searched your profile'
                send_mandrill_email(
                    'ABOTMI_25',
                    ["aswatisunder@gmail.com"],
                    context={
                        'name': advisor_obj.user_profile.first_name,
                        'description': description,
                    }
                )
            except:
                logger.debug('Mail failed while sending request to user')
            # Adding notification for viewed profile
            notif_obj = NotificationFunctions(request, advisor_user_profile)
            notif_obj.save_notification(
                sender=user_profile,
                notification_type=VIEWED_PROFILE
            )
            del(notif_obj)

        '''
        Education details
        '''
        educational_details, certification_details = None, None
        education_obj = EducationAndCertificationDetails.objects.filter(
            user_profile=advisor_user_profile).first()
        if education_obj:
            educational_details = json.loads(education_obj.educational_details)[0]
            if education_obj.certification_details:
                if req_type == "mobile":
                   certification_details = json.loads(education_obj.certification_details)
                else:
                    certification_details = json.loads(education_obj.certification_details)
                    if len(certification_details) == 1 and certification_details[0]['certification_name'] == '':
                       certification_details = ''
            else:
                certification_details = ''
        '''
        Country Region
        '''
        # IP Recognisation
        ip_details = request.session['ip_info']
        user_agent_country = ip_details.get(
            "country", constants.REGION_DEFAULT)
    except Exception as e:
        print e
        logger.error(
            logme('Error: unable to navigate advisor profile--%s, \
            Error-Line Number--%s' % (str(e), str(sys.exc_info()[-1].tb_lineno)), request)
        )
        if req_type == "mobile":
            return JsonResponse({'data': "Please Try again after some time"}, status=200)
        else:
            return HttpResponse('Please Try again after some time')
    if request.session.get('ad_chk_email', None): del request.session['ad_chk_email']
    if request.session.get('ad_chk_mob', None): del request.session['ad_chk_mob']
    if request.session.get('ad_chk_name', None): del request.session['ad_chk_name']
    if request.session.get('ad_chk_loc', None): del request.session['ad_chk_loc']
    if request.session.get('ad_chk_reg', None): del request.session['ad_chk_reg']
    social_auth_ses = request.session.get('social_auth_ses', None)
    if req_type == "mobile":
        data = {
            'title': title,
            'financial_instruments': fin_ins if fin_ins else constants.FINANCIAL_INSTRUMENT_NULL_JSON,
            'feedbacks': feedbacks_list,
            'total_no_invites_to_rate': total_no_invites_to_rate,
            'total_no_rated': total_no_rated,
            'final_peer_avg_rating': final_peer_avg_rating,
            'total_ranked_invites': total_ranked_invites,
            'total_member_ranks': total_member_ranks,
            'final_consumer_avg_ranking': final_consumer_avg_ranking,
            'my_promise': advisor_obj.my_promise,
            'my_sales': advisor_obj.my_sales,
            'educational_details': educational_details,
            'certification_details': certification_details,
            'skills': skills,
            'calendly_link':advisor_obj.calendly_link,
        }
        return data
    else:
        return render(request, 'my_identity/my_identity.html',  locals())


def save_education(request):
    '''
    Description: Saving education details(college name, qualification, year of passout)
    '''
    if request.method == 'POST':
        educational_details = request.POST.get('educational_details', None)

        if educational_details:
            user_profile = request.user.profile
            advisor = user_profile.advisor
            educational_detail = json.loads(educational_details)
            educational_detail = [{
                'qualification': educational_detail['qualification'],
                'school': educational_detail['school'],
                'field_of_study': educational_detail['field_of_study'],
                'grade': educational_detail['grade'],
                'activities': educational_detail['activities'],
                'from_year': educational_detail['from_year'],
                'to_year': educational_detail['to_year']
            }]
            education_obj = EducationAndCertificationDetails.objects.filter(user_profile=user_profile).first()
            if education_obj:
                education_obj.educational_details = json.dumps(educational_detail)
                education_obj.save()
                logger.info('Successully updated the education details', request)
            return JsonResponse({'response': 'success'}, status=200)
        else:
            logger.error(
                logme('Required paramters are not passing', request)
            )
            return HttpResponse(status=400)
    else:
        logger.warning(
            logme(
                'GET request - access forbidden for saving education from my identity',
                request
            )
        )
        return HttpResponse(status=405)


def save_sales_acomplishments(request):
    '''
    Description: Advisor adds accomplishments from Advisor Profile/My Identity.
    '''
    if request.method == 'POST':
        advisor = request.user.profile.advisor
        if request.POST['sales_content']:
            advisor.my_sales = request.POST.get('sales_content', None)
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


def save_self_declaration(request):
    '''
    Description: Advisor adds Self declaration/My Identity.
    '''
    if request.method == 'POST':
        user_profile = request.user.profile
        self_description = request.POST.get('self_declaration_content', None)
        req_type = request.POST.get('req_type', None)
        if self_description:
            user_profile.self_description = self_description
            user_profile.save()
            logger.info(
                logme('added self declaration', request)
            )
            if req_type == 'mobile':
                return 'success'
            else:
                return HttpResponse('success')
        else:
            logger.info(
                logme('added failed self declaration', request)
            )
            if req_type == 'mobile':
                return 'failed'
            else:
                return HttpResponse('failed')
    else:
        logger.info(
            logme('GET request - access forbidden to save self declaration', request)
        )
        return HttpResponse('Access Forbidden')


def update_contact_details(request):
    '''
    Description: Updating contact details from my identity.
    '''
    if request.method == 'POST':
        user = request.user
        user_profile = user.profile
        advisor = user_profile.advisor
        mobile_no = request.POST.get('mobile', None)
        city = request.POST.get('city', None)
        address = request.POST.get('address', None)
        calendly_link = request.POST.get('calendly', None)
        req_type = request.POST.get('req_type', None)
        if mobile_no:
            user_profile.mobile = mobile_no
        if city:
            user_profile.city = city
        if address:
            user_profile.address = address
        advisor.calendly_link = calendly_link
        advisor.save()  
        user_profile.save()
        logger.info(
            logme("updated contact details", request)
        )
        if req_type == "mobile":
            return JsonResponse({'response': 'success'}, status=200)
        else:
            return HttpResponse("success")
    else:
        logger.info(
            logme('GET request - access forbidden to update contact details', request)
        )
        return HttpResponse('Access Forbidden')


def save_advisor_skills(request):
    '''
    Description: Advisor adds Skills/My Identity.
    '''
    if request.method == 'POST':
        user_profile = request.user.profile
        advisor = user_profile.advisor
        skills = request.POST.get('skills_content', None)
        if skills:
            advisor.skills = skills
            advisor.save()
            logger.info(
                logme('added advisor skills', request)
            )
            return HttpResponse('success')
        else:
            logger.info(
                logme('failed advisor skills', request)
            )
            return HttpResponse('failed')
    else:
        logger.info(
            logme('GET request - access forbidden to save advisor skills', request)
        )
        return HttpResponse('Access Forbidden')


def edit_regulatory_registration(request):
    '''
    Description: Editing regulatory registration
    '''
    if request.method == "POST":
        irda_reg_no = False
        user = request.user
        user_profile = user.profile
        advisor = user_profile.advisor
        if advisor.is_rera and advisor.rera_details:
            rera_result = json.loads(advisor.rera_details)
        if advisor.dsa_details:
            dsa_result = json.loads(advisor.dsa_details)
    user_status = user_profile.status
    '''
    Regulatory Registration Uploaded Documents
    '''
    document = UploadDocumentsFunctions(request, user_profile)
    # SEBI CERTIFICATE STATUS
    sebi_certificate_status = document.check_document(constants.SEBI_CERTIFICATE)
    sebi_renewal_certificate = document.check_document(constants.SEBI_RENEWAL_CERTIFICATE)
    # AMFI CERTIFICATE STATUS
    amfi_certificate_status = document.check_document(constants.AMFI_CERTIFICATE)
    amfi_renewal_certificate = document.check_document(constants.AMFI_RENEWAL_CERTIFICATE)
    # IRDA CERTIFICATE STATUS
    irda_certificate_status = document.check_document(constants.IRDA_CERTIFICATE)
    irda_renewal_certificate = document.check_document(constants.IRDA_RENEWAL_CERTIFICATE)
    # REGULATORY OTHERS STATUS
    others_certificate_status = document.check_document(constants.OTHER_CERTIFICATE)
    others_renewal_certificate = document.check_document(
        constants.OTHER_RENEWAL_CERTIFICATE)
    del(document)
    ip_details = get_ipinfo(request)
    user_agent_country = ip_details.get("country", constants.REGION_DEFAULT)
    return render(request, 'my_identity/regulatory_registration.html', locals())


def save_regulatory_registration(request):
    '''
    Description: Save regulatory registration
    '''
    if request.method == 'POST':
        # Advisor Details ----
        user_profile = request.user.profile
        advisor_details, created = Advisor.objects.get_or_create(user_profile = user_profile)
        user_status = user_profile.status
        old_rera_json = advisor_details.rera_details
        old_dsa_json = advisor_details.dsa_details
        old_sebi_number = ''
        old_irda_number = ''
        old_amfi_number = ''
        old_other_registered_organisation = ''
        old_other_registered_number = ''
        sebi_number = ''
        irda_number = ''
        amfi_number = ''
        other_organisation = ''
        other_registration_no = ''
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
            sebi_number = request.POST.get('sebi_registration_no', None)
        if request.POST.get('irda_registration_no', None):
            irda_number = request.POST.get('irda_registration_no', None)
        if request.POST.get('amfi_registration_no', None):
            amfi_number = request.POST.get('amfi_registration_no', None)
        if request.POST.get('other_organisation', None):
            other_organisation = request.POST.get('other_organisation', None)
        if request.POST.get('other_registration_no', None):
            other_registration_no = request.POST.get('other_registration_no', None)
        sebi_expiry_date = None
        amfi_expiry_date = None
        irda_expiry_date = None
        other_expiry_date = None
        sebi_start_date = None
        irda_start_date = None
        amfi_start_date = None
        if request.POST.get('sebi_start_date', None):
            sebi_start_date = datetime.datetime.strptime(
                request.POST.get('sebi_start_date',None), '%d-%m-%Y').strftime('%Y-%m-%d')
        if request.POST.get('irda_start_date', None):
            irda_start_date = datetime.datetime.strptime(
                request.POST.get('irda_start_date',None), '%d-%m-%Y').strftime('%Y-%m-%d')
        if request.POST.get('amfi_start_date', None):
            amfi_start_date = datetime.datetime.strptime(
                request.POST.get('amfi_start_date',None), '%d-%m-%Y').strftime('%Y-%m-%d')
        if request.POST.get('sebi_expiry_date', None):
            sebi_expiry_date =datetime.datetime.strptime(
                request.POST.get('sebi_expiry_date',None), '%d-%m-%Y').strftime(
                    '%Y-%m-%d')
        if request.POST.get('amfi_expiry_date', None):
            amfi_expiry_date =datetime.datetime.strptime(
                request.POST.get('amfi_expiry_date',None), '%d-%m-%Y').strftime(
                    '%Y-%m-%d')
        if request.POST.get('irda_expiry_date', None):
            irda_expiry_date = datetime.datetime.strptime(
                request.POST.get('irda_expiry_date',None), '%d-%m-%Y').strftime(
                    '%Y-%m-%d')
        if request.POST.get('other_expiry_date', None):
            other_expiry_date = datetime.datetime.strptime(
                request.POST.get('other_expiry_date',None), '%d-%m-%Y').strftime(
                    '%Y-%m-%d')
        # Changing CRISIL certificate to expired when advisor try to change IRDA or SEBI Details after getting CRISIL Certificate
        if advisor_details.crisil_expiry_date:
            if advisor_details.crisil_expiry_date >= datetime.date.today():
                if not old_sebi_number == sebi_number\
                    or not old_amfi_number == amfi_number:
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

        advisor_details.sebi_number = sebi_number
        advisor_details.sebi_start_date = sebi_start_date
        advisor_details.sebi_expiry_date = sebi_expiry_date
        advisor_details.amfi_number = amfi_number
        advisor_details.amfi_start_date = amfi_start_date
        advisor_details.amfi_expiry_date = amfi_expiry_date
        advisor_details.irda_number = irda_number
        advisor_details.irda_start_date = irda_start_date
        advisor_details.irda_expiry_date = irda_expiry_date
        advisor_details.other_registered_organisation = other_organisation
        advisor_details.other_registered_number = other_registration_no
        advisor_details.other_expiry_date = other_expiry_date
        '''
        RERA Details
        '''
        if request.POST.get('hidden_value', None):
            rera_values = '['+request.POST.get('hidden_value', None)+']'
            advisor_details.rera_details = rera_values
            advisor_details.is_rera = True
        else:
            rera_values = ''
            advisor_details.rera_details = rera_values
            advisor_details.is_rera = False
        if not rera_values == old_rera_json:
            # removing documents for rera
            remove_doc_ids = get_remove_rera_doc(
                request, old_rera_json, rera_values)
            if remove_doc_ids:
                document = UploadDocumentsFunctions(request, user_profile)
                is_document_deleted = document.remove_document(
                    doc_id=remove_doc_ids)
        '''
        DSA Details
        '''
        if request.POST.get('dsa_hidden_input_field', None):
            dsa_values = request.POST.get('dsa_hidden_input_field', None)
            dsa_json = '['+dsa_values+']'
        else:
            dsa_json = ''
        advisor_details.dsa_details = dsa_json
        if (request.POST.get('sebi_registration_no',None) 
            or request.POST.get('amfi_registration_no',None) 
            or request.POST.get('irda_registration_no',None) 
            or request.POST.get('other_organisation',None) 
            or request.POST.get('hidden_value', None) 
            or request.POST.get('dsa_hidden_input_field',None)):
            advisor_details.is_registered_advisor = True
        regulatory_obj = AdvisorCheckCommonFunctions()
        if not user_status.irda_status and irda_number:
            data = {
                'column_name' : 'irda_urn',
                'reg_no' : irda_number
            }
            irda_status = regulatory_obj.get_regulatory_status(object_dict = data)
            if irda_status:
                user_status.irda_status = 'verified'

        if not user_status.sebi_status and sebi_number:
            data = {
                'column_name' : 'reg_no',
                'reg_no' : sebi_number
            }
            sebi_status = regulatory_obj.get_regulatory_status(object_dict = data)
            if sebi_status:
                user_status.sebi_status = 'verified'

        if not user_status.amfi_status and amfi_number:
            data = {
                'column_name' : 'arn',
                'reg_no' : amfi_number
            }
            amfi_status = regulatory_obj.get_regulatory_status(object_dict = data)
            if amfi_status:
                user_status.amfi_status = 'verified'

        advisor_details.save()
        user_status.save()
        del(regulatory_obj)
        return redirect('/my_identity/')


def guest_details(request, slug=None):
    '''
    Description: Navigating to shared profile link
    '''
    title = 'Guest Details'
    recaptcha_key = constants.RECAPTCHA_KEY
    # ip_details gets advisor's country
    ip_details = get_ipinfo(request)
    user_agent_country = ip_details.get("country", constants.REGION_DEFAULT)
    if slug:
        advisor_user_profile = UserProfile.objects.filter(
            batch_code=slug).first()
        if advisor_user_profile:
            # advisor_obj = advisor_user_profile.advisor
            advisor_user_status, is_created = UserStatus.objects.get_or_create(
                user_profile = advisor_user_profile)
            if is_created:
                advisor_user_status.my_identity_status = True
                advisor_user_status.my_repute_status = True
                advisor_user_status.save()
            url = settings.DEFAULT_DOMAIN_URL+'/my_identity/'
            logger.info(
                logme("redirected to the upwrdz shared profile", request)
            )
            return render(request, 'signup/guest_details.html', locals())
        else:
            return HttpResponse('<h1>Unable to view Profile. Check the URL once.</h1>')
    else:
        logger.info(
            logme("failed to redirected to the upwrdz shared profile", request)
        )
        return HttpResponse(
            '<h1>Unable to view Profile. Please try again after sometime</h1>')


def save_guest_details(request):
    '''
    Description: It saves, adds record in GuestUser table
    '''
    if request.method =='POST':
        name = request.POST.get('name', None)
        mobile = request.POST.get('mobile', None)
        email = request.POST.get('email', None)
        user_profile_id = request.POST.get('user_profile_id', None)
        if user_profile_id:
            guest, created = GuestUser.objects.get_or_create(
                email = email, user_profile = user_profile_id)
            if created:
                guest.name = name
                guest.mobile = mobile
            guest.save()
            return HttpResponse('success')
        else:
            return HttpResponse('failed')


def save_total_advisors_connected_count(request):
    '''
    Description: Advisor adds the count of total advisors connected.
    '''
    if request.method == 'POST':
        user_profile = request.user.profile
        advisor = user_profile.advisor
        total_advisors_connected_count  = request.POST.get(
            'total_advisors_connected', None)
        req_type = request.POST.get('req_type', None)
        if total_advisors_connected_count:
            advisor.total_advisors_connected = total_advisors_connected_count
            advisor.save()
            logger.info(
                logme('added total advisors connected', request)
            )
            if req_type=="mobile":
               return  "success"
            else:
               return HttpResponse('success')
        else:
            logger.info(
                logme('added failed total advisors connected', request)
            )
            return HttpResponse('failed')
    else:
        logger.info(
            logme('GET request - access forbidden to save total advisors connected', request)
        )
        return HttpResponse('Access Forbidden')


def save_total_clients_served_count(request):
    '''
    Description: Advisor adds the count of total clients served.
    '''
    if request.method == 'POST':
        user_profile = request.user.profile
        advisor = user_profile.advisor
        total_client_serverd_count = request.POST.get('total_client_serverd_count', None)
        req_type = request.POST.get('req_type', None)
        if total_client_serverd_count:
            advisor.total_clients_served = total_client_serverd_count
            advisor.save()
            logger.info(
                logme('added total clients served', request)
            )
            if(req_type=="mobile"):
               return  "success"
            else:
               return HttpResponse('success')
        else:
            logger.info(
                logme('added failed total clients served', request)
            )
            return HttpResponse('failed')
    else:
        logger.info(
            logme('GET request - access forbidden to save total clients served', request)
        )
        return HttpResponse('Access Forbidden')


class ShareProfileByEmail(View):

    def get(self, request, *args, **kwargs):
        '''
        Description: Function loads the send/share profile by email modal
        '''
        return render(request, 'my_identity/share_profile_by_email.html', locals())

    def post(self, request, *args, **kwargs):
        '''
        Description: Function for sending profile link to email
            and saving shared user details in AdvisorProfileShare table
        '''
        if request.POST['value'] != '[]':
            details = json.loads(request.POST['value'])
            user = request.user
            user_profile = user.profile
            advisor = user_profile.advisor
            for user_details in details:
                context_dict = {
                    'Title': user_details['title'],
                    'Name': user_details['name'],
                    'body_content': user_details['mail_body'],
                    'user_first_name': user.first_name
                }
                send_mandrill_email_admin_subject(
                    'ABOTMI_16',
                    [user_details['email']],
                    user.username,
                    user_details['subject'],
                    context_dict
                )
                advisor_prof_share = AdvisorProfileShare.objects.create(
                    name=user_details['name'],
                    email=user_details['email'],
                    advisor=advisor
                )
            logger.info(
                logme('sent profile link to respective emails', request)
            )
            return HttpResponse('success')
        else:
            logger.warning(
                logme('email list empty to send profile link to others', request)
            )
            return HttpResponse('failed')


class BatchCode(View):
    '''
    Description:
        get() --> Loading Edit batch modal to update/edit the batch
        post() --> Updating the batch
    '''
    def get(self, request, *args, **kwargs):
        batch_url = settings.DEFAULT_DOMAIN_URL+'/profile/'
        logger.debug(
            logme('Loaded edit batch code modal', request)
        )
        return render(request, 'my_identity/edit_batch_code.html', locals())

    def post(self, request, *args, **kwargs):
        batch_code = request.POST.get('batch_code', None)
        if batch_code:
            advisor = request.user.profile
            if advisor:
                advisor.batch_code = batch_code
                logger.debug(
                    logme('Updated batch code', request)
                )
                advisor.save()
                return HttpResponse('success')
            else:
                logger.debug(
                    logme('Unable to update batch --> request post value is not prenset', request)
                )
                return HttpResponse('failed')
        else:
            logger.debug(
                logme('GET Request -- Access forbidden', request)
            )
            return HttpResponse('failed')


def check_batch_availability(request):
    '''
    Description: Cheking requested batch code is already present or not
    if present generating own batch to help advisor.
    '''
    if request.method == 'POST':
        batch_code = request.POST.get('batch_code', None)
        help_batch_codes = []
        if batch_code:
            is_batch_present = UserProfile.objects.filter(
                batch_code = batch_code).values('batch_code').first()
            if is_batch_present:
                while not len(help_batch_codes) == 3:
                    rand_num = random.randint(1, 1000)
                    randome_batch_code = str(batch_code) + str(rand_num)
                    is_help_batch_present = UserProfile.objects.filter(
                        batch_code=randome_batch_code).values('batch_code').first()
                    if not is_help_batch_present:
                        help_batch_codes.append(randome_batch_code)
                logger.debug(
                    logme('Requested batch is already in use. Giving suggestions to advisor', request)
                )
                return JsonResponse(data={'help_batch_codes' : help_batch_codes})
            else:
                logger.debug(
                    logme('requested batch is available to update', request)
                )
                return HttpResponse('success')
        else:
            logger.debug(
                logme('request POST batch value is not present', request)
            )
            return HttpResponse('failed')
    else:
        logger.debug(
            logme('GET request --> Access forbidden', request)
        )
        return HttpResponse('Access forbidden')


def get_advisory_specilization(request):
    '''
    Description: Editing advisory specialization
    '''
    if request.method == "POST":
        user = request.user
        user_profile = user.profile
        advisor = user_profile.advisor
        financial_instruments = advisor.financial_instruments
        if not financial_instruments:
            financial_instruments_json = None
        if financial_instruments == None or not financial_instruments:
            financial_instruments = '[{"instruments":"select","experience":""}]'
        if financial_instruments:
            financial_instruments_json = json.loads(financial_instruments)
            all_financial_instrument = constants.ALL_FINANCIAL_INSTRUMENT
        logger.info(
            logme("redirected to advisory_spec popup", request)
        )
        return render(request, 'my_identity/advisory_specialization.html', locals())


def advisors_archive(request):
    '''
    Description: Function searchs for the advisors and returns.
    '''
    if request.method == 'GET':
        page_number = request.GET.get('search', None)
        user = request.user
        user_profile = user.profile
        if request.is_ajax():
            debates = UserProfile.objects.filter(
                (
                    Q(email__icontains=page_number)|Q(
                        first_name__icontains=page_number)|Q(
                            mobile__icontains=page_number)
                ) & Q(is_advisor=True)).exclude(email=user_profile.email)
        template = 'dashboard/drop_down_advisors_list.html'
        data = {
            'debates': debates,
        }
        return render_to_response(
            template, 
            data, 
            context_instance = RequestContext(request)
        )


def attach_advisors_link(request):
    '''
    Description: It gets the profile link of the searched advisor.
    '''
    if request.method == 'GET':
        page_number = request.GET.get('search', None) 
        if request.is_ajax():
            user_profile = UserProfile.objects.get(email=page_number)
            # advisor_obj = Advisor.objects.get(user_profile=user_profile)
            user_profile.save()
            PROFILE_URL = None
            advisor_status = UserStatus.objects.get(user_profile=user_profile)
            if user_profile.batch_code:
                PROFILE_URL = settings.DEFAULT_DOMAIN_URL + '/profile/' + user_profile.batch_code
        return render(request, 'dashboard/batch_code_link.html', locals())
       

def follower_profile(request):
    '''
    Description: Navigating to blocked_profile html
    '''
    PAGE_TITLE = 'Blocked_profile'
    title = PAGE_TITLE
    logger.info(
        logme("redirected to the Blocked profile", request)
    )
    return render(request, 'my_identity/blocked_profile.html', locals())


def save_experience(request):
    '''
    Saving Experience
    '''
    if request.method == 'POST':
        experience = request.POST.get('experience', None)
        if experience:
            user_profile = request.user.profile
            user_profile.total_experience = experience
            user_profile.save()
            logger.info(
                logme('Updated total expreience', request)
            )
            return JsonResponse(data={}, status=200)
        else:
            logger.error(
                logme('Unable to update expreience, missing required params', request)
            )
            return JsonResponse(data={}, status=400)
    else:
        logger.error(
            logme('Method not allowed to update the expreience', request)
        )
        return JsonResponse(data={}, status=405)


def save_certification(request):
    '''
    Saving certification
    '''
    if request.method == 'POST':
        certification_detail = request.POST.get('certification_data', None)
        if certification_detail:
            user_profile = request.user.profile
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
            education_obj = EducationAndCertificationDetails.objects.filter(
                user_profile=user_profile).first()
            if education_obj:
                education_obj.certification_details = json.dumps(certification_loop)
                education_obj.save()
            return JsonResponse(data={}, status=200)
        else:
            logger.error(
                logme('Unable to update certification, missing required params', request)
            )
            return JsonResponse(data={}, status=400)
    else:
        logger.error(
            logme('Method not allowed to update the certification', request)
        )
        return JsonResponse(data={}, status=405)


class FinancialInstruments(View):
    '''
    Advisors Financial Instruments sold/Advised

    Get:
        Sending Financial Instruments sold to html

    POST:
        Saving the Financial Instruments sold
    '''

    def get(self, request, *args, **kwargs):
        advisor = request.user.profile.advisor
        fin_ins = advisor.financial_instruments
        fin_ins = json.loads(fin_ins) if fin_ins else None
        fin_opt = constants.FINCANCIAL_INSTRUMENTS
        logger.info(
            logme('Loaded Finacial instruments sold(experience) modal', request)
        )
        return render(
            request,
            'my_identity/edit_experience.html',
            {'fin_ins': fin_ins, 'fin_opt': fin_opt}
        )

    def post(self, request, *args, **kwargs):
        instrument_json = request.POST.get('instrument_json', '')
        if instrument_json:
            advisor = request.user.profile.advisor
            advisor.financial_instruments = instrument_json
            advisor.save()
            logger.info(
                logme('Saved Financial Instruments sold (experience)', request)
            )
            return HttpResponse(200)
        else:
            logger.error(
                logme('instrument_json data from html is missing', request)
            )
            return HttpResponse(400)
