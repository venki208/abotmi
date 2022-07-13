import uuid
import json
import re
import logging

# Django Modules
from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render
from django.utils.crypto import get_random_string

# Database Models
from advisor_check.models import (
    AdvisorData, AmfiData, IrdaData, CaData, BseData, 
    SebiData, UnitedStatesAdvisors, MalaysianAdvisors, SingaporeAdvisors,
    )
from datacenter.models import (
    UserProfile, Advisor, UserMobileOtp, AffiliatedCompany,
    CompanyAdvisorMapping, Country, AdvChkProfileConnectMap
)

# Local Imports
from advisor_check.common_views import AdvisorCheckCommonFunctions
from common.utils import send_sms_alert
from common.views import logme, get_ip_region
from common.notification.views import NotificationFunctions
from signup.djmail import send_mandrill_email

# Constatns
from advisor_check.constants import (
    ADVISOR_TYPE, NOT_APPROVED, SIGNUP_WITH_EMAIL,
    CARDS_PER_PAGE, START_PAGES, PAGE_RANGE, IRDA_REG_FIELD, SEBI_REG_FIELD,
    AMFI_REG_FIELD, CA_REG_FIELD, BSE_REG_FIELD, IRDA_NUMBER, SEBI_NUMBER, AMFI_NUMBER,
    CLAIMED_STATUS_VERIFIED, CLAIMED_STATUS_NOT_VERIFIED, CATEGORY_OTHER, SEARCH,
    ADVISOR_CHECK, ADVISOR_PROFILE, ADVISOR_REPUTE, MY_REG_FIELD, SG_REG_FIELD,
    US_REG_FIELD, AD_CHK_PROFILE_URL, ABOTMI_PROFILE_URL, ABOTMI_REPUTE_URL, VIEW
    )
from common.constants import (
    RECAPTCHA_KEY, FIRM_NAME, CSRF_MIDDELWARE_TOKEN, PAGE, 
    IRDA_TABLE, SEBI_TABLE, CA_TABLE, AMFI_TABLE, ADVISOR_DATA_TABLE, ADVISOR_CHECK_APP,
    BSE_TABLE, IRDA_STATUS_FIELD, AMFI_STATUS_FIELD, SEBI_STATUS_FIELD,
    REGULATORY_VERIFIED, REGION_US, REGION_SG, REGION_MY, REGION_IN,
    INDIAN_NATIONALITY, MEMBER_FACEBOOK_MEDIA, MEMBER_LINKEDIN_MEDIA, REGION_DEFAULT
    )
from common.notification.constants import(
    ADVISOR_CHK_CLAIM, ADV_CHK_CONNECT, REG_REQ
)
from common.api_constants import NEXT_URL_LINK

logger = logging.getLogger(__name__)


def home(request):
    '''
    Navigating to Advisor check home page
    '''
    template_name = "advisor_check/home.html"
    individual_tab = True
    firm_tab = False
    country = Country.objects.all().values('name', 'code')
    total_advisor = AdvisorData.objects.count()
    advisor_type_ca = AdvisorData.objects.filter(
        category__contains='CA').values('name').count()
    advisor_type_mfa = AdvisorData.objects.filter(
        category__contains='mutual_fund').values('name').count()
    advisor_type_ia = AdvisorData.objects.filter(
        category__contains='insurance').values('name').count()
    advisor_type_other = AdvisorData.objects.filter(
        category='other').values('name').count()
    recaptcha_key = RECAPTCHA_KEY
    inv_chk_login = request.session.get('inv_chk_login', None)
    social_auth_ses = request.session.get('social_auth_ses', None)
    logger.info(
        logme('rendered advisor check home page', request)
    )
    return render(request, template_name, locals())


def search(request):
    '''
    Searching Advisor and Listing the Results
    '''
    recaptcha_key = RECAPTCHA_KEY
    title = SEARCH
    country = Country.objects.all().values('name', 'code')
    if request.method == 'POST':
        name = request.POST.get('name', None)
        mobile = request.POST.get('mobile', None)
        email = request.POST.get('email', None)
        city = request.POST.get('city', None)
        firm_name = request.POST.get('firm_name', None)
        chk_country = request.POST.get('country', None)
        advisor_data = ''
        kwargs = {}
        modal_name = ''
        if chk_country == REGION_US:
            modal_name = UnitedStatesAdvisors
        elif chk_country == REGION_SG:
            modal_name = SingaporeAdvisors
        elif chk_country == REGION_MY:
            modal_name = MalaysianAdvisors
        else:
            modal_name = AdvisorData

        for key in request.POST:
            if key == "mobile":
                value = request.POST.get(key, None)
                value = value.replace(" ", "")
            else:
                value = request.POST.get(key, None)
            if value:
                if (not key == FIRM_NAME and
                    not key == CSRF_MIDDELWARE_TOKEN and
                    not key == PAGE and
                        not key == 'country'):
                        kwargs[key+'__icontains'] = value
                elif (not key == CSRF_MIDDELWARE_TOKEN and
                        not key == PAGE and
                        not key == 'country'):
                        if key == FIRM_NAME and value:
                            kwargs['company__icontains'] = value
        advisor_total_obj = modal_name.objects.filter(**kwargs)
        total_advisors_found = advisor_total_obj.count()
        # showing 10 cards per page
        paginator = Paginator(advisor_total_obj, CARDS_PER_PAGE)
        page = request.POST.get('page', None)
        try:
            advisor_obj = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            advisor_obj = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            advisor_obj = paginator.page(paginator.num_pages)
            logger.info(
                logme('empty page', request)
            )
        max_index = len(paginator.page_range)
        start_index = 0
        end_index = max_index if max_index < START_PAGES else START_PAGES
        if page:
            start_index = int(page)-PAGE_RANGE if int(page) > PAGE_RANGE else 0
            end_index = int(page)+PAGE_RANGE if int(page)+PAGE_RANGE < max_index else \
                max_index
        page_range = paginator.page_range[start_index:end_index]
        logger.info(
            logme('listed search results for keyword=%s' % (str(advisor_data)), request)
        )
        template_name = "advisor_check/search.html"
    if request.method == 'GET':
        template_name = "advisor_check/search.html"
    return render(request, template_name, locals())


def check_advisor(request):
    '''
    Checking Advisor is present or not in Advisor check database
    '''
    if request.method == 'POST':
        advisor_id = request.POST.get('advisor_id', None)
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        mobile = request.POST.get('mobile', None)
        advisor_details = AdvisorData.objects.filter(id=advisor_id)
        if advisor_details:
            advisor_details = advisor_details.first()
            if advisor_details.mobile == mobile \
                or advisor_details.mobile2 == mobile\
                or advisor_details.email == email \
                or advisor_details.secondary_email == email:
                    num = uuid.uuid4().hex[:6]
                    user_otp, created = UserMobileOtp.objects.get_or_create(
                        otp_source=ADVISOR_TYPE, user_profile_id=advisor_id
                    )
                    user_otp.otp = num
                    user_otp.mobile = mobile
                    advisor_data = {}
                    advisor_data['email'] = email
                    advisor_data['mobile'] = mobile
                    advisor_data['name'] = name
                    user_otp.verify_data = json.dumps(advisor_data)
                    user_otp.save()
                    message = 'Dear '+name+', Your OTP is '+num+'.'
                    sms_response = send_sms_alert(
                        mobile_number=mobile, message_template=message)
                    data = {
                        'member_name': name,
                        'otp': num
                    }
                    send_mandrill_email(
                        'ABOTMI_19',
                        [email],
                        context=data
                    )
                    context_dict = {
                        'response': 'success',
                        'advisor_id': advisor_id
                    }
                    logger.info(
                        logme('advisor records matched successfully', request)
                    )
                    return JsonResponse(context_dict)
            else:
                context_dict = {
                    'response': 'not_matching'
                }
                logger.info(
                    logme('advisor records not matched', request)
                )
                return JsonResponse(context_dict)
            context_dict = {
                'response': 'not_matching'
            }
            logger.info(
                logme('advisor records not matched', request)
            )
        return JsonResponse(context_dict)
    else:
        logger.info(
            logme('GET request - access forbidden for matching advisor details', request)
        )
        return HttpResponse('Access forbidden')


def create_advisor(request):
    '''
    Description: Creating the Advisor After validating the OTP in UPWRDZ.
        -> Creating company if not exists and Mapping advisor under that company 
    '''
    if request.method == 'POST':
        otp = request.POST.get('otp', None)
        advisor_id = request.POST.get('advisor_id', None)
        user_otp = UserMobileOtp.objects.filter(
            otp=otp,
            user_profile_id=advisor_id,
            otp_source=ADVISOR_TYPE
        )
        if user_otp:
            user_otp = user_otp.first()
            advisor_json = user_otp.verify_data
            if advisor_json:
                data = json.loads(advisor_json)
                advisor_data = AdvisorData.objects.get(
                    id=user_otp.user_profile_id)
                user, status = User.objects.get_or_create(
                    username=data['email'],
                    email=data['email']
                )
                if status:
                    user_password = get_random_string(length=8)
                    user.first_name = data['name']
                    user.is_active = True
                    user.is_staff = True
                    user.set_password(user_password)
                    user.save()
                    user_profile = user.profile
                    user_profile.first_name = data['name']
                    user_profile.email = data['email']
                    user_profile.mobile = data['mobile']
                    user_profile.is_advisor = True
                    user_profile.source_media = SIGNUP_WITH_EMAIL
                    user_profile.save()
                    logger.info(
                        logme('advisor created successfully', request)
                    )
                    try:
                        send_mandrill_email(
                            'ABOTMI_02',
                            [user.profile.email],
                            context={
                                'name': data['name'],
                                'url': NEXT_URL_LINK,
                                'username': user.profile.email,
                                'password': user_password
                            }
                        )
                        logger.info(
                            logme('sent email to advisor for successful claim', request)
                        )
                    except:
                        logger.info(
                            logme(
                                'failed to send email to advisor for successful claim',
                                request
                            )
                        )
                        return HttpResponse('mailfailed')
                    response = 'success'
                else:
                    response = 'user_exists'
                advisor_data.advisor_id = user.profile.id
                if advisor_data.company:
                    company = AffiliatedCompany.objects.filter(
                        contact=advisor_data.company)
                    if company:
                        company = company.first()
                        company.users_count = company.users_count + 1
                        company.save()
                        logger.info(
                            logme('company already exists for advisor claim, company user\
                                count=%s updated' % (str(company.users_count)), request)
                        )
                    else:
                        company_name = re.split(' ', advisor_data.company)
                        company_name = filter(None, company_name)
                        email = "contact@" + company_name[0]
                        user_company, created = User.objects.get_or_create(
                            username=email,
                            email=email
                        )
                        if created:
                            user_company.is_active = True
                            user_company.is_staff = True
                            user_company.save()
                            company_profile = user_company.profile
                            company_profile.email = email
                            company_profile.is_company = True
                            company_profile.save()
                            company_obj, status = AffiliatedCompany.objects.get_or_create(
                                user_profile=company_profile)
                            company_obj.contact = advisor_data.company
                            company_obj.users_count = company_obj.users_count + 1
                            company = company_obj
                            company_obj.save()
                            logger.info(
                                logme(
                                    'company does not exist, created successfully for \
                                    advisor claim', request)
                            )
                    affiliate_company_child, status = CompanyAdvisorMapping.objects.\
                        get_or_create(
                            advisor_user_profile=user.profile,
                            company_user_profile=company.user_profile
                        )
                    if status:
                        affiliate_company_child.status = NOT_APPROVED
                        affiliate_company_child.save()
                        logger.info(
                            logme(
                                'company and advisor mapped successfully for advisor \
                                claim', request)
                        )
                advisor_data.save()
                user_otp.delete()
                logger.info(
                    logme('company advisor data saved successfully', request)
                )
                return HttpResponse(response)
    logger.info(
        logme('could not create advsior for advisor claim', request)
    )
    return HttpResponse('unable to create')


def get_advisor_information(request):
    '''
    Getting Advisor Registration Details
    '''
    data = {
        'response': 'Access forbidden'
    }
    if request.method == 'POST':
        advisor_id = request.POST.get('advisor_id', None)
        if advisor_id:
            registrations = ''
            advisor_check_obj = AdvisorData.objects.filter(id=advisor_id)
            if advisor_check_obj:
                advisor_check_obj = advisor_check_obj.first()
                if advisor_check_obj.registrations:
                    registrations = json.loads(advisor_check_obj.registrations)
                    data = {
                        'response': 'success',
                        'registrations': registrations
                    }
                    logger.info(
                        logme('returned advisor registration data for advisor id = %s' % (
                            str(advisor_id)), request)
                    )
                    return JsonResponse(data)
        data = {
            'response': 'result_not_found'
        }
        logger.info(
            logme(
                'advisor registration details not found for advisor id=%s' % (str(
                    advisor_id)), request
            )
        )
        return JsonResponse(data)
    logger.info(
        logme('GET request- access forbidden for advisor registration details', request)
    )
    return JsonResponse(data)


@login_required()
def get_advisor_card(request):
    '''
    Description: Getting Advisor Matching card using priority mode
        priorities : 1. Primary email
            2. Secondary Email
            3. Primary Mobile
            4. Secondary Mobile
    '''
    title = ADVISOR_CHECK
    user = request.user
    user_profile = user.profile
    advisor_obj = None
    is_advisor_found = ''
    ad_mobile = ''
    primaty_email, secondary_email, primary_mobile, secondary_mobile = '', '', '', ''
    advisor_records_obj = AdvisorData.objects.all().values('name', 'city')[:9]
    if user_profile.mobile:
        ad_mobile = user_profile.mobile.replace(
            " ", "").replace("+91", "").replace("-", "")
    country_list = Country.objects.all().values('name', 'code')
    # country = Country.objects.filter(name=user_profile.country).values('code').first()
    country = get_ip_region(request)
    if country == REGION_US:
        table_name = UnitedStatesAdvisors
    elif country == REGION_SG:
        table_name = SingaporeAdvisors
    elif country == REGION_MY:
        table_name = MalaysianAdvisors
    else:
        table_name = AdvisorData
    # Cheking the Advisor in Advisor Check
    adv_chk_cls_obj = AdvisorCheckCommonFunctions()
    object_dict = {
            'email': user_profile.email,
            'primary_mobile': user_profile.mobile,
            'first_name': user_profile.first_name,
            'type_of_advisor': table_name
        }
    # advisor_obj = adv_chk_cls_obj.check_matching_card(object_dict)
    advisor_obj = table_name.objects.filter(email=user_profile.email).values(
            'id', 'email', 'mobile', 'advisor_id').first()
    if advisor_obj:
        is_advisor_found = True
    del(adv_chk_cls_obj)
    logger.info(
        logme('advisor matched card object = %s' % (
            advisor_obj['id'] if advisor_obj else None), request)
    )
    return render(request, 'advisor_check/match_card.html', locals())


def save_advisor_card(request):
    '''
    Description: Advisor Claiming the card and saving
    '''
    if request.method == 'POST':
        field_name = None
        advisor_reg_field_name = None
        reg_org_data = []
        reg_org_status = []
        advisor_che_card_id = request.POST.get('advisor_check_card_id', None)
        certificate_type = request.POST.get('certification_type', None)
        certification_id = request.POST.get('certification_id', None)
        country = request.POST.get('country_type_val', None)
        advisor_city = request.POST.get('advisors_city', None)
        if not country:
            country = get_ip_region(request)
        expertise = request.POST.get('expertise', None)
        user = request.user
        user_profile = user.profile
        advisor = user_profile.advisor
        user_status = user_profile.status
        if country == REGION_IN:
            if advisor_che_card_id:
                if certificate_type == 'IRDA':
                    model_name = IRDA_TABLE
                    field_name = IRDA_REG_FIELD
                    advisor_reg_field_name = IRDA_NUMBER
                    advisor_reg_status_field_name = IRDA_STATUS_FIELD
                elif certificate_type == 'SEBI':
                    model_name = SEBI_TABLE
                    field_name = SEBI_REG_FIELD
                    advisor_reg_field_name = SEBI_NUMBER
                    advisor_reg_status_field_name = SEBI_STATUS_FIELD
                elif certificate_type == 'AMFI':
                    model_name = AMFI_TABLE
                    field_name = AMFI_REG_FIELD
                    advisor_reg_field_name = AMFI_NUMBER
                    advisor_reg_status_field_name = AMFI_STATUS_FIELD
                elif certificate_type == 'CA':
                    model_name = CA_TABLE
                    field_name = CA_REG_FIELD
                elif certificate_type == 'BSE':
                    model_name = BSE_TABLE
                    field_name = BSE_REG_FIELD
            else:
                model_name = ADVISOR_DATA_TABLE
        elif country == REGION_MY:
            field_name = MY_REG_FIELD
            model_name = 'MalaysianAdvisors'
        elif country == REGION_SG:
            field_name = SG_REG_FIELD
            model_name = 'SingaporeAdvisors'
        elif country == REGION_US:
            field_name = US_REG_FIELD
            model_name = 'UnitedStatesAdvisors'
        else:
            model_name = ADVISOR_DATA_TABLE
        my_model = apps.get_model(ADVISOR_CHECK_APP, model_name)
        if advisor_che_card_id:
            certification_obj = my_model.objects.filter(id=advisor_che_card_id).first()
            certification_obj.claimed_status = CLAIMED_STATUS_VERIFIED
            certification_obj.email = user_profile.email
            certification_obj.city = advisor_city
            ad_chk_status = 'Claimed'
        else:
            certification_obj = my_model.objects.filter(
                email=user_profile.email).first()
            if not certification_obj:
                certification_obj = my_model.objects.create(
                    email=user_profile.email)
            certification_obj.email = user_profile.email
            certification_obj.secondary_email = user_profile.secondary_email
            certification_obj.name = user.get_full_name()
            certification_obj.mobile = user_profile.mobile
            certification_obj.pincode = user_profile.pincode
            certification_obj.title = user_profile.suffix
            certification_obj.category = CATEGORY_OTHER
            certification_obj.source_link = settings.DEFAULT_DOMAIN_URL
            certification_obj.city = advisor_city
            ad_chk_status = 'Created'
        if not model_name == ADVISOR_DATA_TABLE:
            setattr(certification_obj, field_name, certification_id)
        certification_obj.advisor_id = user_profile.id
        certification_obj.save()
        if advisor_che_card_id:
            if certificate_type == 'IRDA' or certificate_type == 'SEBI' \
                or certificate_type == 'AMFI':
                    reg_org_data = [
                        (advisor_reg_field_name, certification_id)
                    ]
                    reg_org_status = [
                        (advisor_reg_status_field_name, REGULATORY_VERIFIED)
                    ]
        if country == REGION_IN:
            other_reg_org_data, other_reg_org_status = get_advisor_check_org_data(
                    user_profile=user_profile,
                    claimed_field=field_name,
                    status=CLAIMED_STATUS_VERIFIED
                )

            total_adv_reg_org_data = reg_org_data + other_reg_org_data
            for k, v in total_adv_reg_org_data:
                setattr(advisor, k, v)

            total_adv_reg_org_status = reg_org_status + other_reg_org_status
            for k, v in total_adv_reg_org_status:
                setattr(user_status, k, v)

        if expertise:
            expertise_json = {}
            expertise = json.loads(expertise)
            loaded_exper_json_length = len(expertise)/2
            exp_no = 0
            for i in range(loaded_exper_json_length):
                if not expertise[exp_no + 1]['value'] == 'Select':
                    expertise_json[expertise[exp_no]['value']] = expertise[exp_no + 1]['value']
                exp_no = exp_no + 2
            advisor.expertise = json.dumps(expertise_json)
        advisor.is_registered_advisor = True
        advisor.save()
        user_status.save()
        # Notification class object
        nf = NotificationFunctions(request=request, receive=user_profile)
        nf.save_notification(
            notification_type=REG_REQ
        )
        del(nf)
        logger.info(
            logme(
                'advisor saved his advisor check card and redirected to My Repute Page', 
                request
            )
        )
        if user_profile.advisor.is_confirmed_advisor:
            return HttpResponseRedirect('/my_identity/')
        else:
            return HttpResponseRedirect('/signup/face_capture/')
    else:
        return HttpResponse('Access forbidden')


def send_otp_to_match_card(request):
    '''
    Description: Sending OTP to unmatched data to verify
    '''
    if request.method == 'POST':
        otp_type = request.POST.get('otp_type', None)
        mobile = request.POST.get('mobile', None)
        email = request.POST.get('email', None)
        email = request.POST.get('email', None)
        num = uuid.uuid4().hex[:6]
        user_otp, created = UserMobileOtp.objects.get_or_create(
            otp_source=ADVISOR_TYPE, user_profile_id=request.user.profile.id
        )
        user_otp.otp = num
        user_otp.mobile = mobile
        advisor_data = {}
        advisor_data['email'] = email
        advisor_data['mobile'] = mobile
        advisor_data['name'] = request.user.first_name
        user_otp.verify_data = json.dumps(advisor_data)
        user_otp.save()
        if otp_type == 'mobile' or otp_type == 'email_and_mobile':
            if mobile:
                try:
                    message = 'Dear '+request.user.profile.first_name+', Your OTP is '+num+'.'
                    sms_response = send_sms_alert(
                        mobile_number=mobile, message_template=message
                    )
                    logger.info(
                        logme('sent OTP to %s' % (mobile), request)
                    )
                except:
                    logger.info(
                        logme('unable send OTP to mobile', request)
                    )
        if otp_type == 'email' or otp_type == 'email_and_mobile':
            if email:
                data = {
                    'member_name': request.user.profile.first_name,
                    'otp': num
                }
                try:
                    send_mandrill_email(
                        'ABOTMI_19',
                        [email],
                        context=data
                    )
                    logger.info(
                        logme('sent OTP to %s' % (email), request)
                    )
                except:
                    logger.info(
                        logme('unable send OTP to Email', request)
                    )
        return HttpResponse('success')
    else:
        return HttpResponse('Access forbidden')


def validate_otp(request):
    '''
    Description: Validating the OTP
    '''
    if request.method == 'POST':
        otp = request.POST.get('otp', None)
        user_otp = UserMobileOtp.objects.filter(
            otp=otp,
            user_profile_id=request.user.profile.id,
            otp_source=ADVISOR_TYPE
        )
        if user_otp:
            logger.info(
                logme('validation: OTP is valied', request)
            )
            user_otp.delete()
            return HttpResponse('success')
        else:
            logger.info(
                logme('validation: OTP is not valied', request)
            )
            return HttpResponse('failed')
    else:
        return HttpResponse('Access forbidden')


def get_certified_card(request):
    '''
    Checking Advisor Certifications details are present or not for Claiming into UPWRDZ
    '''
    if request.method == 'POST':
        cerificate_id = request.POST.get('certificate_id', None)
        certificate_type = request.POST.get('certificate_type', None)
        country_type = request.POST.get('country_type', None)
        kwargs = {}
        if cerificate_id and country_type:
            if country_type == REGION_IN:
                if certificate_type == 'IRDA':
                    model_name = IrdaData
                    kwargs['irda_urn'] = cerificate_id
                elif certificate_type == 'SEBI':
                    model_name = SebiData
                    kwargs['reg_no'] = cerificate_id
                elif certificate_type == 'AMFI':
                    model_name = AmfiData
                    kwargs['arn'] = cerificate_id
                elif certificate_type == 'CA':
                    model_name = CaData
                    kwargs['reg_id'] = cerificate_id
                elif certificate_type == 'BSE':
                    model_name = BseData
                    kwargs['bse_clearing_number'] = cerificate_id
            elif country_type == REGION_MY:
                model_name = MalaysianAdvisors
                kwargs['licence_number'] = cerificate_id
            elif country_type == REGION_SG:
                model_name = SingaporeAdvisors
                kwargs['member_number'] = cerificate_id
            elif country_type == REGION_US:
                model_name = UnitedStatesAdvisors
                kwargs['lic_id'] = cerificate_id
            else:
                data = {
                    'status_code': 200,
                    'card_id': '',
                    'country_type': country_type
                }
                return JsonResponse(data)
            certification_obj = model_name.objects.filter(**kwargs).first()
            if certification_obj:
                data = {
                    'status_code': 302,
                    'card_id': certification_obj.id,
                    'country_type': country_type
                }
            else:
                data = {
                    'status_code': 200,
                    'card_id': '',
                    'country_type': country_type
                }
        else:
            data = {
                'status_code': 204
            }
        return JsonResponse(data)
    else:
        return HttpResponse('Access forbidden')


def check_advisor_claimed(request):
    '''
    Checking UPWRDZ advisor is claimed or not
    '''
    user_profile = request.user.profile
    kwargs = {
        'advisor_id': user_profile.id
    }
    advisor_obj = AdvisorData.objects.filter(**kwargs).values('id').first()
    amfi_obj = AmfiData.objects.filter(**kwargs).values('id').first()
    irda_obj = IrdaData.objects.filter(**kwargs).values('id').first()
    ca_obj = CaData.objects.filter(**kwargs).values('id').first()
    bse_obj = BseData.objects.filter(**kwargs).values('id').first()
    sebi_obj = SebiData.objects.filter(**kwargs).values('id').first()
    us_adv_obj = UnitedStatesAdvisors.objects.filter(**kwargs).values('id').first()
    sg_adv_obj = SingaporeAdvisors.objects.filter(**kwargs).values('id').first()
    my_adv_obj = MalaysianAdvisors.objects.filter(**kwargs).values('id').first()
    if advisor_obj or amfi_obj or irda_obj or ca_obj or bse_obj or sebi_obj \
        or us_adv_obj or sg_adv_obj or my_adv_obj:
            return True
    else:
        return False


def get_advisor_check_org_data(user_profile=None, claimed_field=None, status=None):
    '''
    Descrption: Getting the Registration numbers from SEBI, AMFI, IRDA tables
    '''
    reg_fields = [IRDA_REG_FIELD, SEBI_REG_FIELD, AMFI_REG_FIELD]
    total_reg_num = []
    total_reg_status = []
    adv_tab_field_name = None
    for org_field in reg_fields:
        if not claimed_field == org_field:
            if org_field == IRDA_REG_FIELD:
                model_name = IRDA_TABLE
                adv_tab_field_name = IRDA_NUMBER
                advisor_reg_status_field_name = IRDA_STATUS_FIELD
            elif org_field == SEBI_REG_FIELD:
                model_name = SEBI_TABLE
                adv_tab_field_name = SEBI_NUMBER
                advisor_reg_status_field_name = SEBI_STATUS_FIELD
            else:
                model_name = AMFI_TABLE
                adv_tab_field_name = AMFI_NUMBER
                advisor_reg_status_field_name = AMFI_STATUS_FIELD
            my_model = apps.get_model(ADVISOR_CHECK_APP, model_name)
            other_cert_obj = my_model.objects.filter(email=user_profile.email).first()
            if other_cert_obj:
                other_cert_obj.claimed_status = status
                other_cert_obj.advisor_id = user_profile.id
                reg_org_number = getattr(other_cert_obj, org_field)
                total_reg_num.append(
                    (adv_tab_field_name, reg_org_number)
                )
                total_reg_status.append(
                    (advisor_reg_status_field_name, REGULATORY_VERIFIED)
                )
                other_cert_obj.save()
    return total_reg_num, total_reg_status


def get_advisor_navigation_url(request):
    '''
    Generating Advisors profile link
    parameters:
        ad_chk_id -> id of the advisor
        page_type -> 'profile/repute'
        catogery_type -> catogery type (ex: CA, SG, US, etc...)
    '''
    if request.method == 'POST':
        ad_chk_id = request.POST.get('ad_chk_id', None)
        page_type = request.POST.get('page_type', None)
        chk_country = request.POST.get('chk_country', None)
        nav_url = None
        if ad_chk_id and page_type:
            ad_chk_model = AdvisorCheckCommonFunctions.get_table_name(chk_country)
            ad_chk_obj = ad_chk_model.objects.filter(id=ad_chk_id).first()
            if ad_chk_obj:
                if ad_chk_obj.advisor_id:
                    user_profile_obj = UserProfile.objects.filter(
                        id=ad_chk_obj.advisor_id).first()
                    if user_profile_obj:
                        user_profile_obj.save()
                        if page_type == ADVISOR_PROFILE:
                            nav_url = ABOTMI_PROFILE_URL % (user_profile_obj.batch_code)
                        elif page_type == ADVISOR_REPUTE:
                            nav_url = ABOTMI_REPUTE_URL % (user_profile_obj.batch_code)
                        else:
                            nav_url = '/member/'
                else:
                    nav_url = AD_CHK_PROFILE_URL % (ad_chk_obj.id, chk_country)
                return HttpResponse(nav_url)
            else:
                return HttpResponse(204)
        else:
            return HttpResponse(400)


def profile(request, ad_chk_id=None, ct_type=None):
    '''
    Getting profile details of advisor in advisor check.
    parameters:
        ad_chk_id -> id of the advisor
        ct_type -> catogery type (ex: CA, SG, US, etc...)
    '''
    title = 'Profile'
    if ad_chk_id and ct_type:
        ad_chk_model = AdvisorCheckCommonFunctions.get_table_name(ct_type)
        query_col, renamed_fields = AdvisorCheckCommonFunctions.get_profile_view_fields(
            ad_chk_model.__name__)
        ad_chk_obj = ad_chk_model.objects.filter(id=ad_chk_id).annotate(
            **renamed_fields).values(*query_col).first()
        pr_conn_view, is_created = AdvChkProfileConnectMap.objects.get_or_create(
            user_profile=request.user.profile,
            advisor_chk_id=ad_chk_id,
            registration_type=ad_chk_model.__name__,
            action_type=VIEW
        )
        if ad_chk_obj['email']:
            pr_conn_view.email = ad_chk_obj['email']
        pr_conn_view.save()
        return render(request, 'advisor_check/profile.html', locals())
    else:
        return Http404('Missing required parameters')


def connect_advisor(request):
    '''
    Description: Function adds the advisor and advisor's respective registration 
        entry to the AdvChkProfileConnectMap table.
    '''
    if request.method == 'POST':
        advisor_id = request.POST.get('advisor_id', None)
        chk_country = request.POST.get('chk_country', None)
        user_profile = request.user.profile
        # category_name = category_name if category_name else ADVISOR_DATA_TABLE
        if advisor_id:
            adv_chk_modal = AdvisorCheckCommonFunctions.get_table_name(chk_country)
            adv_chk_obj = adv_chk_modal.objects.filter(id=advisor_id).first()
            if adv_chk_obj:
                if adv_chk_obj.advisor_id:
                    advisor_u_p = UserProfile.objects.filter(
                        id=adv_chk_obj.advisor_id).first()
                    advisor_adv = advisor_u_p.advisor
                    email = advisor_u_p.email
                    name = advisor_u_p.user.get_full_name()
                    try:
                        # Email to the Advisor- When Advisor checks the peers
                        if user_profile.advisor.is_register_advisor:
                            if advisor_adv.calendly_link:
                                context_dict = {
                                    'advisor_name': request.user.get_full_name(),
                                    'advisor_email_id': request.user.email,
                                    'peer_name': name,
                                    'calendly_url': advisor_adv.calendly_link
                                }
                                send_mandrill_email(
                                    'ABOTMI_34',
                                    [request.user.email],
                                    context=context_dict
                                )
                            else:
                                context_dict = {
                                    'member_name': request.user.get_full_name(),
                                    'advisor_name': name
                                }
                                send_mandrill_email(
                                    'ABOTMI_32',
                                    [request.user.email],
                                    context=context_dict
                                )
                        # Email to the Investor- When Investor connects with the advisor
                        else:
                            if advisor_adv.calendly_link:
                                context_dict = {
                                    'member_name': request.user.get_full_name(),
                                    'advisor_name': name,
                                    'calendly_url': advisor_adv.calendly_link
                                }
                                send_mandrill_email(
                                    'ABOTMI_35',
                                    [request.user.email],
                                    context=context_dict
                                )
                            else:
                                context_dict = {
                                    'member_name': request.user.get_full_name(),
                                    'advisor_name': name
                                }
                                send_mandrill_email(
                                    'ABOTMI_32',
                                    [request.user.email],
                                    context=context_dict
                                )
                    except:
                        logger.debug(
                            'Mail failed while sending request to user')
                else:
                    email = adv_chk_obj.email
                    name = adv_chk_obj.name
                if email:
                    connect_obj, created = AdvChkProfileConnectMap.objects.get_or_create(
                        user_profile=user_profile,
                        advisor_chk_id=advisor_id,
                        action_type='connect',
                        registration_type=adv_chk_modal.__name__
                    )
                    connect_obj.email = email
                    connect_obj.save()
                    # Email to the Advisor
                    try:
                        context_dict = {
                            'investor_name': request.user.get_full_name(),
                            'advisor_name': name,
                            'investor_email_id': request.user.email
                        }
                        send_mandrill_email(
                            'ABOTMI_25',
                            [email],
                            context=context_dict
                        )
                    except:
                        logger.debug('Mail failed while sending request to user')
                    if adv_chk_obj.advisor_id:
                        adv_profile = UserProfile.objects.filter(
                            id=adv_chk_obj.advisor_id).first()
                        profile_url = settings.DEFAULT_DOMAIN_URL + '/profile/' + \
                            user_profile.batch_code
                        nf = NotificationFunctions(
                            request=request)
                        nf.save_notification(
                            data=[profile_url, request.user.get_full_name()],
                            notification_type=ADV_CHK_CONNECT,
                            sender=user_profile,
                            receive=adv_profile
                        )
                        del(nf)
                    return JsonResponse({'status_code': 200,'advisor_id':adv_chk_obj.advisor_id})
                else:
                    return JsonResponse(
                        {'status_code': 204, 'status_txt': 'email_not_found'})
            else:
                return JsonResponse({'status_code': 204, 'status_txt': 'not_found'})
        else:
            return JsonResponse({'status_code': 400})


def get_calendly_link(request):
    if request.method == 'POST':
        advisor_id = request.POST.get('id', None)
        if advisor_id:
            adv_obj = Advisor.objects.filter(user_profile_id=advisor_id).first()
            if adv_obj and adv_obj.calendly_link:
                advisor_user_profile = UserProfile.objects.filter(
                    id=advisor_id).first()
                # Commented temporarily
                # context_dict = {
                #     'member_name': request.user.first_name,
                #     'advisor_name': advisor_user_profile.first_name,
                #     'calendly_url': adv_obj.calendly_link
                # }
                # Email to the Investor
                # send_mandrill_email(
                #     'ABOTMI_31',
                #     [request.user.email],
                #     context=context_dict
                # )
                # context_dict = {
                #     'member_name': request.user.first_name,
                #     'advisor_name': advisor_user_profile.first_name,
                # }
                # Email to the Advisor
                # send_mandrill_email(
                #     'ABOTMI_25',
                #     [advisor_user_profile.email],
                #     context=context_dict
                # )
                return JsonResponse({'status_code': 200, 'data': adv_obj.calendly_link})
            else:
                return JsonResponse({'status_code': 204, 'data': ''})
        else:
            return JsonResponse({'status_code': 400})
    else:
        return HttpResponse('Access forbidden')
