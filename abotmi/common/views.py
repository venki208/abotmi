# python lib
import base64
import cStringIO as StringIO
import datetime
import json
import logging
import os
import random
import re
import requests
import time
import uuid
import random
from mimetypes import MimeTypes
from datetime import date

# Django Modules
from django.conf import settings
from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template.loader import render_to_string, get_template
from django.template import RequestContext, Context
from django.conf.urls.static import static
from django.core.files.storage import default_storage
from django.db.models import Avg, query
from django.utils.crypto import get_random_string

# Third party lib
from xhtml2pdf import pisa
import pandas as pd
from reportlab.lib.units import inch

# Database Models
from django.contrib.auth.models import User
from datacenter.models import (
    ReferralPointsType, ReferralPoints, SocialMediaLikesShareCount, Advisor, 
    TransactionsDetails, UploadDocuments, UserProfile, MeetUpEvent, TrackWebinar, 
    AdvisorRating, CompanyAdvisorMapping, AffiliatedCompany, ClientAdvisorMapping, 
    UserMobileOtp, India_Pincode, DigitalFootPrint, AdvisorPublishedVideo, 
    EducationAndCertificationDetails)
from advisor_check.models import (
    AdvisorData, IrdaData, AmfiData, CaData, SebiData, BseData, FinraAdvisors, 
    UnitedStatesAdvisors, SingaporeAdvisors, MalaysianAdvisors)

# Local imports
from common import constants, api_constants
from common.utils import calculate_discount_amount, calculate_tax_amount, send_sms_alert
from signup.djmail import send_mandrill_email_with_attachement, send_mandrill_email
from signup import constants as signup_constants

logger = logging.getLogger(__name__)


def referral_points(beneficiary, referred, referral_type):
    '''
    Adding points to referral advisor
    '''
    points_obj = ReferralPointsType.objects.filter(name=referral_type)
    for refer_advisor in points_obj:
        points = refer_advisor.points
        if refer_advisor.level == 1:
            beneficiary = beneficiary
        if refer_advisor.level == 2:
            if beneficiary.referred_by:
                beneficiary = beneficiary.referred_by.profile
        refer_signup_points_obj = ReferralPoints.objects.create(
            referralpointstype=refer_advisor,
            beneficiary=beneficiary,
            referred=referred,
            points=points
        )
        previous_total_points = beneficiary.total_points
        beneficiary.total_points = points + previous_total_points
        beneficiary.save()


def social_media_like_count(blog_url, type_social_media):
    '''
    Creating/Updating the social media post count
    '''
    social_media_obj, created = SocialMediaLikesShareCount.objects.get_or_create(
        url=blog_url)
    '''
    Facebook
    ---------------------------
    1. Check type of social media
    2. Generating access token in facebook using app id and app client_secret
    3. fetch likes and share count from facebook using api with generated access token
    4. Check existing record or not, if it is new, record is created or else update the 
        count
    -----------------------------------------
    '''
    if type_social_media == "fb":
        token_params = {
            'grant_type': 'client_credentials',
            'client_id': settings.FACEBOOK_API,
            'client_secret': settings.FACEBOOK_APP_SECRET,
            'redirect_uri': settings.DEFAULT_DOMAIN_URL
        }
        token_request = requests.post(
            constants.FACEBOOK_SHARE_URL,
            params=token_params
        )
        if token_request.status_code == 200:
            token_request = json.loads(token_request.content)
            access_token = token_request['access_token']
            fb_url = constants.FB_GRAPH_URL+'?id='+blog_url+'&fields=engagement'
            headers = {'Content-Type': 'application/json'}
            fb_req = requests.get(fb_url, headers=headers)
            if fb_req.status_code == 200:
                fb_json = fb_req.content.encode('UTF-8')
                fb_like_obj = json.loads(fb_json)
                if fb_like_obj is not None and 'engagement' in fb_like_obj:
                    if created:
                        social_media_obj.facebook_shares = fb_like_obj[
                            'engagement']['share_count']
                    if not created:
                        social_media_obj.facebook_shares = fb_like_obj[
                            'engagement']['share_count']

    '''
    google
    ---------------------------
    1. Check type of social media
    2. fetch likes and share count from google plus using api
    3. Check existing record or not, if it is new, record is created or else update the 
        count
    ---------------------------
    '''
    if type_social_media == "g+":
        data = "{\n\
            \"jsonrpc\": \"2.0\",\n\
            \"apiVersion\": \"v1\",\n\
            \"id\": \"p\",\n\
            \"params\": {\n\
                \"nolog\": \"true\",\n\
                \"source\": \"widget\",\n\
                \"userId\": \"@viewer\",\n\
                \"id\": \""+str(blog_url)+"\",\n\
                \"groupId\": \"@self\"\n\
            },\n\
            \"key\": \"AIzaSyCM6MqwVTDhaXxrvC0ccDgdwsWxovDmIXk\",\n\
            \"method\": \"pos.plusones.get\"\n\
        }"
        headers = {'Content-Type': 'application/json'}
        time.sleep(10)
        request_google_share_activity = requests.post(
            constants.GOOGLE_SHARE_URL,
            data=data,
            headers=headers,
            verify=False  # temprory : need to bechange verify = false to true
        )
        google_json = json.loads(request_google_share_activity.text)
        if google_json is not None:
            if created:
                social_media_obj.google_plus_shares = google_json[
                    'result']['metadata']['globalCounts']['count']
            if not created:
                social_media_obj.google_plus_shares = google_json[
                    'result']['metadata']['globalCounts']['count']

    '''
    linkedin
    ---------------------------
    1. Check type of social media
    2. fetch share count from linkedin using api
    3. Check existing record or not, if it is new, record is created or else update the
        count
    ---------------------------
    '''
    if type_social_media == "ln":
        headers = {'Content-Type': 'application/json'}
        time.sleep(10)
        link_url = constants.LINKEDIN_SHARE_URL + blog_url + "&format=json"
        request_linkedin_share_activity = requests.post(link_url, headers=headers)
        if request_linkedin_share_activity.status_code == 200:
            linkedin_json = request_linkedin_share_activity.content.encode('UTF-8')
            linkedin_json_obj = json.loads(linkedin_json)
        if linkedin_json_obj is not None:
            if created:
                social_media_obj.linkedin_shares = linkedin_json_obj['count']
            if not created:
                social_media_obj.linkedin_shares = linkedin_json_obj['count']
    total_count = social_media_obj.facebook_shares \
        + social_media_obj.google_plus_shares \
        + social_media_obj.linkedin_shares
    social_media_obj.total_count = total_count
    social_media_obj.save()


def top_three_post(json_res=[]):

    '''
    Social Media counts
    --------------------
    1.  Create Object for SocialMediaLikesShareCount to fetch to fetch top most three and
        convert into json format using serializers.
    2.  Using for loops and compare icore post link and reia social top post link from the
        table. If both are same get detail information of post and append it in the
        count[].
    3.  Add count key in the same count list.
    4.  Displayed Top three Post on templates using count list.
    -----------------------------------------------------------
    '''
    token_obj_all = json.dumps(json_res)
    token_obj_all = json.loads(token_obj_all)
    # To store the top three post from social details count table
    social_media_count = []
    # Add top post from icore json to display on templage
    count = []
    social_media_count = serializers.serialize(
        'json',
        SocialMediaLikesShareCount.objects.filter().order_by('total_count')[:3]
    )
    sm_count_obj = json.loads(social_media_count)

    if token_obj_all and sm_count_obj:
        for item1 in sm_count_obj:
            for item in token_obj_all:
                if item['link'] == item1['fields']['url']:
                    blog_url = item['link']
                    social_media_obj = SocialMediaLikesShareCount.objects.get(
                        url=blog_url)
                    item['facebook_count'] = social_media_obj.facebook_shares
                    item['google_count'] = social_media_obj.google_plus_shares
                    item['linkedin_count'] = social_media_obj.linkedin_shares
                    count.append(item)
    return count


def social_media_like_count_bg_process():
    '''
    Getting the Social media Like count
    '''
    url_obj = SocialMediaLikesShareCount.objects.all()
    for item in url_obj:
        url = item.url
        social_media_like_count(url, 'fb')
        social_media_like_count(url, 'g+')
        social_media_like_count(url, 'ln')


def check_crisil_advisor(advisor):
    '''
    Descrption: 1) Checking Advisor got CRISIL certificate or not
                2) if he is not applied CRISIL than it returns not_crisil_advisor
                3) checking CRISIL certificate got expired or not
    '''
    if advisor.crisil_expiry_date:
        if advisor.crisil_expiry_date >= datetime.date.today():
            if advisor.crisil_application_status == constants.CRISIL_EXPIRED or \
                advisor.crisil_application_status == constants.CRISIL_EXPIRED_BY_USER:
                    crisil_certificate_valid = False
            else:
                crisil_certificate_valid = True
        else:
            crisil_certificate_valid = False
    else:
        crisil_certificate_valid = ''
    return crisil_certificate_valid


def fetch_resources(uri, rel):
    '''
    Descrption: Fetch the static files and media files from static directory using
        settings
    '''
    if uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    elif uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.LOADING_STATIC_FOR_PDF, uri.replace(
            settings.STATIC_URL, ""))
    return path


def generate_pdf(request, html_file, context_data, download, filename):
    '''
    Descrption: Converting Html into PDF
    '''
    rendered_html = render_to_string(html_file, locals())
    template = get_template(html_file)
    context = context_data
    html = template.render(context)
    result = StringIO.StringIO()
    file = open('file.pdf', "w+b")
    pisaStatus = pisa.CreatePDF(
        html.encode('utf-8'), dest=file, encoding='utf-8', link_callback=fetch_resources)
    file.seek(0)
    pdf = file.read()
    file.close()
    response = HttpResponse(pdf, 'application/pdf')
    if download:
        response['Content-Disposition'] = 'attachment; filename="%s.pdf"' % (filename)
    return response


def invoice_gen(advisor, transaction_instance):
    '''
    Genearing Invoice number for CRISIL
    '''
    current_year = date.today().strftime("%Y")
    current_month = date.today().strftime("%m")
    invoice_code = constants.INVOICE_NUMBER_NEW
    invoice_year = current_year
    invoice_sequence = constants.START_INVOICE_SEQUENCE
    '''
    get the latest object in the current year which is in the current financial year
    and increment the sequence
    '''
    latest_invoice = TransactionsDetails.objects.filter(
        invoice_number__contains=current_year).order_by('-serial_no').exclude(
            serial_no=0, invoice_number='')
    if latest_invoice:
        invoice_sequence = latest_invoice[0].serial_no + 1
    else:
        '''
        check if we are in the previous financial year,
        if it is, increment the sequence
        '''
        if int(current_month) <= 3:
            invoice_year = int(current_year) - 1
            latest_invoice = TransactionsDetails.objects.filter(). \
                order_by('-serial_no').exclude(serial_no=0, invoice_number='')
            if latest_invoice:
                invoice_sequence = latest_invoice[0].serial_no + 1
    '''
    if it is renewal, change the invoice code to 02 series
    '''
    if advisor.crisil_application_status == constants.CRISIL_RENEWAL_PAYMENT_SUBMITTED:
        invoice_code = constants.INVOICE_NUMBER_RENEWAL
    '''
    formation of new invoice number
    '''
    new_invoice_no = invoice_code + str(invoice_year) + '-' + str(
        invoice_sequence).zfill(6)
    return new_invoice_no


def auth_token(username, password):
    '''
    Descrption: Generating UPLYF Auth token
    '''
    if username and password:
        auth_credentials = {
            'username': username,
            'password': password
        }
        auth_response = requests.post(
            api_constants.AUTH_URL,
            data=auth_credentials,
            verify=constants.SSL_VERIFY
        )
        token = json.loads(auth_response.content.encode('UTF-8'))
        return token
    else:
        return False


def get_all_members(advisor_email):
    '''
    Descrption: Get all members and registerd, unregistered count data from UPLYF
    '''
    token = auth_token(settings.UPLYF_USER_NAME, settings.UPLYF_PASSWORD)
    headers = {'Authorization': 'JWT %s' % token['token']}
    advisor_data = {'advisor_email': advisor_email}
    view_members = requests.post(
        api_constants.VIEW_MEMBERS_DETAILS,
        headers=headers,
        data=advisor_data,
        verify=constants.SSL_VERIFY
    )
    if view_members.status_code == 200:
        return json.loads(view_members.content)
    else:
        return False


def get_invited_members(advisor_email):
    '''
    Descrption: Get all invite members data from UPLYF
    '''
    token = auth_token(settings.UPLYF_USER_NAME, settings.UPLYF_PASSWORD)
    headers = {'Authorization': 'JWT %s' % token['token']}
    advisor_data = {'advisor_email': advisor_email}
    view_members = requests.post(
        api_constants.VIEW_INVITED_MEMBERS_DETAILS,
        headers=headers,
        data=advisor_data,
        verify=constants.SSL_VERIFY
    )
    if view_members.status_code == 200:
        return json.loads(view_members.content)
    else:
        return False


def client_enquiry(advisor_name, advisor_id, advisor_email):
    '''
    Getting Advisors Enquiry Management details from UPLYF
    '''
    data = {
        "advisor_id": advisor_id,
        "advisor_name": advisor_name,
        "advisor_email": advisor_email
    }
    member_data = ''
    members_data = requests.post(
        api_constants.ENQUIRY_MANAGEMENT_DETAILS,
        data=data,
        verify=constants.SSL_VERIFY
    )
    if members_data:
        return json.loads(members_data.content)
    else:
        return False


def get_uplyf_project_list():
    '''
    Descrption : Getting All Project names with Id from UPLYF
    '''
    token = auth_token(settings.UPLYF_USER_NAME, settings.UPLYF_PASSWORD)
    headers = {'Authorization': 'JWT %s' % token['token']}
    project_name = requests.get(
        api_constants.UPLYF_PROJECT_NAMES,
        headers=headers,
        verify=constants.SSL_VERIFY
    )
    if project_name.status_code == 200:
        project_name = json.loads(project_name.content)
        return project_name['data']
    else:
        return False


def get_all_advisors_count(request, region=constants.REGION_DEFAULT):
    '''
    Getting Advisors count according to Region from Advisor Check database
    '''
    if region == constants.REGION_US:
        # returns US Data
        advisor_type_usa = UnitedStatesAdvisors.objects.count()
        advisor_type_finra = FinraAdvisors.objects.count()
        total_advisor_count = advisor_type_usa + advisor_type_finra

        data = [
            {'Advisor Enrolled': total_advisor_count},
            {'Insurance': advisor_type_usa},
            {'Brokers': advisor_type_finra},
        ]
    elif region == constants.REGION_SG:
        # returns Singapore data
        advisor_type_singapore = SingaporeAdvisors.objects.count()
        total_advisor_count = advisor_type_singapore

        data = [
            {'Advisor Enrolled': total_advisor_count},
            {'Financial Advisors': advisor_type_singapore},
        ]
    elif region == constants.REGION_MY:
        # returns Malaysian data
        advisor_type_malaysian = MalaysianAdvisors.objects.values('id').all()
        # gathering the counts
        deal_in_securities = advisor_type_malaysian.filter(
            regulated_activity__startswith="Dealing in Securities").values('id').count()
        deal_in_derivatives = advisor_type_malaysian.filter(
            regulated_activity__startswith="Dealing in Derivatives").values('id').count()
        funds_advisor = advisor_type_malaysian.filter(
            regulated_activity__startswith="Fund Management").values('id').count()
        investment_advice = advisor_type_malaysian.filter(
            regulated_activity__startswith="Investment Advice").values('id').count()
        advice_on_corporate = advisor_type_malaysian.filter(
            regulated_activity__startswith="Advising on Corporate Finance").values(
                'id').count()
        financial_planning = advisor_type_malaysian.filter(
            regulated_activity__startswith="Financial Planning").values('id').count()
        # category count
        equities_advisor_count = deal_in_securities + deal_in_derivatives
        funds_advisor_count = funds_advisor
        advisory_count = investment_advice + advice_on_corporate + financial_planning
        total_advisor_count = equities_advisor_count + funds_advisor_count \
            + advisory_count

        data = [
            {'Advisor Enrolled': total_advisor_count},
            {'Equity': equities_advisor_count},
            {'Funds': funds_advisor_count},
            {'Advisory': advisory_count},
        ]
    elif region == constants.REGION_CA:
        # returns Canada data
        advisor_type_ca_count = CaData.objects.count()
        advisor_type_sebi_count = SebiData.objects.count()
        advisor_type_irda_count = IrdaData.objects.count()
        advisor_type_amfi_count = AmfiData.objects.count()
        advisor_type_bse_count = BseData.objects.count()
        advisor_type_other = AdvisorData.objects.filter(
            category='other').values('id').count()
        total_advisor_count = advisor_type_ca_count + advisor_type_irda_count \
            + advisor_type_amfi_count + advisor_type_sebi_count + advisor_type_bse_count \
            + advisor_type_other

        data = [
            {'Advisor Enrolled': total_advisor_count},
            {'CA': advisor_type_ca_count},
            {'SEBI': advisor_type_sebi_count},
            {'IRDA': advisor_type_irda_count},
            {'AMFI': advisor_type_amfi_count},
            {'BSE': advisor_type_bse_count},
            {'Other': advisor_type_other},
        ]
    elif region == constants.REGION_IN:
        # returns India data
        # -----------------------
        # total_advisor_count
        # advisor_type_ca_count
        # advisor_type_sebi_count
        # advisor_type_irda_count
        # advisor_type_amfi_count
        # advisor_type_bse_count
        # advisor_type_other
        # -----------------------
        advisor_type_ca_count = CaData.objects.count()
        advisor_type_sebi_count = SebiData.objects.count()
        advisor_type_irda_count = IrdaData.objects.count()
        advisor_type_amfi_count = AmfiData.objects.count()
        advisor_type_bse_count = BseData.objects.count()
        advisor_type_other = AdvisorData.objects.filter(
            category='other').values('id').count()
        total_advisor_count = advisor_type_ca_count + advisor_type_irda_count \
            + advisor_type_amfi_count + advisor_type_sebi_count + advisor_type_bse_count \
            + advisor_type_other

        data = [
            {'Advisor Enrolled': total_advisor_count},
            {'CA': advisor_type_ca_count},
            {'SEBI': advisor_type_sebi_count},
            {'IRDA': advisor_type_irda_count},
            {'AMFI': advisor_type_amfi_count},
            {'BSE': advisor_type_bse_count},
            {'Other': advisor_type_other},
        ]
    else:
        # return All Regions data count
        # -----------------------
        # total_advisor_count
        # advisor_type_ca_count
        # advisor_type_sebi_count
        # advisor_type_irda_count
        # advisor_type_amfi_count
        # advisor_type_bse_count
        # advisor_type_other
        # -----------------------
        advisor_type_ca_count = CaData.objects.count()
        advisor_type_sebi_count = SebiData.objects.count()
        advisor_type_irda_count = IrdaData.objects.count()
        advisor_type_amfi_count = AmfiData.objects.count()
        advisor_type_bse_count = BseData.objects.count()
        advisor_type_other = AdvisorData.objects.filter(
            category='other').values('id').count()
        total_advisor_count = advisor_type_ca_count + advisor_type_irda_count \
            + advisor_type_amfi_count + advisor_type_sebi_count \
            + advisor_type_bse_count + advisor_type_other

        data = [
            {'Advisor Enrolled': total_advisor_count},
            {'CA': advisor_type_ca_count},
            {'SEBI': advisor_type_sebi_count},
            {'IRDA': advisor_type_irda_count},
            {'AMFI': advisor_type_amfi_count},
            {'BSE': advisor_type_bse_count},
            {'Other': advisor_type_other},
        ]
    return data


def get_binary_image(user_profile):
    '''
    Descrption: This will convert image into binary format
    '''
    profile_pic = ''
    try:
        if user_profile.picture:
            profile_image = user_profile.picture
            mime = MimeTypes()
            image = default_storage.open(
                user_profile.picture.url.split('media/')[1], 'r')
            image_type = mime.guess_type(profile_image.url)[0]
            binary_url = 'data:' + image_type + ';base64,'
            profile_pic = binary_url + base64.b64encode(image.read())
    except:
        profile_pic = ''
    return profile_pic


def upload_image_and_get_path(user_profile, documents_type, image):
    '''
    Descrption: upload into s3 bucket or local and return the path of the file
    '''
    server_domains = [
        'dev.abotmi.com', 'test.abotmi.com', 'abotmi.com', 'prod.abotmi.com',
        'www.abotmi.com', 'abotmi-dev.upwrdz.com',
    ]
    if documents_type and image:
        missing_padding = len(image) % 4
    if missing_padding != 0:
        image += b'=' * (4 - missing_padding)
        encoded_image = image.encode('ascii', 'ignore')
        encoded_image = encoded_image[22:]
        if any(n in settings.DEFAULT_HOST for n in server_domains):
            '''
            ACTION: use to store file / profile picture in AWS S3 storage
            '''
            if not documents_type == 'Profile Picture':
                picture_path = "reia/"+str(user_profile.id)+"/"\
                    + user_profile.registration_id+documents_type+str(random.getrandbits(128))+".jpg"
            else:
                picture_path = "reia/" + \
                    str(user_profile.id) + "/" + \
                    user_profile.registration_id + "pic.png"
            default_storage.exists(picture_path)
            file = default_storage.open(picture_path, 'w')
            file.write(encoded_image.decode('base64'))
            file.close()
        else:
            if not documents_type == 'Profile Picture':
                picture_path = "reia/"+str(user_profile.id)+"/"\
                    + user_profile.registration_id+documents_type + \
                    str(random.getrandbits(128))+".jpg"
                picture_url = "uploads/"+picture_path
                if documents_type == 'testimonial_picture':
                    picture_path = "reia/testimonial/"\
                        + documents_type+str(random.getrandbits(128))+".jpg"
                    picture_url = "uploads/"+picture_path
            else:
                picture_path = "reia/" + \
                    str(user_profile.id) + "/" + \
                    user_profile.registration_id + "pic.png"
                picture_url = "uploads/"+picture_path
            fh = open(picture_url, "wb")
            fh.write(encoded_image.decode('base64'))
            fh.close()
        return picture_path
    return False


def get_eipv_documents(request, user_profile):
    '''
    Descrption : creating eipv document objects.
    '''
    # For US demo purpose - Commemted temporarily
    ip_details = get_ipinfo(request)
    user_agent_country = ip_details.get("country", constants.REGION_DEFAULT)
    eipv_aadhaar = UploadDocuments.objects.filter(
        user_profile=user_profile,
        documents_type=constants.EIPV_AADHAAR
        )
    eipv_face_capture = UploadDocuments.objects.filter(
        user_profile=user_profile,
        documents_type=constants.EIPV_FACE_CAPTURE
    )
    data = {  
        'eipv_aadhaar': eipv_aadhaar,
        'eipv_face_capture': eipv_face_capture
    }
    return data


def check_user_uplyf(advisor_email):
    '''
    Cheking Advisor is exists in UPLYF or not
    '''
    token = auth_token(settings.UPLYF_USER_NAME, settings.UPLYF_PASSWORD)
    headers = {'Authorization': 'JWT %s' % token['token']}
    advisor_data = {'advisor_email': advisor_email}
    view_user = requests.post(
        api_constants.CHECK_UPLYF_USER,
        headers=headers,
        data=advisor_data,
        verify=constants.SSL_VERIFY
    )
    if view_user.status_code == 200:
        return json.loads(view_user.content)
    else:
        return False


def logme(message, request):
    '''
    Description : returns formatted log message string (message , user id , ip)
    '''
    log_message = '%s | %s | %s' % (
        message,
        str('Anonymous User' if not request.user.id else request.user.id),
        get_ip(request)
    )
    return log_message


def get_ip(request):
    '''
    Description : returns user IP
    '''
    ip = None
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_ipinfo(request):
    '''
    Description : returns user IP information of given ip
    '''
    ip = get_ip(request)
    ip_and_query = ip + "/json/"
    json_result = {}
    param_data = {"token": getattr(settings, 'IP_INFO_TOKEN', '13300771afb0ed')}
    IP_INFO_URL = getattr(settings, 'IP_INFO_URL', 'https://ipinfo.io/')
    request_url = IP_INFO_URL + "/" + ip_and_query
    res = requests.get(request_url, params=param_data)
    res_data = res.content
    if "Rate limit exceeded" in res_data:
        res_data = '{\n  "ip": "106.51.67.101",\n  "country": "US"\n}'
    return json.loads(res_data)


class AdvisorCommonFunction:
    '''
    Description: Creating Advisor Common funcitons for Re-use
    '''
    def __init__(self, request):
        logger.info(
            logme('Common class object is created', request)
        )

    def get_reffred_registered_advisors(self, object=None):
        '''
        Description: Fetching Registered reffered advisors
        ex: get_reffred_registered_advisors(object = user_profile)
        '''
        user_profile_obj = UserProfile.objects.filter(
            advisor__is_register_advisor=True,
            referred_by=object
        )
        return user_profile_obj

    def get_reffred_registered_advisors_count(self, object=None):
        ref_reg_obj = self.get_reffred_registered_advisors(object)
        return ref_reg_obj.count()

    def get_reffred_advisors(self, object=None):
        '''
        Description: Fetching all reffered advisors
        ex: get_reffred_registered_advisors(object = user_profile)
        '''
        user_profile_obj = UserProfile.objects.filter(
            referred_by=object
        )
        return user_profile_obj

    def get_reffred_advisors_count(self, object=None):
        ref_adv = self.get_reffred_advisors(object=None)
        return ref_adv.count()


class RatingAndRankingCommonFunctions:
    '''
    Description: Creating Rating Common funcitons for Re-use
    '''

    def __init__(self, request, advisor):
        logger.info(
            logme('Rating and Ranking class object is created', request)
        )
        self.request = request if request else None
        self.advisor = advisor

    def get_all_rated_by_advisor(self, avg_rating=None):
        '''
        Description: Get all Ratings
        parameter:
        1. avg_rating --> get all rating with avg value (ex: avg_rating = 3.0)(optional)
        '''
        kwargs = {}
        kwargs['advisor'] = self.advisor
        kwargs['user_type'] = 'advisor'
        if avg_rating:
            kwargs['avg_rating__gte'] = avg_rating
        rating_obj = AdvisorRating.objects.filter(**kwargs)
        return rating_obj

    def get_all_rated_by_advisor_count(self, avg_rating=None):
        '''
        Description: Get all Ratings count
        parameter:
        1. avg_rating --> get all rating with avg value (ex: avg_rating = 3.0)(optional)
        '''
        rating_obj = self.get_all_rated_by_advisor(avg_rating)
        return rating_obj.count()

    def get_all_ranked_by_advsior(self, avg_rating=None):
        '''
        Description: Get all Rankings
        parameter:
        1. avg_rating --> get all ranking with avg value (ex: avg_rating = 3.0)(optional)
        '''
        kwargs = {}
        kwargs['advisor'] = self.advisor
        kwargs['user_type'] = 'member'
        if avg_rating:
            kwargs['avg_rating__gte'] = avg_rating
        ranking_obj = AdvisorRating.objects.filter(**kwargs)
        return ranking_obj

    def get_all_ranked_by_advsior_count(self, avg_rating=None):
        '''
        Description: Get all Rankings count
        parameter:
        1. avg_rating --> get all ranking with avg value (ex: avg_rating = 3.0)(optional)
        '''
        ranking_obj = self.get_all_ranked_by_advsior(avg_rating)
        return ranking_obj.count()


class CommonObjects:
    '''
    Description: Creating Common funcitons for Re-use
    '''

    def __init__(self, params):
        self.request = params['request'] if params.has_key('request') else None
        if self.request:
            logger.info(
                logme('Common class object is created', params['request'])
            )

    def get_all_added_clients(self, object=None):
        '''
        Description: Getting all client Added by requested advisor
        '''
        total_members = None
        members = get_all_members(object.username)
        if members:
            total_members = members['content']
        return total_members


class Otp:
    '''
    Description: Class for sending/verifying OTP

    Create Object By passing request,
    optional: user_profile_id(pass only the id), name
    '''
    __mobile_otp = None
    __email_otp = None

    def __init__(self, request, user_profile_id=None, name=None):
        self.request = request
        logger.info(
            logme('Common class object is created', self.request)
        )
        self.user_profile_id = user_profile_id
        self.name = name
        self.__mobile_otp = random.randint(100000, 999999)
        self.__email_otp = uuid.uuid4().hex[:6]
        self.user_profile_id = user_profile_id

    def send_otp(self, mobile=None, email=None, otp_type=constants.OTP_TO_MOBILE):
        '''
        Sending OTP to Email or Mobile
        # mobile --> Mobile Number
        # email --> Email Id
        # otp_type -->
            type    constant
            ----    ---------
            mobile  OTP_TO_MOBILE
            Email   OTP_TO_EMAIL
            BOTH    OTP_TO_BOTH
            Default OTP_TO_MOBILE
        '''
        kwargs = {}
        kwargs['user_profile_id'] = self.user_profile_id
        user_otp_data = {}
        user_otp_data['name'] = self.name
        if self.user_profile_id and mobile or email:
            if mobile:
                if otp_type == constants.OTP_TO_MOBILE or otp_type==constants.OTP_TO_BOTH:
                    otp_code = random.randint(100000, 999999)
                    kwargs['otp_source'] = constants.OTP_MOBILE
                    user_otp_data['mobile'] = mobile
                    user_otp, created = UserMobileOtp.objects.get_or_create(**kwargs)
                    user_otp.otp = otp_code
                    user_otp.mobile = mobile
                    user_otp.verify_data = json.dumps(user_otp_data)
                    user_otp.save()
                    self.send_otp_to_mobile(
                        mobile=mobile, name=self.name, mobile_otp=otp_code)

            if email:
                if otp_type == constants.OTP_TO_EMAIL or otp_type==constants.OTP_TO_BOTH:
                    otp_code = uuid.uuid4().hex[:6]
                    kwargs['otp_source'] = constants.OTP_EMAIL
                    user_otp_data['email'] = email
                    user_otp, created = UserMobileOtp.objects.get_or_create(**kwargs)
                    user_otp.otp = otp_code
                    user_otp.mobile = mobile
                    user_otp.verify_data = json.dumps(user_otp_data)
                    user_otp.save()
                    self.send_otp_to_email(email=email, name=self.name, email_otp=otp_code)
        else:
            return None

    def send_otp_to_mobile(self, mobile=None, name=None, mobile_otp=None):
        '''
        Descrption: Sending OTP to mobile
        '''
        try:
            if not mobile_otp:
                mobile_otp = random.randint(100000, 999999)
            message = 'Dear %s, Your OTP is %s.' % (name, str(mobile_otp))
            sms_response = send_sms_alert(
                mobile_number=mobile, message_template=message)
            if sms_response.status_code == 200:
                logger.info(
                    logme('sent otp to mobile', self.request)
                )
            else:
                logger.error(
                    logme('unable to send otp to mobile exception:%s' \
                        %(sms_response.content), self.request)
                )
            return mobile_otp
        except Exception as e:
            logger.info(
                logme('unable to send otp to mobile exception:%s' %(e), self.request)
            )
            msg = "Unable to send"

    def send_otp_to_email(self, email=None, name=None, email_otp=None):
        '''
        Descrption: Sending OTP to email
        '''
        try:
            if not email_otp:
                email_otp = uuid.uuid4().hex[:6]
            data = {
                'member_name': name,
                'otp': email_otp
            }
            send_mandrill_email(
                'ABOTMI_19',
                [email],
                context=data
            )
            logger.info(
                logme('sent otp to email', self.request)
            )
            return email_otp
        except Exception as e:
            message = "Unable to send"
            logger.info(
                logme('unable to send otp to email exception:%s' %(e), self.request)
            )


    def send_signup_otp(
                self, mobile=None, email=None, name=None, otp_type=None, ad_info=None):
        '''
        Sending Signup OTP to email/mobile
        '''
        if (mobile or email) and otp_type:
            kwargs = {
                'otp_source': otp_type
            }
            if mobile:
                kwargs['mobile']= mobile
                mob_otp = self.__mobile_otp
                self.send_otp_to_mobile(
                    mobile=mobile, name=name, mobile_otp=mob_otp)
            if email:
                kwargs['email'] = email
                emi_otp = self.__email_otp
                self.send_otp_to_email(
                    email=email, name=name, email_otp=emi_otp)
            umo, status = UserMobileOtp.objects.get_or_create(**kwargs)
            umo.otp = mob_otp if mobile else emi_otp
            if ad_info: 
                umo.verify_data = ad_info
            umo.save()
            return True
        else:
            return False

    def send_resend_signup_otp(
                self, mobile=None, email=None, name=None, otp_type=None):
        '''
        Sending Signup OTP to email/mobile
        '''
        if (mobile or email) and otp_type:
            kwargs = {
                'otp_source': otp_type
            }
            user_otp_data = {}
            if otp_type == constants.OTP_TO_MOBILE:
                if mobile:
                    kwargs['mobile']= mobile
                    otp_code = random.randint(100000, 999999)
                    user_otp_data['mobile'] = mobile
                    user_otp, created = UserMobileOtp.objects.get_or_create(**kwargs)
                    if created:
                        user_otp.otp = otp_code
                        user_otp.mobile = mobile
                        user_otp.verify_data = json.dumps(user_otp_data)
                        user_otp.save()
                    self.send_otp_to_mobile(
                        mobile=mobile, name=name, mobile_otp=user_otp.otp)
            
            if otp_type in [constants.OTP_TO_EMAIL, constants.SIGNUP_OTP]:
                if email:
                    if otp_type == constants.SIGNUP_OTP:
                        user_otp = UserMobileOtp.objects.filter(
                            otp_source='signup_otp', email=email).first()
                    else:
                        kwargs['email'] = email
                        otp_code = uuid.uuid4().hex[:6]
                        user_otp_data['email'] = email
                        user_otp, created = UserMobileOtp.objects.get_or_create(**kwargs)
                        if created:
                            user_otp.otp = otp_code
                            user_otp.mobile = mobile
                            user_otp.verify_data = json.dumps(user_otp_data)
                            user_otp.save()
                    self.send_otp_to_email(email=email, name=name, email_otp=user_otp.otp)
            return True
        else:
            return False

    def validate_otp(self, otp=None, email=None, mobile=None,
                        otp_type=constants.OTP_TO_MOBILE, verify=True):
        '''
        Description: Verifies/Validate the OTP and delete the object
            verify = True --> It will verify/validate the OTP and deletes the object
            verify = False --> It will validate the OTP and return True if valid or False
        '''
        kwargs = {}
        if self.user_profile_id: kwargs['user_profile_id'] = self.user_profile_id
        kwargs['otp'] = otp
        if otp_type == constants.OTP_TO_MOBILE:
            kwargs['otp_source'] = constants.OTP_MOBILE
            kwargs['mobile'] = mobile
        elif otp_type == constants.SIGNUP_OTP:
            kwargs['otp_source'] = constants.SIGNUP_OTP
        else:
            kwargs['otp_source'] = constants.OTP_EMAIL
        user_mobile_otp = UserMobileOtp.objects.filter(**kwargs).first()
        if user_mobile_otp:
            logger.info(
                logme('%s object found - Valid OTP'%(otp_type), self.request)
            )
            if verify:
                user_mobile_otp.delete()
            return True
        else:
            logger.info(
                logme('%s object not found - invalid OTP'%(otp_type), self.request)
            )
            return False


class UploadDocumentsFunctions:

    '''
    Description: Getting Document and document status using document type and
    '''
    def __init__(self, request, user_profile):
        logger.info(
            logme('Upload Documents class object is created', request)
        )
        self.user_profile = user_profile
        self.request = request

    def get_document(self, document_type=None, doc_id=None, many=False):
        '''
        Getting Uploaded document

        ==> any one is mandatory(expects atleast one value)

        # document_type --> ex: 'sebi_certificate'

        # doc_id --> ex: 5 or [1,2,3] or {idL:'1', idL:'2'}(i.e; object with values id) or ['1', '2']

        # many --> True for more then one record else return single record
        '''
        kwargs = {}
        kwargs['user_profile'] = self.user_profile
        if document_type:
            kwargs['documents_type'] = document_type
        if doc_id:
            if not type(doc_id) == query.ValuesQuerySet and not type(doc_id) == list:
                doc_id = [doc_id]
            kwargs['id__in'] = doc_id
        document = UploadDocuments.objects.filter(**kwargs)
        if not many:
            document = document.first()
        return document

    def check_document(self, document_type):
        '''
        Cheking document is preset or not
        '''
        document = self.get_document(document_type)
        if document:
            return True
        else:
            return False

    def get_document_status(self, document_type=None, doc_id=None):
        '''
        Getting uploaded status using document type
        '''
        if document_type or doc_id:
            document = self.get_document(document_type, doc_id)
            if document:
                return document.status
            else:
                return None
        else:
            return None

    def get_all_documents(self):
        '''
        Getting all docuemtns using document type
        '''
        documents = UploadDocuments.objects.all()
        return documents

    def remove_document(self, document_type=None, doc_id=None):
        '''
        Removing document
        '''
        try:
            kwargs = {}
            kwargs['user_profile'] = self.user_profile
            if document_type:
                kwargs['documents_type'] = document_type
            if doc_id:
                if not type(doc_id) == query.ValuesQuerySet and not type(doc_id) == list:
                    doc_id = [doc_id]
                kwargs['id__in'] = doc_id
            UploadDocuments.objects.filter(**kwargs).delete()
            return True
        except Exception as e:
            logger.info(
                logme('Unable to delete the document error:%s'%(str(e)), self.request)
            )
            return False


class EducationQualificationFunctions:
    '''
    Description: Getting Education information, Additional education informatio with 
    document status.
    '''

    def __init__(self, request, user_profile):
        logger.info(
            logme('Education qualification class object created', request)
        )
        self.request = request
        self.user_profile = user_profile

    def get_additional_qualifications(self, load_json=True):
        '''
        Getting Additional Qualification Information Json with upload document status

        # load_json = True (by default True), it will load the json and return

        # load_json = False, it will return dumped string json
        '''
        document = UploadDocumentsFunctions(self.request, self.user_profile)
        add_qul_json = self.user_profile.additional_qualification
        if add_qul_json:
            additional_qualification = json.loads(add_qul_json)
            for add_qul in additional_qualification:
                add_doc_id = add_qul.get('documents_upload', None)
                if add_doc_id:
                    doc_status = document.get_document_status(doc_id=add_doc_id)
                    if doc_status == 'verified':
                        add_qul['document_verified'] = doc_status
            if load_json:
                return additional_qualification
            else:
                return json.dumps(additional_qualification)
        else:
            return None



def get_all_client(user_profile):
    '''
    Description: Getting all client Added by requested advisor from local table
    '''
    client_details=''
    client_details = ClientAdvisorMapping.objects.filter(user_profile = user_profile)
    client_list = []
    if client_details:
        for client_detail in client_details:
            temp = {}
            temp['first_name'] = client_detail.client.first_name
            temp['email'] = client_detail.client.email
            temp['mobile'] = client_detail.client.mobile
            temp['created_date'] = str(client_detail.created_date)
            client_list.append(temp)
        client_list = json.dumps(client_list)
        client_list = json.loads(client_list)
    return client_list


def list_client_enquiry(advisor_name, advisor_id, advisor_email):
    '''
    Getting Advisors Enquiry Management Accepted and Rejected list from UPLYF
    '''
    data = {
        "advisor_id" : advisor_id,
		"advisor_name" :advisor_name,
		"advisor_email" : advisor_email
    }
    member_data = ''
    members_data = requests.post(
        api_constants.ENQUIRY_MANAGEMENT_ACCEPT_REJECT_LIST,
        data = data,
        verify = constants.SSL_VERIFY
    )
    if members_data:
        return json.loads(members_data.content)
    else:
        return False

def upload_reingo_transaction_document(trans_document, reingo_id, trans_doc_name):
    '''
    Uploading Reingo Document in UPLYF
    '''
    token = auth_token(settings.UPLYF_USER_NAME, settings.UPLYF_PASSWORD)
    headers = {'Authorization': 'JWT %s' %token['token']}
    filename = os.path.splitext(trans_doc_name)
    data = {
        "reingo_transaction_doc" : trans_document,
        "reingo_trans_id" : reingo_id,
        "doc_name" : filename[0]
    }
    transaction_data = requests.post(
        api_constants.UPLOAD_REINGO_TRANSACTION_DOCUMENT_URL,
        headers=headers,
        data = data,
        verify = constants.SSL_VERIFY
    )
    if transaction_data.status_code == 200:
        return True
    else:
        return False


def get_notification_services_json(user_profile=None, advisor=None):
    '''
    Description : Get json for notification services
    '''
    notifiction_json = {}
    if advisor:
        if not advisor.sms_alert and not user_profile.notification_service:
            notifiction_json['sms_alert'] = False
            notifiction_json['newsletter_alert'] = True
            notifiction_json = json.dumps(notifiction_json)
        elif not user_profile.notification_service:
            notifiction_json['sms_alert'] = True
            notifiction_json['newsletter_alert'] = True
            notifiction_json = json.dumps(notifiction_json)
        else:
            notifiction_json = user_profile.notification_service
    elif not user_profile.notification_service:
        notifiction_json['sms_alert'] = True
        notifiction_json['newsletter_alert'] = True
        notifiction_json = json.dumps(notifiction_json)
    return notifiction_json


def get_practice_contry_details_json(advisor):
    '''
    Descrption: Convert contry details in field into json
    '''
    practice_details_json = []
    practice_details = {}
    if advisor.practice_country and advisor.practice_city and advisor.practice_location:
        practice_details['practice_country'] = advisor.practice_country.name
        practice_details['practice_city'] = advisor.practice_city
        practice_details['practice_location'] = advisor.practice_location
        practice_details['practice_pincode'] = ""
        practice_details_json=[practice_details]
        advisor_practice_details = json.dumps(practice_details_json)
        return advisor_practice_details
    else:
        return None


def get_sms_status(user_status):
    '''
    Description : Get sms_alert for user
    '''
    sms_status = None
    if user_status.notification_service:
        sms_status = json.loads(user_status.notification_service)['sms_alert']
    else:
        sms_status = None
    return sms_status


def get_exp_from_financial_instruments_for_type(str_data, type):
    '''
    Method to get experience for 'type' from advisor financial_instruments column
    return None if 'type' is not present in advisor financial_instruments column
    '''
    try:
        return [int(x['experience'])  for x in json.loads(str_data) if type in x['instruments']][0]
    except Exception as e:
        return 0


def get_number_of_language(lang_str):
    '''
    Getting count of Languages
    '''
    if lang_str != "" or lang_str != None:
        return len(lang_str.split(','))
    return 0


def get_advisor_meetup_hosted_count(user_profile_instance):
    '''
    Getting Advisors Meetup events
    '''
    meetup = MeetUpEvent.objects.filter(user_profile = user_profile_instance)
    if meetup:
        return len(meetup)
    return 0


def get_advisor_webinar_hosted_count(user_profile_instance):
    '''
    Getting Advisors Webinar events
    '''
    webinar = TrackWebinar.objects.filter(user_profile = user_profile_instance)
    if webinar:
        return len(webinar)
    return 0


def get_advisor_rating(user_profile_instance, type_user):
    '''
    Getting Advisors Avg. Rating
    '''
    advisor_rating = AdvisorRating.objects.filter(
        existing_user_profile=user_profile_instance, user_type=type_user)
    avg_rating = 0
    if advisor_rating:
        avg_rating = advisor_rating.exclude(
            avg_rating__lte=0.0).aggregate(
            Avg('avg_rating'))['avg_rating__avg']
        if not avg_rating:
            avg_rating = 0
    return avg_rating


def get_kyc_step_status(request, user, user_profile, advisor):
    kyc_step1 = 'not_filled'
    kyc_step2 = 'not_filled'
    kyc_step3 = 'not_filled'
    kyc_step4 = 'not_filled'
    kyc_step5 = 'not_filled'
    fields_second_step_cnt = 0
    fields_third_step_cnt = 0
    fields_fourth_step_cnt = 0

    # First step check
    document = UploadDocumentsFunctions(request, user_profile)
    proof_of_identity = document.get_document(
        document_type=user_profile.proof_of_identity)
    face_capture = document.get_document(
        document_type='eipv_face_capture')
    ip_details = request.session['ip_info']
    user_agent_country = ip_details.get("country", constants.REGION_DEFAULT)
    if face_capture:
        kyc_step1 = 'completed'
    else:
        kyc_step1 = 'not_filled'

    # second step check
    passport = document.get_document(
        document_type='passport')
    driving_licence = document.get_document(
        document_type='driving_licence')
    id_card = document.get_document(
        document_type='id_card')

    if user_agent_country == 'IN' and user_profile.adhaar_card:
            kyc_step2 = 'completed'
    if not user_agent_country == 'IN':
        if user.profile.country and (passport or driving_licence or id_card):
            kyc_step2 = 'completed'
        else:
            kyc_step2 = 'not_filled'

    # Third step check
    fields_second_step = [
        user_profile.first_name, user_profile.last_name,
        user_profile.gender, user_profile.birthdate, user_profile.mobile,
        user_profile.nationality, user_profile.email, user_profile.address,
        user_profile.city, user_profile.pincode, user_profile.state,
        user_profile.country, advisor.my_promise,
    ]
    if user_agent_country == 'IN':
        fields_second_step += [
            user_profile.father_name, user_profile.mother_name,
            user_profile.pan_no, user_profile.marital_status
        ]
    for fields in fields_second_step:
        if not fields:
            fields_second_step_cnt += 1
    if (fields_second_step_cnt < len(fields_second_step) and
            not fields_second_step_cnt == 0):
                kyc_step3 = 'partial'
    elif fields_second_step_cnt == len(fields_second_step):
        kyc_step3 = 'not_filled'
    else:
        kyc_step3 = 'completed'

    # fourth step check
    fields_third_step = [
        user_profile.language_known, user_profile.mother_tongue, 
        user_profile.languages_known_read_write, user_profile.designation,
        user_profile.company_name, advisor.practice_details]
    for fields in fields_third_step:
        if not fields:
            fields_third_step_cnt += 1

    questions = json.loads(advisor.questions) if advisor.questions else None
    if questions:
        fields_third_step_question = [
            questions[0]['Answer'],
            questions[1]['Answer'],
            questions[2]['Answer'],
            questions[3]['Answer']
        ]
        for question in fields_third_step_question:
            if question == 'undefined':
                fields_third_step_cnt += 1
    else:
        fields_third_step_cnt = 4
    if advisor.is_submitted_questions and fields_third_step_cnt == 0:
        kyc_step4 = 'completed'
    elif fields_third_step_cnt < (len(fields_third_step)+4):
        kyc_step4 = 'partial'
    else:
        kyc_step4 = 'not_filled'

    # Fifth step check
    education = EducationAndCertificationDetails.objects.filter(
        user_profile=user_profile).first()
    if education:
        if education.educational_details:
            kyc_step5 = 'completed'
        elif education.educational_details or education.certification_details:
            kyc_step5 = 'partial'
        else:
            kyc_step5 = 'not_filled'
    else:
        kyc_step5 = 'not_filled'

    return {
        "kyc_step1": kyc_step1,
        "kyc_step2": kyc_step2,
        "kyc_step3": kyc_step3,
        "kyc_step4": kyc_step4,
        "kyc_step5": kyc_step5
    }


def invoice_bill_pdf(user_profile,invoice_id,template_name,context_dict):
    '''
        description:When admin click paid in edit CRISIL Certification modal generating 
            invoice bill in PDF format.
    '''
    transaction_obj = TransactionsDetails.objects.get(invoice_number=invoice_id)
    invoice_sequence = transaction_obj.invoice_number.rsplit('-', 1)
    transaction_obj.invoice_number = invoice_sequence[0] + '-' + str(
        int(invoice_sequence[1]))
    invoice_number = transaction_obj.invoice_number
    description = ''
    total_years_selected = ''
    if transaction_obj.description:
        description = json.loads(transaction_obj.description)
        total_years_selected = int(description['no_of_years_selected'])+int(
            description['offered_years'])
    filename = user_profile.first_name
    filename = filename+".pdf"
    advisor = Advisor.objects.get(user_profile=user_profile)
    communication_email = user_profile.email
    if user_profile.communication_email_id == 'secondary':
        communication_email = user_profile.secondary_email

    if transaction_obj.promo_code:
        discount_amount_percentage = constants.CRISIL_CERTIFICATE_DISCOUNT
        discount_amount = calculate_discount_amount(
            transaction_obj.amount, discount_amount_percentage
        )
    else:
        discount_amount_percentage = 0
        discount_amount = calculate_discount_amount(
            transaction_obj.amount, discount_amount_percentage)
    tax_amount = calculate_tax_amount(discount_amount, constants.TAX_PERCENTAGE_CRISIL)
    context1 = {
        'user_profile'  : user_profile,
        'advisor' : advisor,
        'transaction_obj': transaction_obj,
        'certificate_cost':discount_amount,
        'tax_amount':tax_amount,
        'description':description,
        'total_years_selected':total_years_selected,
        'invoice_number':invoice_number
    }
    resource_directory = os.path.abspath(os.path.dirname(__file__)+"../static/")
    template = get_template('nfadmin/invoice_bill_pdf.html')
    rendered_html = render_to_string("nfadmin/invoice_bill_pdf.html", locals())
    html = template.render(context1)
    file = open(user_profile.first_name+'_'+str(user_profile.id)+'.pdf', "w+b")
    pisaStatus = pisa.CreatePDF(
        html.encode('utf-8'), 
        dest=file, 
        encoding='utf-8',
        link_callback=fetch_resources
    )
    file.seek(0)
    pdf = base64.b64encode(file.read())
    file.close()
    os.remove(os.path.realpath(file.name))
    pdf_attachement = {
        'type':'application/pdf',
        'content':pdf,
        'name':filename
    }
    context_det = { "advisor_name": user_profile.first_name }
    send_mandrill_email_with_attachement(
        template_name, 
        [communication_email], 
        pdf_attachement, 
        context_dict
    )


def get_icore_posts():
    '''
    Method - This method to get icore all posts
    '''
    url_all = settings.ICORE_API_URL+'/posts?filter[posts_per_page]=-1'
    headers_all = {'Content-Type': 'application/json'}
    req_all = requests.get(url_all, headers=headers_all)
    json_res_all = req_all.content.encode('UTF-8')
    token_obj_all = json.loads(json_res_all)
    total_icore_posts = len(token_obj_all)
    return token_obj_all, total_icore_posts


def create_user_from_uploaded_file(advisor_data, user_profile_id):
    """
    Method - To Create the advisors by company using excel file
    """
    failed_users_list = []
    user_profile = UserProfile.objects.filter(id=user_profile_id).first()
    total_no_of_records = len(advisor_data)
    duplicate_no_of_records = 0
    for key, advisor_instance in advisor_data.iteritems():
        advisor_email = None
        try:
            advisor_email = advisor_instance["email"].encode('UTF-8')
            if not re.match('[^@]+@[^@]+\.[^@]+',advisor_email):
                advisor_email = None
            advisor_name = advisor_instance["username"].encode('UTF-8')
            advisor_mobile = str(advisor_instance["mobile"])
            advisor_reg_no = advisor_instance["reg_no"]
            advisor_years_of_experience = str(advisor_instance["years_of_experience"])
            if advisor_email == "nan" or advisor_email == "":
                advisor_email = None
            if advisor_email:
                password = get_random_string(length=8)
                from login.common_views import LoginCommonFunctions
                direct_signup = LoginCommonFunctions({'request':""})
                data = {
                    'email' : advisor_email,
                    'password' : password,
                    'first_name' : advisor_name,
                    'mobile' : advisor_mobile
                }
                is_created = direct_signup.createuser(
                    object = data
                )
                advisor_profile = is_created['user_profile']
                if is_created['status'] == 201:
                     if not advisor_profile.registration_id:
                        while(True):
                            num =  uuid.uuid4().hex[:10]
                            if not UserProfile.objects.filter(registration_id = num):
                                advisor_profile.registration_id = num
                                advisor_profile.save()
                                break
                            else:
                                continue
                if is_created['status'] == 200:
                    duplicate_no_of_records +=1
                advisor_obj = advisor_profile.advisor
                company_details = AffiliatedCompany.objects.filter(
                    user_profile=user_profile).first()
                if company_details:
                    advisor_questions = add_company_to_advisor_question_json(
                        company_name = company_details.company_name,
                        advisor = advisor_obj,
                        company_url = company_details.website_url,
                        domain = company_details.domain_name,
                        reg_no = advisor_reg_no,
                        years_of_exp = advisor_years_of_experience
                    )
                    if advisor_questions:
                        advisor_obj.questions = advisor_questions
                        advisor_obj.save()
                company_profile = user_profile
                advisor_map,status_ad = CompanyAdvisorMapping.objects.get_or_create(
                    company_user_profile=company_profile, advisor_user_profile=advisor_profile
                )
                if status_ad:
                    advisor_map.status = 'not_approved'
                    advisor_map.save()
            else:
                failed_users_list.append(advisor_instance)
        except Exception as e:
            if advisor_email:
                user_exception = {advisor_email : str(e)}
                failed_users_list.append(user_exception)
            else:
                failed_users_list.append(advisor_instance)
        # successful data upload
        if len(failed_users_list) == 0:
            send_mandrill_email('REIA_25_01',
                [user_profile.email],
                context = {
                    'company_name':user_profile.first_name,
                    'no_of_records':total_no_of_records,
                    'admin_user_name':'admin',
                    'date_of_upload':datetime.datetime.today().strftime('%d %b, %Y'),
                    'time_of_upload':datetime.datetime.today().strftime('%H:%M')
                }
            )
        else:                          # unsuccessful data upload
            send_mandrill_email('REIA_25_02',
                [user_profile.email],
                context={
                    'company_name':user_profile.first_name,
                    'total_no_of_records': total_no_of_records,
                    'records_updated_in_DB': total_no_of_records-(\
                        duplicate_no_of_records+len(failed_users_list)),
                    'records_to_be_uploaded': len(failed_users_list),
                    'no_of_records': duplicate_no_of_records,
                    'admin_user_name': 'admin',
                    'date_of_upload':datetime.datetime.today().strftime('%d %b, %Y'),
                    'time_of_upload':datetime.datetime.today().strftime('%H:%M')
                }
            )


def add_company_to_advisor_question_json(company_name=None, advisor=None,
                                            company_url=None, domain=None,
                                            reg_no=None, years_of_exp=None):
    '''
    Description: Adding company data into financial origanisation json present in advsior
        questions
    '''
    if company_name and advisor and company_url and domain:
        advisor_questions = advisor.questions
        reg_id = advisor.user_profile.email if not reg_no else reg_no
        if advisor_questions:
            existing_questions = json.loads(advisor_questions)
            financial_organisation_json = existing_questions[2]['Remark'][0]['Remark']
            if not domain in json.dumps(financial_organisation_json):
                company_name = '{"Answer": "'+company_name+'", \
                    "Question": "'+signup_constants.THIRD_REMARK_SUB_QUESTION1+'"}'
                company_url = '{"Answer": "'+company_url+'", \
                    "Question": "'+signup_constants.THIRD_REMARK_SUB_QUESTION2+'"}'
                ad_com_reg_id = '{"Answer": "'+reg_id+'", \
                    "Question": "'+signup_constants.THIRD_REMARK_SUB_QUESTION3+'"}'
                y_of_exp = '{"Answer": "'+years_of_exp+'", \
                    "Question": "'+signup_constants.THIRD_REMARK_SUB_QUESTION4+'"}'
                new_comp_attr = [company_name, company_url, ad_com_reg_id, y_of_exp]
                if financial_organisation_json:
                    for i in range(0,4):
                        financial_organisation_json.append(json.loads(new_comp_attr[i]))
                    existing_questions[2]['Remark'][0]['Answer'] = \
                        str(int(existing_questions[2]['Remark'][0]['Answer']) + 1)
                else:
                    new_financial_organisation = '['
                    for index, val in enumerate(new_comp_attr, start=1):
                        if not index == len(new_comp_attr):
                            new_financial_organisation=new_financial_organisation+val +','
                        else:
                            new_financial_organisation=new_financial_organisation+val+']'
                    existing_questions[2]['Answer'] = 'yes'
                    existing_questions[2]['Remark'][0]['Answer'] = '1'
                    existing_questions[2]['Remark'][0]['Remark'] = json.loads(
                        new_financial_organisation)
            return json.dumps(existing_questions)
        else:
            questions = [
                {
                    "Question":signup_constants.FIRST_QUESTION,
                    "Answer":"undefined",
                    "Remark":[
                        {
                            "Question":signup_constants.FIRST_REMARK_SUB_QUESTION1,
                            "Answer":""
                        },
                        {
                            "Question":signup_constants.FIRST_REMARK_SUB_QUESTION2,
                            "Answer":""
                        },
                        {
                            "Question":signup_constants.FIRST_REMARK_SUB_QUESTION3,
                            "Answer":""
                        }
                    ]
                },
                {
                    "Question":signup_constants.SECOND_QUESTION,
                    "Answer":"undefined",
                    "Remark":""
                },
                {
                    "Question":signup_constants.THIRD_QUESTION,
                    "Answer":"yes",
                    "Remark":[
                        {
                            "Question":signup_constants.THIRD_SUB_QUESTION1,
                            "Answer":"1",
                            "Remark":[
                                {
                                    "Question":signup_constants
                                        .THIRD_REMARK_SUB_QUESTION1,
                                    "Answer":company_name
                                },
                                {
                                    "Question":signup_constants
                                        .THIRD_REMARK_SUB_QUESTION2,
                                    "Answer": company_url
                                },
                                {
                                    "Question":signup_constants
                                        .THIRD_REMARK_SUB_QUESTION3,
                                    "Answer": reg_id
                                },
                                {
                                    "Question":signup_constants
                                        .THIRD_REMARK_SUB_QUESTION4,
                                    "Answer": years_of_exp
                                }
                            ]
                        }
                    ]
                },
                {
                    "Question":signup_constants.FOURTH_QUESTION,
                    "Answer":"undefined"
                }
            ]
            return json.dumps(questions)
    else:
        return None


def get_advisor_education_detils(up_instance):
    '''
    This method is for getting only education details of an advisor
    parameter : userprofile instance
    returns : dict json of qualification
    '''
    edu_json = []
    if up_instance:
        if up_instance.qualification and up_instance.year_passout:
            higher_qualification = {
                "deg":str(up_instance.qualification), 
                "year":str(up_instance.year_passout)
            }
            edu_json.append(higher_qualification)
        if up_instance.additional_qualification:
            for qualification in json.loads(up_instance.additional_qualification):
                add_qual_json = {
                    "deg":str(qualification['additional_qualification']),
                    "year":str(qualification['year_passout'])
                }
                edu_json.append(add_qual_json)
    return edu_json


def get_no_of_regulatory_registrations(advisor_instance):
    '''
    Getting advisors regulatory registrations(sebi,rera,irda)
    parameter : advisor instance
    returns : count of regulatory registrations and json of regulatory registrations
        validated
    '''
    user_profile_id = advisor_instance.user_profile.id
    no_reg_regs = 0
    no_reg_regs_validate = {}
    no_reg_regs = no_reg_regs+1 if advisor_instance.sebi_number else no_reg_regs
    no_reg_regs = no_reg_regs+1 if advisor_instance.irda_number else no_reg_regs
    if advisor_instance.rera_details :
        no_reg_regs = no_reg_regs + 1
        no_reg_regs_validate["rera"] = True
    #Check Sebi data for advisor
    sebi = SebiData.objects.filter(advisor_id = user_profile_id)
    if sebi:
        no_reg_regs_validate["sebi"] = True
    #Check Irda data for advisor
    irda = IrdaData.objects.filter(advisor_id = user_profile_id)
    if irda:
         no_reg_regs_validate["irda"] = True
    no_reg_regs_validate = no_reg_regs_validate if no_reg_regs_validate else None
    return no_reg_regs, no_reg_regs_validate


def get_advisor_associated_organization_count(up_instance):
    '''
    Getting advisors associated_organizations count
    parameter : userprofile instance
    returns : count of associated_organizations with advisor
    '''
    company_adv_mapp_count = 0
    company_adv_mapp = CompanyAdvisorMapping.objects.filter(
        advisor_user_profile=up_instance)
    if company_adv_mapp:
        company_adv_mapp_count = company_adv_mapp.count()
    return company_adv_mapp_count


def get_practice_locations(adv_instance):
    '''
    Getting advisors practice locations
    parameter : advisor instance
    returns : array of picodes
    '''
    practice_pincode = []
    if adv_instance.practice_details:
        practice_details = json.loads(adv_instance.practice_details)
        for pd in practice_details:
            practice_pincode.append(str(pd['practice_pincode']))
    return practice_pincode


def get_advisor_level(request, user, advisor):
    '''
    Description: Calculating Advisor level based on no of advisors referred and registered
        and minimum value of avg rating and ranking done by all advisors and external users
    '''
    advisor_level = ''
    clients_level = ''
    advisor_comm_obj = AdvisorCommonFunction(request)
    rating_and_ranking_comm_obj = RatingAndRankingCommonFunctions(request, advisor)
    '''
    Referred registered advisors
    '''
    refered_advisors = advisor_comm_obj.get_reffred_registered_advisors_count(
        object=user
    )
    '''
    Rating count with avg rating 3.0
    '''
    rating_count = rating_and_ranking_comm_obj.get_all_rated_by_advisor_count(
        constants.MINIMUM_AVG_RATING,
    )
    '''
    Ranking count with avg rating 3.0
    '''
    ranking_count = rating_and_ranking_comm_obj.get_all_ranked_by_advsior_count(
        constants.MINIMUM_AVG_RATING,
    )

    # if advisor refer 100 registered advisors than that advisor is CONNECTED
    if refered_advisors >= constants.FIRST_LEVEL_MINIMUM_ADVISOR_COUNT \
        and refered_advisors <= constants.SECOND_LEVEL_MINIMUM_ADVISOR_COUNT:
            advisor_level = constants.CONNECTED

    # if advisor refer >=500 registered advisors than that advisor is WELL_CONNECTED
    if refered_advisors >= constants.SECOND_LEVEL_MINIMUM_ADVISOR_COUNT:
        advisor_level = constants.WELL_CONNECTED

    # if advisor rated by 500+ advisors with minimum avg 3.0
    # than that advisor is HIGHLY_CONNECTED
    if rating_count >= constants.SECOND_LEVEL_MINIMUM_ADVISOR_COUNT:
        advisor_level = constants.HIGHLY_CONNECTED

    # if advisor add >=500 members with minimum advisors avg rating 3.0 and rated
    # advisors are 500+ than that advisor is TRUSTED
    if rating_count >= constants.SECOND_LEVEL_MINIMUM_ADVISOR_COUNT \
        and refered_advisors >= constants.SECOND_LEVEL_MINIMUM_ADVISOR_COUNT:
            advisor_level = constants.TRUSTED

    # if advisor is ranked by >=500 members with minimum 3.0 rating
    # then that advisor is LARGE_CLIENT_BASED
    if ranking_count >= constants.SECOND_LEVEL_MINIMUM_ADVISOR_COUNT:
        clients_level = constants.LARGE_CLIENT_BASED

    # if advisor is HIGHLY_CONNECTED and LARGE_CLIENT_BASED
    # than that advisor is MOST_TRUSTED
    if rating_count >= constants.SECOND_LEVEL_MINIMUM_ADVISOR_COUNT \
            and clients_level == constants.LARGE_CLIENT_BASED:
            clients_level = constants.MOST_TRUSTED

    # if advisor is MOST_TRUSTED and CRISIL verified than that advisor is TEA
    if clients_level == constants.MOST_TRUSTED:
        if advisor_obj.is_crisil_verified:
            advisor_level = constants.TRUSTED_ECONOMIC_ADVISOR

    del(advisor_comm_obj)
    del(rating_and_ranking_comm_obj)

    data = {
        "advisor_level":advisor_level,
        "clients_level":clients_level
    }
    return data


def customize_sorted_list(data_dict, keyorder):
    '''
    Changing the json with new set of keys
    parametes: 
        data_dict: expects dict json
        keyorder: new key list set
    '''
    result = []
    for key in keyorder:
        res = {}
        if key in data_dict.keys():
            res[key] = data_dict[key]
            result.append(res)
    result=json.dumps(result)
    return result


def get_remove_rera_doc(request, old_rera_json, new_rera_json):
    '''
    Returns removed document ids from rera json

    Parametes:
        old_rera_json: need to pass old rera json
        new_rera_json: need to pass new rera json
    
    Compares new rera json with old rera json and returns removed rera_certificate 
        and rera_renewal_certificate ids from old rera
    '''
    final_cert_ids = []
    old_cert_ids = []
    new_cert_ids = []

    if old_rera_json:
        old_rera_json = json.loads(old_rera_json)
        for rera_json in old_rera_json:
            rera_cert = rera_json.get('rera_certificate', None)
            rera_renew_cert= rera_json.get('rera_renewal_certificate', None)
            if rera_cert:
                old_cert_ids.append(rera_cert)
            if rera_renew_cert:
                old_cert_ids.append(rera_renew_cert)
        if old_cert_ids:
            old_cert_ids = ",".join(old_cert_ids).split(',')

    if new_rera_json:
        new_rera_json = json.loads(new_rera_json)
        for rera_json in new_rera_json:
            rera_cert = rera_json.get('rera_certificate', None)
            rera_renew_cert = rera_json.get('rera_renewal_certificate', None)
            if rera_cert:
                new_cert_ids.append(rera_cert)
            if rera_renew_cert:
                new_cert_ids.append(rera_renew_cert)
        if new_cert_ids:
            new_cert_ids = ",".join(new_cert_ids).split(',')

    for old_ids in old_cert_ids:
        if not old_ids in new_cert_ids:
            final_cert_ids.append(old_ids)

    return final_cert_ids


def check_rera_reg_state_same_as_practice_state(adv_instance):
    '''
    Checking rera registration states and practice states and returning common states
    '''
    return_val = 0
    if adv_instance:
        if adv_instance.rera_details:
            states = get_practice_state_by_advisor_instance(adv_instance)
            if states:
                rera_details = json.loads(adv_instance.rera_details)
                for rd in rera_details:
                    if rd['rera_state']:
                        if rd['rera_state'].lower() in states:
                            return_val = 2
                            break
                        else:
                            return_val = 1
    return return_val


def get_practice_state_by_advisor_instance(adv_instance):
    '''
    Returning Practice states as List
    '''
    result = []
    if adv_instance:
        if adv_instance.practice_details:
            pract_details = json.loads(adv_instance.practice_details)
            pin_list = [pd['practice_pincode']
                      for pd in pract_details if pd['practice_pincode']]
            ind_pc = India_Pincode.objects.filter(
                pin_code__in=pin_list
            ).values_list('state_name')
            result = list(set([st_nm[0].lower() for st_nm in ind_pc if st_nm]))
    return result


def get_adv_rate_count_by_user_type(adv_instance, user_type):
    """
    This method returns count of rating present for advisor and type
    percentage of average rating out of 5
    """
    ar = AdvisorRating.objects.filter(advisor=adv_instance, user_type=user_type)
    r_count = ar.count()
    avg_percent = 0
    if ar:
        avg_rating = ar.aggregate(Avg('avg_rating'))['avg_rating__avg']
        if avg_rating > 0:
            avg_percent = (avg_rating/5)*100
    return r_count, avg_percent


def mlegion_auth_token(username, password):
    '''
    Descrption: Generate token to establsih a connection with MLEGION
    '''
    if username and password:
        auth_credentials = {
            'username' : username,
            'password' : password
        }
        auth_response = requests.post(
            api_constants.MLEGION_AUTH_TOKEN_URL,
            data = auth_credentials,
            verify = constants.SSL_VERIFY
        )
        token = json.loads(auth_response.content.encode('UTF-8'))
        return token
    else:
        return False


def get_ip_region(request):
    ip_details = request.session['ip_info']
    user_agent_country = ip_details.get("country", constants.REGION_DEFAULT)
    return user_agent_country

