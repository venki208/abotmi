import logging, hashlib, datetime, random
import json,requests,base64,uuid
from datetime import datetime, timedelta
import time
from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.contrib.auth import login
from django.http import HttpResponse,JsonResponse, HttpResponseRedirect
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum,Avg
from django.conf import settings
from django.core import serializers
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_jwt.settings import api_settings
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import status
from tld import get_tld
from aadhaar import conf as local_settings
from common import constants,api_constants
from common.utils import calculate_final_amount_with_discount_and_tax_amount,JSONEncoder
from num2words import num2words
from time import strftime,gmtime


from login.common_views import LoginCommonFunctions
from login.views import email_signup,send_signup_otp,resend_email_mobile_otps,validate_otp,user_logout
from dashboard.forms import PaymentForm
from dashboard.views import manage_uplyf_transaction, save_calendly_link
from my_identity.views import update_contact_details,save_total_advisors_connected_count,\
    save_total_clients_served_count, save_self_declaration, save_education, save_certification
from my_growth.views import index as my_growth_index
from webinar import views as webinar_views
from meetup.views import create_meetup_event,list_meetup_events,delete_meetup_event_from_post,list_mail_invitation,send_meetup_invitation, update_events
from signup.views import upload_eipv_documents,submit_eipv,send_otp,verify_otp, personal_info_forms, submit_eipv_doc, \
    save_foot_print_verification, delete_foot_print_verification, user_profile_answer, register, user_profile_basicdetails,check_email
from signup.views import educational_qualification,delete_upload_file,aadhaar_verification
from common.views import (social_media_like_count_bg_process, social_media_like_count, 
    top_three_post,get_all_members, get_invited_members, referral_points,invoice_gen, 
    logme, get_binary_image, check_crisil_advisor, generate_pdf,auth_token, 
    get_sms_status, get_ipinfo,get_kyc_step_status
)
from advisor_check.views import check_advisor_claimed

from common.constants import SSL_VERIFY, FASIAAMERICA, FASIA_DOMAIN, FASIA_COMPANY_EMAIL

from api.serializers import UserSerializer, UserProfileSerializer, USerializer, \
    MeetupSerializer, WebinarSerializer, AdvisorSerializer, AdvisorRegistrationSerializer,UploadDocumentSerializer

from signup.djmail import send_mandrill_email, send_mandrill_email_with_attachement,\
    send_mandrill_email_dynamic_from, send_mandrill_email_admin, send_mandrill_email_admin_subject
from common.utils import generate_key, send_sms_alert

from datacenter.models import Advisor, EmailVerification, UserProfile,India_Pincode, ExternalUser,\
    AdvisorRating, TrackReferrals, Member, AdvisorType, PromoCodes,AadhaarTransactions,TransactionsDetails,\
    UploadDocuments, MeetUpEvent, TrackWebinar,CompanyAdvisorMapping,AffiliatedCompany,Country, \
    AdvisorVideoRequest, DigitalFootPrint,EducationAndCertificationDetails

from wordpress_xmlrpc import Client,WordPressPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media,posts
from wordpress_xmlrpc.methods.posts import NewPost

import dashboard
import my_identity

# from rest_framework import serializers
# from rest_framework_mongoengine import serializers as document_serializers

logger = logging.getLogger(__name__)


# sample obtain token call is
# curl -X POST -d "username=<username>&password=<password>" http://localhost:8000/api/get-auth-token/

# using the token, you may call to get details like below
# curl  -X GET http://localhost:8000/api/get-user-list/ -H 'Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImJhbGFqaSIsInVzZXJfaWQiOiJiYWxhamkiLCJlbWFpbCI6IiIsImV4cCI6MTQ0NDE0NDA3Mn0.p9zmXU22NG2z9tfyDlHb11PxJNwOkXlf5PfGZqxPSOY'

# data post can be done like the following
# curl  -X POST http://localhost:8000/api/api-token-verify/ -H 'Content-Type: Application/json' -d '{"token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImJhbGFqaSIsInVzZXJfaWQiOiJiYWxhamkiLCJlbWFpbCI6IiIsImV4cCI6MTQ0NDE0NDA3Mn0.p9zmXU22NG2z9tfyDlHb11PxJNwOkXlf5PfGZqxPSOY"}'


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)



@api_view(['GET'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_user_list(request):
    logger.debug("Testing")
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    logger.info(
        logme('returned all advisors list', request)
    )
    return JSONResponse(serializer.data, status=201)


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def is_register_user(request):
    user_obj = request.user
    user_profile_obj = user_obj.profile
    advisor_obj = user_profile_obj.advisor
    is_reg_user = advisor_obj.is_register_advisor
    is_confirmed =  advisor_obj.is_confirmed_advisor
    result = get_kyc_step_status(request, user_obj, user_profile_obj, advisor_obj)
    # if is_reg_user and is_confirmed:
    #     logger.info(
    #         logme('validation - user confirmed registered', request)
    #     )
    #     return JSONResponse("Confirmed",status=200)
    # elif not is_confirmed and  is_reg_user:
    #     logger.info(
    #         logme('validation - user registered', request)
    #     )
    #     return JSONResponse("Registered",status=200)
    # else:
    #     logger.info(
    #         logme('validation - user not registered', request)
    #     )
    #     return JSONResponse("Not Registered",status=200)
    logger.info(
        logme('validation - user registered status %s'%(str(is_reg_user)), request)
    )
    return JSONResponse(result,status=200)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def is_registerd_user(request):
    user_obj = request.user
    user_profile_obj = user_obj.profile
    advisor_obj = user_profile_obj.advisor
    is_reg_user = advisor_obj.is_register_advisor
    is_confirmed =  advisor_obj.is_confirmed_advisor
    # result = get_kyc_step_status(request, user_obj, user_profile_obj, advisor_obj)
    if is_reg_user and is_confirmed:
        logger.info(
            logme('validation - user confirmed registered', request)
        )
        return JSONResponse("Confirmed",status=200)
    elif not is_confirmed and  is_reg_user:
        logger.info(
            logme('validation - user registered', request)
        )
        return JSONResponse("Registered",status=200)
    else:
        logger.info(
            logme('validation - user not registered', request)
        )
        return JSONResponse("Not Registered",status=200)
    logger.info(
        logme('validation - user registered status %s'%(str(is_reg_user)), request)
    )
    return JSONResponse(is_reg_user,status=200)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def is_adharregister_user(request):
    user_obj = request.user
    user_profile_obj = user_obj.profile
    is_adhaaar = user_profile_obj.adhaar_card
    if is_adhaaar :
        return JSONResponse("Aadhaar",status=200)  
    else:
        return  JSONResponse("Not_Aadhaar_present",status=302) 

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_user_details(request):
    logger.debug("Testing")
    user = request.user
    serializer = UserSerializer(user)
    logger.info(
        logme('returned advisor=%s details'%(str(user)), request)
    )
    return JSONResponse(serializer.data, status=201)


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def user_createpassword(request):
    context = RequestContext(request)
    oldpassword = request.POST['oldpassword']
    newpassword = request.POST['newpassword']
    if request.user.check_password(oldpassword):
        request.user.set_password(newpassword)
        request.user.save()
        logger.info(
            logme('advisor password changed successfully', request)
        )
        return JSONResponse({'data': 'success'}, status=200)
    else:
        logger.info(
            logme(
                'advisor entered wrong old password, redirected to change password',
                request
            )
        )
        return JSONResponse({'data':'Wrong Old Password'})


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def create_webinar_mobile(request):
    response = webinar_views.create_webinar(request)
    return JsonResponse({'data': response}, status=200)


@api_view(['GET'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def uplyfdetails_mobile(request):
    response = create_meetup_event(request)
    return JsonResponse({'data': response}, status=200)


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def aadhar_verification_data(request):
    user = request.user
    user_profile = user.profile
    advisor = user_profile.advisor
    country_data=user_profile.country
    passport = UploadDocuments.objects.filter(user_profile=user_profile,documents_type='passport')
    serializer_passport = UploadDocumentSerializer(passport,many=True)
    driving_licence = UploadDocuments.objects.filter(user_profile=user_profile,documents_type='driving_licence')
    serializer_driving_data = UploadDocumentSerializer(driving_licence,many=True)
    id_card = UploadDocuments.objects.filter(user_profile=user_profile,documents_type='id_card')
    id_card_data = UploadDocumentSerializer(id_card,many=True)
    return JsonResponse({'passport_data': serializer_passport.data,'driving_licence':serializer_driving_data.data,"id_card":id_card_data.data,"country_data":country_data}, status=200)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def create_meetup_mobile(request):
    response = create_meetup_event(request)
    return JsonResponse({'data': response}, status=200)


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def delete_meetup_event_mobile(request):
    response = delete_meetup_event_from_post(request)
    return response 


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def meetupupdate(request):
    response = update_events(request)
    return JsonResponse({"data": response}, status=200)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def save_educationDetails(request):
    response = save_education(request)
    return response

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def save_certificationDetails(request):
    response = save_certification(request)
    return response

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def delete_webinar_event_mobile(request):
    response = webinar_views.delete_webinar(request)
    return JsonResponse({'data': response}, status=200)


@api_view(['GET'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def list_mail_invitation_mobile(request):
    response = []
    response = list_mail_invitation(request)
    return JsonResponse({'data': response}, status=200)


@api_view(['GET'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def list_meetup_mobile(request):
    response = list_meetup_events(request)
    event_list = MeetupSerializer(response, many=True)
    return JsonResponse({'data': event_list.data}, status=200)


def default(o):
  if type(o) is datetime.date or type(o) is datetime:
    return o.isoformat()


@api_view(['GET'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def list_webinar_mobile(request):
    response = webinar_views.dashboard(request)
    event_torate_list = []
    for event in response:
        event_dict = {}
        event_dict['id'] = event.id
        event_dict['room_id'] = event.room_id
        event_dict['room_name'] = event.room_name
        event_dict['room_url'] = event.room_url
        event_dict['room_pin'] = event.room_pin
        event_dict['password'] = event.password
        now_timestamp = time.time()
        offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
        time_event_webinar = event.starts_at + offset
        event_dict['starts_at'] = datetime.strftime(
            time_event_webinar, "%d-%m-%Y %H:%M")
        event_dict['uplyf_project'] = event.uplyf_project
        event_torate_list.append(event_dict)
    return JsonResponse({'data': event_torate_list}, status=200)


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_user_profile(request):
    logger.debug("Testing")
    user = request.user.profile
    serializer = UserProfileSerializer(user)
    logger.info(
        logme('returned advsior=%s details' % (str(user)), request)
    )
    return JSONResponse(serializer.data, status=200)


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def test_list(request):
    logger.debug("Testing")
    td = [{'name': 'mobisir', 'age': '6'},
          {'name': 'arthavidhya', 'age': '7'},
          {'name': 'northfacing', 'age': '1'}]
    serializer = USerializer(td, many=True)
    logger.info(
        logme('returned test list', request)
    )
    return JSONResponse(serializer.data, status=201)


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_profile_details(request):
    '''
        Sending details(
            Name,My Belife,My Promises,Peer Rating Details, Client Ranking Details, 
            Register type
            certificate Details(SEBI,IRDA....), Advisor profile referral code
        ) using API
    '''
    # fetching rating details
    user_obj = request.user
    user_profile_obj = user_obj.profile
    advisor_obj = user_profile_obj.advisor
    advisor_status = advisor_obj.crisil_application_status
    advisor_rate_invites = AdvisorRating.objects.filter(
            advisor=advisor_obj,
            user_type='advisor'
        )
    total_no_invites_to_rate = 0
    total_no_rated = 0
    final_peer_avg_rating = 0.0
    total_members = 0
    product_experience = []
    if advisor_rate_invites:
        total_no_invites_to_rate = advisor_rate_invites.count()
        total_no_rated = advisor_rate_invites.exclude(avg_rating__lte=0.0).count()
        final_peer_avg_rating = advisor_rate_invites.exclude(avg_rating__lte=0.0).aggregate(Avg('avg_rating'))['avg_rating__avg']
    advisor_member_ratings = AdvisorRating.objects.filter(
        advisor=advisor_obj,
        user_type='member'
    )
    feedbacks = (AdvisorRating.objects.filter(
            advisor=advisor_obj,
            user_type='member').exclude(feedback__isnull=True)).values_list('feedback')
    if (len(feedbacks) != 0) and (not feedbacks):
        feedbacks = json.loads(feedbacks)
    total_ranked_invites = 0
    total_member_ranks = 0
    final_consumer_avg_ranking = 0
    total_reffered_advisor_count = 0
    referred_registered_advisor_count = 0
    # if advisor_member_ranks:
    #     total_ranked_invites = advisor_member_ranks.count()
    #     total_member_ranks = advisor_member_ranks.filter(rating__lte=0.0).count()
    #     final_consumer_avg_ranking = advisor_member_ranks.exclude(rating__lte=0.0).aggregate(Avg('rating'))['rating__avg']

    if advisor_member_ratings:
        total_ranked_invites += advisor_member_ratings.count()
        total_member_ranks += advisor_member_ratings.exclude(
            avg_rating__lte=0.0).count()
        if advisor_member_ratings.exclude(avg_rating__lte=0.0):
            new_rating = (
                final_consumer_avg_ranking + advisor_member_ratings.exclude(
                    avg_rating__lte=0.0).aggregate(
                    Avg('avg_rating'))['avg_rating__avg']
            )
            if new_rating > final_consumer_avg_ranking and final_consumer_avg_ranking != 0:
                final_consumer_avg_ranking = new_rating / 2
            else:
                final_consumer_avg_ranking = new_rating

    total_reffered_advisor_count = TrackReferrals.objects.filter(
        referred_by=user_profile_obj).count()
    referred_registered_advisor_count = Advisor.objects.filter(
        is_register_advisor=True,
        user_profile__referred_by=user_obj
        ).count()
    if total_reffered_advisor_count:
        referred_unregistered_advisor_count = total_reffered_advisor_count - referred_registered_advisor_count
    else:
        total_reffered_advisor_count = referred_registered_advisor_count
        referred_unregistered_advisor_count = 0
    crisil_final = {}
    # Member Deatils
    members = 0
    total_members = 0
    registered_member = 0
    un_registered_members = 0
    if members:
        total_members = len(members['content'])
        registered_member = members['members_registered_count']
        un_registered_members = total_members - registered_member

    promo_code = PromoCodes.objects.filter(user_profile=user_profile_obj)
    if promo_code:
        promo_code = promo_code.values_list('promo_code')
    crisil_details = TransactionsDetails.objects.filter(user_profile=user_profile_obj)
    if crisil_details:
        crisil_final = {
            'amount': crisil_details[0].discounted_amount,
            'bankname': crisil_details[0].bank_name,
            'cheque_no': crisil_details[0].cheque_dd_no,
            'cheque_date': crisil_details[0].cheque_dd_date
        }
    advisor_status = advisor_obj.crisil_application_status
    discount_percentage = 0
    crisil_reg_no = ''
    crisil_expiry_date = ''
    if advisor_status == constants.CRISIL_GOT_CERTIFICATE:
        crisil_reg_no = advisor_obj.crisil_registration_number
        crisil_expiry_date = advisor_obj.crisil_expiry_date
    no_of_years_selected = ''
    transaction_object = TransactionsDetails.objects.filter(user_profile=user_profile_obj)
    if transaction_object:
        transaction_object = transaction_object.first()
        description = json.loads(transaction_object.description)
        no_of_years_selected = int(description['no_of_years_selected']) \
            + int(description['offered_years'])


    if advisor_status == constants.CRISIL_EXPIRED:
        crisil_amount = calculate_final_amount_with_discount_and_tax_amount(
                constants.CRISIL_CERTIFICATE_VALUE,
                constants.CERTIFICATE_RENEWAL_YEAR,
                discount_percentage,
                constants.TAX_PERCENTAGE_CRISIL
            )
    else :
        crisil_amount = calculate_final_amount_with_discount_and_tax_amount(
                constants.CRISIL_CERTIFICATE_RENEWAL_VALUE,
                constants.CERTIFICATE_RENEWAL_YEAR,
                discount_percentage,
                constants.TAX_PERCENTAGE_CRISIL
            )
    no_of_years_selected = ''
    if crisil_details:
        crisil_details = crisil_details.first()
        description = json.loads(crisil_details.description)
        no_of_years_selected = int(description['no_of_years_selected']) + int(description['offered_years'])
    # STREAM_URL = settings.STREAM_URL
    # stream_course_details_json = None
    # get_all_stream_course_json=None
    # if advisor_obj.is_stream_user:
    #     stream_course_details_json = stream_views.get_stream_course_details(
    #             request, user_profile_obj, advisor_obj)
    #     # check for couse status
    #     if stream_course_details_json:
    #         certification_title = []
    #         course_test_status = False
    #         for objects in stream_course_details_json:
    #             if objects['course_percentage'] >= 50:
    #                 course_test_status = True
    #                 course_dict = {
    #                     'course_id': objects['course_id'],
    #                     'course_nam': objects['course_name'],
    #                     'course_test_status': objects['course_test_status']
    #                 }
    #                 certification_title.append(course_dict)

    #         if course_test_status:
    #             advisor_object = Advisor.objects.get(user_profile=user_profile_obj)
    #             advisor_object.is_certified_advisor = True
    #             advisor_object.certification_title = certification_title
    #             advisor_object.reia_level = constants.REIA_LEVEL_2
    #             advisor_object.save()
    # commented for now once upwrdz team done the functionality , we will uncomment
    # get_all_stream_course_json = stream_views.get_all_stream_course(request,user_obj)
    # practice_country = ''
    # practice_city = ''
    # if advisor_obj.practice_country:
    #     practice_country = advisor_obj.practice_country.name
    #     practice_city = advisor_obj.practice_city
    practice_details = advisor_obj.practice_details if advisor_obj.practice_details else ''
    educational_details, certification_details = None, None
    education_obj = EducationAndCertificationDetails.objects.filter(
            user_profile=user_profile_obj).first()

    if education_obj:
        educational_details = json.loads(education_obj.educational_details)[0]
        certification_details = json.loads(education_obj.certification_details)
    rera_details = advisor_obj.rera_details
    if rera_details:
        rera_details = json.loads(rera_details)
    else:
        rera_details = constants.RERA_VALUES_NULL_JSON
    dsa_details = advisor_obj.dsa_details
    if dsa_details:
        dsa_details = json.loads(dsa_details)
    else:
        dsa_details = constants.DSA_RESULTS_NULL_JSON
    advisory_ins = advisor_obj.financial_instruments
    if advisory_ins:
        advisory_ins = json.loads(advisory_ins)
    else:
        advisory_ins = constants.FINANCIAL_INSTRUMENT_NULL_JSON
    instruments = constants.ALL_FINANCIAL_INSTRUMENT
    additional_qualification_list = user_profile_obj.additional_qualification
    if additional_qualification_list:
        additional_qualification_list = json.loads(additional_qualification_list)
    else:
        additional_qualification_list = []
    question = advisor_obj.questions
    val = request.POST.get('req_type', None)
    if val == 'mobile':
        if question:
            question = json.loads(question)
            if question[1]['Remark']:
                question[1]['Remark'] = question[1]['Remark'].replace("!"," ")
                question[1]['Remark'] = question[1]['Remark'].replace("$","\n")
    else:
        if question:
            question = json.loads(question)
    product_experience = advisor_obj.financial_instruments
    if product_experience:
        product_experience = json.loads(product_experience)

    profile_picture = ""
    if user_profile_obj.picture:
        profile_picture = get_binary_image(user_profile_obj)

    # ICORE latest posts
    url_all = settings.ICORE_API_URL+'/posts?filter[posts_per_page]=-1'
    headers_all = {'Content-Type': 'application/json'}
    req_all = requests.get(url_all, headers=headers_all)
    json_res_all = req_all.content.encode('UTF-8')
    token_obj_all = json.loads(json_res_all)
    total_icore_posts = len(token_obj_all)
    icore_posts_list = []
    post_data = []
    authorpost_list = []
    commentpost_list = []

    for icorepost in token_obj_all[:3]:
        icore_dict = {}
        icore_dict["ID"] = icorepost["ID"]
        icore_dict["title"] = icorepost["title"]
        icore_dict["link"] = icorepost["link"]
        icore_posts_list.append(icore_dict)

    pancard_detail = None
    if user_profile_obj.pan_no:
        pancard_detail = user_profile_obj.pan_no
    author_post_url = settings.ICORE_API_URL+'/posts/author/'+str(advisor_obj.wordpress_user_id)
    headers = {'Content-Type': 'application/json'}
    author_post_req = requests.get(author_post_url, headers=headers_all)
    author_post_res = author_post_req.content.encode('UTF-8')
    author_post_json_res = json.loads(author_post_res)
    total_author_post = len(author_post_json_res)
    for authorpost in author_post_json_res:
        icore_dict = {}
        post_url = settings.ICORE_API_URL+'/posts/'+authorpost["ID"]
        headers = {'Content-Type': 'application/json'}
        post_req = requests.get(post_url, headers=headers_all)
        post_res = post_req.content.encode('UTF-8')
        post_json_res = json.loads(post_res)
        icore_dict["ID"] = post_json_res["ID"]
        icore_dict["title"] = post_json_res["title"]
        icore_dict["link"] = post_json_res["link"]
        authorpost_list.append(icore_dict)

    comment_post_url = settings.ICORE_API_URL+'/comments/'+user_profile_obj.email
    headers = {'Content-Type': 'application/json'}
    comment_post_req = requests.get(comment_post_url, headers=headers_all)
    comment_post_res = comment_post_req.content.encode('UTF-8')
    comment_post_json_res = json.loads(comment_post_res)
    for commentpost in comment_post_json_res:
        icore_dict = {}
        icore_dict["comment"] = commentpost["comment_content"]
        post_url = settings.ICORE_API_URL+'/posts/'+commentpost["comment_post_ID"]
        headers = {'Content-Type': 'application/json'}
        post_req = requests.get(post_url, headers=headers_all)
        post_res = post_req.content.encode('UTF-8')
        post_json_res = json.loads(post_res)
        icore_dict["ID"] = post_json_res["ID"]
        icore_dict["link"] = post_json_res["link"]
        commentpost_list.append(icore_dict)



    data = {
        'first_name': user_profile_obj.first_name,
        'middle_name': user_profile_obj.middle_name,
        'last_name': user_profile_obj.last_name,
        'suffix': user_profile_obj.suffix,
        'mother_name': user_profile_obj.mother_name,
        'father_name': user_profile_obj.father_name,
        'birthday': user_profile_obj.birthdate,
        'secondary_email': user_profile_obj.secondary_email,
        'gender': user_profile_obj.gender,
        'address': user_profile_obj.address,
        'state': user_profile_obj.state,
        'language_known': user_profile_obj.language_known,
        'mother_tongue': user_profile_obj.mother_tongue,
        'highest_qualification': user_profile_obj.qualification,
        'company_name': user_profile_obj.company_name,
        'designation': user_profile_obj.designation,
        'annual_income': user_profile_obj.annual_income,
        'company_website': user_profile_obj.company_website,
        'company_address1': user_profile_obj.company_address1,
        'company_address2': user_profile_obj.company_address2,
        'company_landmark': user_profile_obj.company_landmark,
        'company_state': user_profile_obj.company_state,
        'company_locality': user_profile_obj.company_locality,
        'company_country': user_profile_obj.company_country,
        'company_city': user_profile_obj.company_city,
        'company_pincode': user_profile_obj.company_pincode,
        'nationality': user_profile_obj.nationality,
        'marital_status': user_profile_obj.marital_status,
        'facebook_media': user_profile_obj.facebook_media,
        'linkedin_media': user_profile_obj.linkedin_media,
        'google_media': user_profile_obj.google_media,
        'twitter_media': user_profile_obj.twitter_media,
        'languages_known_read_write': user_profile_obj.languages_known_read_write,
        'landmark': user_profile_obj.landmark,
        'street_name': user_profile_obj.street_name,
        'pincode': user_profile_obj.pincode,
        'answer': question,
        'Advisory_ins': advisory_ins,
        'instruments': instruments,
        'practice_details': practice_details,
        'locality': user_profile_obj.locality,
        'my_belief': user_profile_obj.my_belief,
        'my_promise': advisor_obj.my_promise,
        'total_no_invites_to_rate': total_no_invites_to_rate,
        'total_no_rated': total_no_rated,
        'final_peer_avg_rating': final_peer_avg_rating,
        'total_no_invites_to_rank': total_ranked_invites,
        'total_member_ranks': total_member_ranks,
        'final_consumer_avg_ranking': final_consumer_avg_ranking,
        'SEBI_registration_no': advisor_obj.sebi_number,
        'SEBI_expire_date': advisor_obj.sebi_expiry_date,
        'SEBI_valid_from': advisor_obj.sebi_start_date,
        'AMFI_registration_no': advisor_obj.amfi_number,
        'AMFI_expire_date': advisor_obj.amfi_expiry_date,
        'AMFI_valid_from': advisor_obj.amfi_start_date,
        'IRDA_registration_no': advisor_obj.irda_number,
        'IRDA_expire_date': advisor_obj.irda_expiry_date,
        'IRDA_valid_from': advisor_obj.irda_start_date,
        'other_registration_no': advisor_obj.other_registered_number,
        'other_registration_state': advisor_obj.other_registered_organisation,
        'other_expiry_date': advisor_obj.other_expiry_date,
        'confirmed': advisor_obj.is_confirmed_advisor,
        'RERA_details': rera_details,
        'DSA_details':dsa_details,
        'education_qualification': advisor_obj.credibility_declaration_qualification,
        'profile_referral_code': user_profile_obj.referral_code,
        'wordpress_user_id': advisor_obj.wordpress_user_id,
        'total_reffered_advisor_count': total_reffered_advisor_count,
        'referred_registered_advisor_count': referred_registered_advisor_count,
        'total_clients_served': advisor_obj.total_clients_served,
        'total_advisors_connected': advisor_obj.total_advisors_connected,
        'sales_accomplishments': advisor_obj.my_sales,
        'facebook_contact': user_profile_obj.facebook_media,
        'google_contact': user_profile_obj.google_media,
        'linkedin_contact': user_profile_obj.linkedin_media,
        'twitter_contact': user_profile_obj.twitter_media,
        'email_id': user_profile_obj.email,
        'mobile_number': user_profile_obj.mobile,
        'locality': user_profile_obj.locality,
        'city': user_profile_obj.city,
        'languages_known_speak': user_profile_obj.language_known,
        'languages_known_read_write': user_profile_obj.languages_known_read_write,
        'product_experience': product_experience,
        'total_clients_added': total_members,
        'total_clients_registered': registered_member,
        'total_clients_unregistered': un_registered_members,
        'picture_url': profile_picture,
        'crisil_application_status': advisor_obj.crisil_application_status,
        'crisil_promo_code': promo_code,
        'crisil_amount': crisil_final,
        # 'stream_details' : get_all_stream_course_json,
        'total_icore_posts': total_icore_posts,
        'icore_posts': icore_posts_list,
        'my_posts': authorpost_list,
        'my_posts_total': total_author_post,
        'advisor_total_points': user_profile_obj.total_points,
        'client_feedback': feedbacks,
        'qualifications': user_profile_obj.qualification,
        'certified_advisor': advisor_obj.is_certified_advisor,
        'crisil_verified': advisor_obj.is_crisil_verified,
        'my_icore_comments': commentpost_list,
        'crisil_register_no': crisil_reg_no,
        'crisil_expiry_date': crisil_expiry_date,
        'crisil_pay_amount': crisil_amount,
        'crisil_years_selected': no_of_years_selected,
        'college': user_profile_obj.college_name,
        'year_passout': user_profile_obj.year_passout,
        'Additional_qualification_list': additional_qualification_list,
        'education_category': user_profile_obj.education_category,
        'country': user_profile_obj.country,
        'pan_no': pancard_detail,
        'primary_communication': user_profile_obj.primary_communication,
        'communication_email_id': user_profile_obj.communication_email_id,
        'educational_details':educational_details,
        'certification_details':certification_details
    }
    
    logger.info(
        logme('returned advisor profile details(my track) = %s using api'%(str(user_obj)),request)
    )
    return JSONResponse(data, status=200)


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def send_mail_admin_subject(request):
    '''
        Sending Email to user from contact@reiaglobal.com to user Email
        [template_name = 'REIA-01-2', email_to = User Email,
         user_email = Advisor Email(This Email come to Reply to Field),
         subject = Subject of Email, context = Content of Email.
        ]
    '''
    context_dict = {
        'Title': request.POST['title'],
        'Name' : request.POST['name'],
        'body_content' : request.POST['mail_body'],
        'user_first_name' : request.user.first_name
    }
    send_mandrill_email_admin_subject(request.POST['template_name'], [request.POST['email_to']],
        request.user.username, request.POST['subject'], context_dict)
    logger.info(
        logme('sent email to advisor %s' % (str(request.user)), request)
    )
    return JSONResponse("success", status=200)


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_dashboard_details(request):
    members = Member.objects.filter(user_profile__created_by=request.user)
    total_members = members.count()
    registered_member = 0
    un_registered_members = 0
    for member in members:
        if member.is_register_member:
            registered_member += 1
        else:
            un_registered_members += 1
    reffered_users = UserProfile.objects.filter(referred_by=request.user)
    loop_users = reffered_users.count()
    logger.info(
        logme('sent advisors and members details', request)
    )
    return JSONResponse('success', status=200)


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_advisorloop_details(request):
    response = dashboard.views.view_loop(request)
    return JSONResponse({'data': response}, status=200)


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def save_refer_advisor(request):
    response = dashboard.views.save_refer_advisor(request)
    return JSONResponse({'data': response}, status=200)


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def check_refer_advisor_email(request):
    response = dashboard.views.valid_email(request)
    return JSONResponse({'data': response}, status=200)


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_raterank_details(request):
    response = dashboard.views.view_ranking_or_rating(request)
    return JSONResponse({'data': response}, status=200)


@api_view(['GET'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_peerlist_torate(request):
    advisor_torate_list = []
    for advisorlist in AdvisorRating.objects.filter(existing_user_profile=request.user.profile,activation_key__isnull=False):
            advisor_dict = {}
            advisor_dict['name'] = advisorlist.advisor.user_profile.first_name
            advisor_dict['email'] = advisorlist.advisor.user_profile.email
            advisor_dict['activation_key'] = advisorlist.activation_key
            advisor_torate_list.append(advisor_dict)
    logger.info(
        logme('get all peer list to rate', request)
    )
    return JSONResponse(advisor_torate_list, status=200)


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def rate_advisor(request):
    response = dashboard.views.rate_advisor(request)
    return JSONResponse({'data': response}, status=200)


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def invite_peerto_rate(request):
    response = dashboard.views.invite_advisor_to_rate(request)
    return JSONResponse({'data': response}, status=200)


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def save_sale_accomplishment(request):
    advisor = Advisor.objects.get(user_profile=request.user.profile)
    if request.POST['sale_content']:
        advisor.my_sales = request.POST['sale_content']
        advisor.save()
        logger.info(
            logme('sale accomplishments details saved successfully', request)
        )
        return HttpResponse("success")
    else:
        logger.info(
            logme('invalid content, could not save sale accomplishments details', request)
        )
        return HttpResponse("Not valid content")
    return HttpResponse("success")


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def check_crisil_promocode(request):
    code = request.POST['code']
    valid_promocode = PromoCodes.objects.filter(user_profile=request.user.profile, 
    promo_code=code)
    if valid_promocode:
        discount_amount = \
            float(constants.CRISIL_CERTIFICATE_VALUE/100)*(100-constants.CRISIL_CERTIFICATE_DISCOUNT)
        tax_amount = float(discount_amount/100)*(constants.TAX_PERCENTAGE_CRISIL)
        final_amount = discount_amount + tax_amount
        status = 'valid'
    else:
        tax_amount = float(constants.CRISIL_CERTIFICATE_VALUE/100)*(constants.TAX_PERCENTAGE_CRISIL)
        final_amount = constants.CRISIL_CERTIFICATE_VALUE + tax_amount
        discount_amount = 0
        status = 'invalid'
    data ={
        'amount' : final_amount,
        'promocode_status' : status,
        'discount_amount' : discount_amount,
        'tax' : tax_amount
    }
    logger.info(
        logme('validation - checked CRISIL promocode status=%s'%(str(status)), request)
    )
    return JSONResponse(data,status=200)

# ===========================================================
# Applying CRISIL
# ===========================================================
@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def appling_crisil(request):
    '''
        Description: Advisor is applying for CRISIL Certification.
    '''
    if request.method == 'POST':
        promocode = request.POST['promocode']
        crisil_selected_years = request.POST['crisil_selected_years']
        crisil_offered_years = 0
        discount_percentage = 0
        if int(crisil_selected_years) == constants.CERTIFICATE_YEARS:
            crisil_offered_years = constants.CRISIL_OFFERED_YEARS
        # checking promocode is valid or not
        valid_promocode = ''
        if request.POST['promocode_status'] == 'applied':
            valid_promocode = PromoCodes.objects.filter(user_profile = request.user.profile,promo_code = promocode)
        if valid_promocode:
            discount_percentage = constants.CRISIL_CERTIFICATE_DISCOUNT
            final_amount = calculate_final_amount_with_discount_and_tax_amount(\
                    constants.CRISIL_CERTIFICATE_VALUE,
                    crisil_selected_years,
                    discount_percentage,
                    constants.TAX_PERCENTAGE_CRISIL
                )
        else:
            final_amount = calculate_final_amount_with_discount_and_tax_amount(\
                    constants.CRISIL_CERTIFICATE_VALUE,
                    crisil_selected_years,
                    discount_percentage,
                    constants.TAX_PERCENTAGE_CRISIL
                )
        advisor = Advisor.objects.filter(user_profile = request.user.profile)
        if advisor:
            advisor = advisor.first()
        '''
        if the user has any previous transaction, then it is renewal
        for renewal update the object
        '''
        transaction_instance, status = TransactionsDetails.objects.get_or_create(
                                                user_profile = request.user.profile)
        new_invoice_no = invoice_gen(advisor, transaction_instance)
        if valid_promocode:
            transaction_instance.promo_code = promocode
        transaction_instance.discounted_amount = final_amount
        transaction_instance.invoice_number = new_invoice_no
        transaction_instance.amount = constants.CRISIL_CERTIFICATE_VALUE*int(crisil_selected_years)
        transaction_instance.transaction_type = constants.TR_TYPE
        transaction_instance.serial_no = int(new_invoice_no.split('-')[-1])
        description = {
            "transaction_type":"Bank Details",
            "remark":"",
            "no_of_years_selected":crisil_selected_years,
            "offered_years":crisil_offered_years
        }
        description = json.dumps(description)
        transaction_instance.description = description
        transaction_instance.save()
        # changing the status in crisil application status in advisor table
        advisor.crisil_application_status = constants.CRISIL_APPLIED
        advisor.save()
        # SEND EMAIL ALERT to Advisor================================
        communication_email = request.user.profile.email
        if request.user.profile.communication_email_id == 'secondary':
            communication_email = request.user.profile.secondary_email
        first_name = request.user.profile.first_name
        last_name = request.user.profile.last_name
        name =  first_name + ' '+ last_name
        our_account_name = constants.CRISIL_ACCOUNT_NAME
        our_account_number = constants.CRISIL_ACCOUNT_NUMBER
        our_bank_name = constants.CRISIL_BANK_NAME
        our_branch_name = constants.CRISIL_BANK_BRANCH
        our_branch_IFSC_code = constants.CRISIL_BANK_IFSC_CODE
        url_one = constants.CRISIL_URL_ONE
        amount_in_words = num2words(final_amount, lang='en_IN')
        context_dict = {
            'username': name,
            'our_account_name': our_account_name,
            'our_account_number': our_account_number,
            'our_bank_name': our_bank_name,
            'our_branch_name': our_branch_name,
            'our_branch_IFSC_code': our_branch_IFSC_code,
            'url': url_one,
            'final_amount':final_amount,
            'final_amount_in_words': amount_in_words
        }
        send_mandrill_email('REIA_17', [communication_email], context=context_dict)

        # SEND EMAIL ALERT TO ADMIN ===============================
        send_mandrill_email_admin('reaf-contact-admin', [settings.REIA_ADMIN_EMAIL], communication_email, context={})

        # SEND SMS ALERT ==========================================
        if request.user.profile.mobile:
            mobile_number=request.user.profile.mobile
            sms_status = get_sms_status(request.user.profile.status)
            if sms_status == True:
                message = 'Dear '+request.user.profile.first_name+' ('+request.user.profile.registration_id+'),Thank you for expressing interest to become a CRISIL verified Advisor. To proceed, upload the payment details.'
                sms_response = send_sms_alert(mobile_number=mobile_number, message_template=message)
        logger.info(
            logme('advisor applied for CRISIL certification for %s years, mailed sent to reia admin and advisor'%(str(crisil_selected_years)), request)
        )
        return Response(data = {'result': 'success'}, status=200)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def crisil_submit_form(request):
    tr_instance, tr_status = TransactionsDetails.objects.get_or_create(user_profile=request.user.profile)
    description = tr_instance.description
    discounted_amount = tr_instance.discounted_amount
    documents_new_upload, status = UploadDocuments.objects.get_or_create(\
        user_profile=request.user.profile, registration_number=request.POST['cheque_dd_no'])
    documents_new_upload.documents = request.FILES['scaned_doc']
    documents_new_upload.documents_type = "bank_details"
    documents_new_upload.save()
    tr_instance.bank_name = request.POST['bankname']
    tr_instance.cheque_dd_no = request.POST['cheque_dd_no']
    tr_instance.cheque_dd_date = request.POST['cheque_date']
    tr_instance.user_profile = request.user.profile
    tr_instance.discounted_amount = discounted_amount
    tr_instance.upload_cheque_dd_id = documents_new_upload
    tr_instance.status = None
    tr_instance.description = description
    tr_instance.save()
    advisor = Advisor.objects.filter(user_profile = request.user.profile)
    if advisor:
        advisor = advisor.first()
        if not advisor.crisil_application_status == constants.CRISIL_RENEWAL_PAYMENT_RE_SUBMIT:
            advisor.crisil_application_status = constants.CRISIL_PAYMENT_SUBMITTED
        else:
            advisor.crisil_application_status = constants.CRISIL_RENEWAL_PAYMENT_SUBMITTED
    advisor.save()

    # SEND EMAIL ALERT to Advisor ================================
    communication_email = request.user.profile.email
    if request.user.profile.communication_email_id == 'secondary':
        communication_email = request.user.profile.secondary_email
    first_name = request.user.profile.first_name
    last_name = request.user.profile.last_name
    advisor_name =  first_name + ' '+ last_name
    context_dict = {
        'advisor_name': advisor_name
    }

    logger.info(
        logme('submitted CRISIL payment details', request)
    )
    return Response(data = {'result': 'success'}, status=200)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def crisil_renew_submit(request):
    '''
    Description: Submitting the payment form for renewal payment
    '''
    bank_name=request.POST['bank_name']
    reference_number=request.POST['reference_number']
    payment_date=request.POST['payment_date']
    amount=request.POST['amount']
    years_selected=request.POST['years_selected']
    advisor_status = request.user.profile.advisor.crisil_application_status
    documents_new_upload, status = UploadDocuments.objects.get_or_create(\
        user_profile=request.user.profile, registration_number=request.POST['reference_number'])
    documents_new_upload.documents=request.FILES['renewal_reference_doc']  #reference_number
    documents_new_upload.documents_type = "bank_details"
    documents_new_upload.save()
    tr_instance  = TransactionsDetails.objects.get(user_profile=request.user.profile)
    if advisor_status =='crisil_certificate_expired':
        description = json.loads(tr_instance.description)
        description_json = {
            "remark": "",
            "offered_years": 0,
            "no_of_years_selected": constants.CERTIFICATE_RENEWAL_YEAR,
            "transaction_type": "bank_details"}
        description = json.dumps(description_json)
        tr_instance.description = description
        tr_instance.amount = constants.CRISIL_CERTIFICATE_VALUE
        crisil_application_status=constants.CRISIL_PAYMENT_SUBMITTED
    if advisor_status == constants.CRISIL_EXPIRED_BY_USER :
        tr_instance.amount = constants.CRISIL_CERTIFICATE_RENEWAL_VALUE
        crisil_application_status=constants.CRISIL_RENEWAL_PAYMENT_SUBMITTED

    tr_instance.user_profile = request.user.profile
    tr_instance.invoice_number = tr_instance.invoice_number
    tr_instance.bank_name = bank_name
    tr_instance.cheque_dd_no = reference_number
    tr_instance.cheque_dd_date = payment_date
    tr_instance.discounted_amount = amount
    tr_instance.serial_no = int(tr_instance.invoice_number.split('-')[-1])
    tr_instance.status = None
    tr_instance.save()
    advisor = Advisor.objects.filter(user_profile = request.user.profile)
    if advisor:
        advisor = advisor.first()
    advisor.crisil_application_status = crisil_application_status
    advisor.save()

    # SEND EMAIL ALERT to Advisor ================================
    communication_email = request.user.profile.email
    if request.user.profile.communication_email_id == 'secondary':
        communication_email = request.user.profile.secondary_email
    first_name = request.user.profile.first_name
    last_name = request.user.profile.last_name
    advisor_name =  first_name + ' '+ last_name
    context_dict = {
        'advisor_name': advisor_name
    }
    logger.info(
        logme('renewed CRISIL payment details', request)
    )
    return Response(data = {'result': 'success'}, status=200)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def disown_member(request):
    member_email = request.POST['member_email']
    member = User.objects.get(email=member_email)
    user_profile = UserProfile.objects.get(user=member)
    user_profile.created_by = member
    user_profile.save()
    logger.info(
        logme('disowned member from advisors loop', request)
    )
    return JSONResponse("success",status=200)

@api_view(['POST'])
@permission_classes((AllowAny,))
def forgot_password_reset(request):
    try:
        received = request.POST['resend_email']
        user = User.objects.get(username=received)
        user.is_staff=1
        user.save()
    except:
        logger.info(
            logme('email id %s does not exist for forgot password request'%(str(received)), request)
        )
        return JSONResponse("User object does not exists",status=500)
    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
    activation_key = hashlib.sha1(salt+user.email).hexdigest()
    key_expires = datetime.today() + timedelta(2)
    if user.profile.advisor.is_register_advisor or user.profile.source_media == constants.SIGNUP_WITH_EMAIL:
        try:
            verification = EmailVerification.objects.get(user_profile=user.profile)
            verification.activation_key=activation_key
            verification.key_expires=key_expires
            verification.save()
            logger.info(
                logme('forgot password activation key created', request)
            )
        except ObjectDoesNotExist:
            verification = EmailVerification(user_profile=user.profile, activation_key=activation_key, key_expires=key_expires)
            verification.save()
            logger.info(
                logme('forgot password activation key created', request)
            )
        try:#----------forgot password mail----------
            communication_email = user.profile.email
            if user.profile.communication_email_id == 'secondary':
                communication_email = user.profile.secondary_email
            send_mandrill_email('ABOTMI_26', [communication_email], context={'Name': user.profile.first_name, 'Website': settings.DEFAULT_HOST, 'Ack': activation_key})
            #----------------------------------------------
            logger.info(
                logme('forgot password activation link email sent', request)
            )
            return JSONResponse('Activation Link Mail sent',status=200)
        except:
            logger.error(
                logme('failed to send email with forgot password activation link', request)
            )
            return JSONResponse("Mail failure",status=500)
    else:
        logger.info(
            logme('email id %s does not exist for forgot password request'%(str(received)), request)
        )
        return JSONResponse("You are not a Registered User. Use Sign-up and Register. Sign-up Now",status=500)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def contact_us_reia(request):
    context = RequestContext(request)
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
        'message1': content_msg
    }
    try:
        send_mandrill_email('ABOTMI_27', [email_id], context=context_dict)
        send_mandrill_email_admin('reaf-contact-admin', [constants.REIA_ENQUIRY_ADMIN_EMAIL], request.POST['email'], context_dict)
        logger.info(
            logme('email sent to upwrdz admin for enquiry and confirmation mail to advisor', request)
        )
        return HttpResponse('success')
    except:
        logger.info(
            logme('enquiry email send failed(contact us upwrdz)', request)
        )
        return HttpResponse('Access forbidden')


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_icore_specificposts(request):
    icorepostresult = []
    token_obj_rating = {}
    postid = request.POST['id']
    USERNAME = settings.ICORE_ADMIN
    PASSWORD = settings.ICORE_ADMIN_PWD
    url      = settings.ICORE_API_URL+'/posts/'+postid
    headers  = {'Content-Type': 'application/json'}
    req      = requests.get(url, auth=(USERNAME, PASSWORD), headers=headers)
    json_res = req.content.encode('UTF-8')
    token_obj = json.loads(json_res)
    #----------------------------------
    # Display Comments specific posts
    #-----------------------------------
    url_comment      = settings.ICORE_API_URL+'/posts/'+postid+'/comments/'
    headers_comment  = {'Content-Type': 'application/json'}
    req_comment      = requests.get(url_comment, auth=(USERNAME, PASSWORD), headers=headers_comment,verify=SSL_VERIFY)
    json_res_comment = req_comment.content.encode('UTF-8')
    token_obj_comment = json.loads(json_res_comment)
    #------------------------------------
    # Dispaly Ratings for specific posts
    #------------------------------------
    url_rating      = settings.ICORE_API_URL+'/posts/'+postid+'/rating/'
    headers_rating  = {'Content-Type': 'application/json'}
    req_rating      = requests.get(url_rating, auth=(USERNAME, PASSWORD), headers=headers_rating)
    json_res_rating = req_rating.content.encode('UTF-8')
    token_obj_rating = json.loads(json_res_rating)

    categories=[]

    for i in token_obj['terms']['category']:
        categories.append(i['name'])

    icorepostresult = {
        'avatar' : token_obj['author']['avatar'],
        'username' : token_obj['author']['name'],
        'title' : token_obj['title'],
        'date' : token_obj['date'],
        'icoreimage' : token_obj['featured_image'],
        'category' : categories,
        'comments' : token_obj_comment,
        'rating' : token_obj_rating,
        'link':token_obj['link'],
        'content':token_obj['content']
    }
    logger.info(
        logme('returned icoreid = %s blog post'%(str(postid)), request)
    )
    return JSONResponse(icorepostresult,status=200)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def rate_icore_post(request):
    post_id         = request.POST['post_id']
    user            = request.user.id
    advisor_details = Advisor.objects.get(user_profile = request.user.profile)
    wordpress_user  = advisor_details.wordpress_user_id
    rating_sum      = request.POST['star_sum']
    rating_latest_updated_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    USERNAME = settings.ICORE_ADMIN
    PASSWORD = settings.ICORE_ADMIN_PWD
    url      = settings.ICORE_API_URL+'/posts/'+post_id+'/rating/'
    headers  = {'Content-Type': 'application/json'}
    rating_data = {}
    rating_data['data'] = [
            {"id" : post_id, "latest" : rating_latest_updated_time },
            [
                {"meta_key":"stars-rating_sum","meta_value":rating_sum},
                {"meta_key":"stars-rating_max","meta_value":"5"},
                {"meta_key":"stars-rating_votes","meta_value":"1"},
                {"meta_key":"stars-rating_rating","meta_value":rating_sum},
                {"meta_key":"stars-rating_distribution","meta_value":""},
                {"meta_key":"stars-rating_latest","meta_value":rating_latest_updated_time}
            ],
            {"user_id":wordpress_user, "logged":rating_latest_updated_time }, {"meta_value":rating_sum}
        ]
    rating_json_data = json.dumps(rating_data)
    req = requests.post(url, auth=(USERNAME, PASSWORD), headers=headers, data=rating_json_data, verify=SSL_VERIFY)
    logger.info(
        logme('rated icore post id=%s'%(str(post_id)), request)
    )
    #get the average icore rating
    req_rating      = requests.get(url, auth=(USERNAME, PASSWORD), headers=headers)
    json_res_rating = req_rating.content.encode('UTF-8')
    token_obj_rating = json.loads(json_res_rating)
    return JSONResponse({"data":token_obj_rating},status=200)

@api_view(['GET'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def icore_search_posts_by_author(request):
    context = RequestContext(request)
    if request.method == 'GET':
        USERNAME = settings.ICORE_ADMIN
        PASSWORD = settings.ICORE_ADMIN_PWD
        # ================Fetching recent for posts==================
        url_all      = settings.ICORE_API_URL+'/posts/'
        headers_all  = {'Content-Type': 'application/json'}
        req_all      = requests.get(url_all, auth=(USERNAME, PASSWORD), headers=headers_all)
        json_res_all = req_all.content.encode('UTF-8')
        token_obj_all = json.loads(json_res_all)
        # ================Search result posts==================
        author      = request.GET.get('author',False)
        if author:
            request.session['author'] = author
        else:
            author = request.session['author']
        url      = settings.ICORE_API_URL+'/posts/author/'+author
        headers  = {'Content-Type': 'application/json'}
        req      = requests.get(url, auth=(USERNAME, PASSWORD), headers=headers)
        json_res = req.content.encode('UTF-8')
        token_obj = json.loads(json_res)
        context_dict = { 'search': token_obj }
        post_data = []
        if token_obj:
            for post_author in token_obj:
                post_url = settings.ICORE_API_URL+'/posts/'+post_author['ID']
                headers  = {'Content-Type': 'application/json'}
                post_req      = requests.get(post_url, auth=(USERNAME, PASSWORD), headers=headers)
                post_json_res = post_req.content.encode('UTF-8')
                post_data.append(json.loads(post_json_res))

def not_single_event():
    ''' if there are no webinar/ meetup events for the advisor send a msg of the same
    in the response '''
    not_events = []
    data = dict()
    data['msg'] = 'There are no events scheduled by your advisor(s)'
    not_events.append(data)
    return not_events

@api_view(['GET'])
@permission_classes((AllowAny,))
def get_advisor_events(request):
    '''get list of advisor id in the url and split with ',' to make an array'''
    ids = request.GET['advisor_id'].split(',')
    ''' response has to be a list contains dictionary put into that '''
    ''' get the advisor's name and make a dictionary '''
    if request.GET['event_type'].encode('utf8') == 'meetup':
        advisor_meetup_events = []
        ''' for each advisor id make the list of events and the advisor name'''
        for advisor_id in ids:
            ''' id in the url is in str format. we need to convert the same into
            integer to proceed'''
            i = int(float(advisor_id))
            meetup_events = MeetUpEvent.objects.filter(user_profile = i)
            if meetup_events:
                meetup_serializer = MeetupSerializer(meetup_events, many = True)
                name = UserProfile.objects.get(id = i)
                ''' form the advisor name dict'''
                advisor_name_dict = dict()
                advisor_name_dict['advisor_name'] = name.first_name + \
                ' ' + name.middle_name + ' ' + name.last_name
                ''' copy the meetup serializer into another variable and append the advisor
                name dictionary to the seraiized data '''
                meetup_serialized_data = meetup_serializer.data
                '''append the name dict to the serialized data'''
                meetup_serialized_data.append(advisor_name_dict)
                advisor_meetup_events.append(meetup_serialized_data)
        if advisor_meetup_events:
            logger.info(
                logme('returned meetup events for user', request)
            )
            return Response(advisor_meetup_events, status=status.HTTP_200_OK)
        else:
            # there are no meetup events for any of the advisors
            no_events = []
            no_events = not_single_event()
            logger.info(
                logme('no meetup events for this user', request)
            )
            return Response(no_events, status = status.HTTP_412_PRECONDITION_FAILED)
    elif request.GET['event_type'].encode('utf8') == 'webinar':
        advisor_webinar_events = []
        for advisor_id in ids:
            i = int(float(advisor_id))
            webinar_events = TrackWebinar.objects.filter(user_profile = i)
            if webinar_events:
                webinar_serializer = WebinarSerializer(webinar_events, many = True)
                name = UserProfile.objects.get(id = i)
                advisor_name_dict = dict()
                advisor_name_dict['advisor_name'] = name.first_name + \
                ' ' + name.middle_name + ' ' + name.last_name
                ''' copy the webinar serializer into another variable and append the advisor
                name dictionary to the seraiized data '''
                webinar_serialized_data = webinar_serializer.data
                webinar_serialized_data.append(advisor_name_dict)
                advisor_webinar_events.append(webinar_serialized_data)
        if advisor_webinar_events:
            logger.info(
                logme('returned all webinar events for user', request)
            )
            return Response(advisor_webinar_events, status=status.HTTP_200_OK)
        else:
            # there are no webinar events for any of the advisors
            no_events = []
            no_events = not_single_event()
            logger.info(
                logme('no webinar events for this user', request)
            )
            return Response(no_events, status = status.HTTP_412_PRECONDITION_FAILED)

@api_view(['POST'])
@permission_classes((AllowAny,))
def create_direct_signup_user(request):
    password = get_random_string(length=8)
    user_name  = request.POST.get('email', None)
    first_name  = request.POST.get('first_name', None)
    mobile  = request.POST.get('mobile', None)
    direct_signup = LoginCommonFunctions({'request':request})
    data = {
        'password' : password,
        'email' : user_name,
        'first_name' : first_name,
        'mobile' : mobile
    }
    is_created = direct_signup.createuser(
        object = data
    )
    status_code = is_created.get('status')
    user = User.objects.get(email=user_name)
    user_profile_obj = UserProfile.objects.get(user=user)
    if not user_profile_obj.registration_id:
        while(True):
            num =  uuid.uuid4().hex[:10]
            if not UserProfile.objects.filter(registration_id = num):
                user_profile_obj.registration_id = num
                user_profile_obj.save()
                break
            else:
                continue
    if status_code == 201:
        return Response(data={'result' : 'success'}, status=status.HTTP_201_CREATED)
    elif status_code == 200:
        return Response(data={'result' : 'Email already exists'}, status=202)
    else:
        return Response(data={}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes((AllowAny,))
def social_signup_login_details(request):
    exist_user=0
    member=0
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    user_name  = request.POST['email']
    email      = user_name
    first_name = request.POST['first_name']
    source     = request.POST['source']
    last_name  = request.POST['last_name']
    username = user_name
    
    try:
        gender = request.POST['gender'].upper()

    except:
        gender  = ""
    try:
        birth   = request.POST['birthday']
        date = datetime.strptime(birth, "%m/%d/%Y")
        birthday  = datetime.strftime(date, "%Y-%m-%d")
    except:
        birthday = ""
    logger.debug(gender)
    logger.debug("username "+user_name+" email:"+email)
    # check user exists or not
    user = None
    try:
        user = User.objects.get(email=user_name)
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        user_profile = UserProfile.objects.get(user = user)
        if not user_profile.is_member:
            if not user_profile.is_advisor:
                user_profile.source_media = source
                user_profile.facebook_media = user_name
                user_profile.save()
            #----checking exist user or not
            # 1 is Already existing user
            # 0 is new user
            #-----------------
            exist_user=1
        else:
            member=1
    
    except ObjectDoesNotExist:
            user = None
            # Create User and redirect to next
            user_password = get_random_string(length=8)
            user = User.objects.create_user(username=user_name,email=email,password=user_password)
            user.first_name = first_name
            user.last_name  = last_name
            user.is_active = True
            user.is_staff = True
            # Creating BackEnd model for user
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            user.save()
            #----------welcome mail----------
            # send_mandrill_email('ABOTMI_01', [email], context={'Name': first_name})
            #----------------------------------
            # Creating User Profile
            user_profile = UserProfile.objects.get(user=user)
            user_profile.first_name = user.first_name
            user_profile.last_name  = user.last_name
            user_profile.email      = user.email
            user_profile.gender     = gender
            user_profile.source_media = source
            user_profile.is_advisor = True
            if request.POST.get('ref_link',None):
                referrer_obj = UserProfile.objects.get(referral_code = request.POST['ref_link'])
                user_profile.referred_by = referrer_obj.user
                referral_points(referrer_obj, user_profile, constants.SIGNUP_POINTS)
            if birthday:
                user_profile.birthdate  = birthday
            if(source == 'FACEBOOK'):
                user_profile.facebook_media = user.email
            elif(source == 'LINKEDIN' ):
                user_profile.linkedin_media = user.email
            else:
                user_profile.google_media = user.email
            user_profile.communication_email_id = 'primary'
            if not user_profile.registration_id:
                while(True):
                    num =  uuid.uuid4().hex[:10]
                    if not UserProfile.objects.filter(registration_id = num):
                        user_profile.registration_id = num
                        user_profile.save()
                        break
                    else:
                        continue
            user_profile.save()
            # return JSONResponse(data = {'token' : token}, status = 200)
            #----checking exist user or not
            # 1 is Already existing user
            # 0 is new user
            #-----------------
            exist_user=0
        
    if user:
        if user.is_active and user.is_staff and not user.profile.is_member:
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            if request.POST["next_url"] is not "":
                if user.profile.is_company:
                    return JSONResponse(data ={'user' : 'companyuser'},status = 200)
                if exist_user == 1:
                    return JSONResponse(data = {'token' : token}, status = 200)
                else:
                     return JSONResponse(data = {'token' : token}, status = 200)
        elif user.profile.is_member:
            return JSONResponse(data ={'user ':'member_user'},status = 200)
        else:
            return JSONResponse(data ={'user':'deactivated'},status = 200)
    else:
         return JSONResponse(data = {'result' : 'Invalid'}, status = 200)

@api_view(['POST'])
@permission_classes((AllowAny,))
def check_email_exists_send(request):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    user_name  = request.POST['email']
    email      = user_name
    first_name = request.POST['first_name']
    source     = request.POST['source']
    last_name  = request.POST['last_name']
    next_url   = request.POST["next_url"]
    gender = request.POST['gender'].upper()
    username = user_name
    user_details = User.objects.filter(username=username).first()
    user_profile_details = UserProfile.objects.filter(user=user_details).first()
    try:
        if user_details and not user_details.profile.is_member:
            email_status = "verified"
            payload = jwt_payload_handler(user_details)
            token = jwt_encode_handler(payload)
            user_password = user_details.password
            return JSONResponse(data = {'token' : token,'email_verified_status': email_status,'first_name':first_name,'email':email,'password':user_password,'last_name':last_name,'source':source,'next_url':next_url,'gender':gender}, status = 200)
   
        else:
            response_data = send_signup_otp(request)
            email_status = "not verified"
            token = "null"
            user_password = "null"
            return JSONResponse(data = {'token' : token,'email_verified_status': email_status,'first_name':first_name,'email':email,'password':user_password,'last_name':last_name,'source':source,'next_url':next_url,'gender':gender}, status = 200)

        logger.info(
                logme('validation - email exists', request)
            )
    except Exception as e:
        logger.info(
                logme('Error: Checking Emails--%s' % (str(e)), request)
            )
        # return HttpResponse(status=500)
    if request.method == "GET":
        logger.info(
            logme('GET request - access forbidden for checking email', request)
        )
        return HttpResponse(status=405)

   





def prepare_request_for_aadhaar_bridge(user_profile, aadhaar_number, type):
    if type == local_settings.AADHAAR_ADVISOR_STR :
        random_no=random.randint(100000,999999)
        aadhaar_transaction = AadhaarTransactions.objects.create(
            user_profile_id = user_profile.id,
            email = user_profile.email,
            aadhaar_number = aadhaar_number,
            api_type = 'SEND_OTP'
        )
        request_id = str(random_no)+str(aadhaar_transaction.id)
        successUrl = local_settings.AADHAR_MOBILE_SUCESSS_URL
        failureUrl = local_settings.AADHAR_MOBILE_FAILURE_URL
    else:
        random_no=random.randint(100000,999999)
        aadhaar_transaction = AadhaarTransactions.objects.create(
            user_profile_id = user_profile.id,
            email = user_profile.email,
            aadhaar_number = aadhaar_number,
            api_type = 'MEM_OTP'
        )
        request_id = str(random_no)+str(aadhaar_transaction.id)
        successUrl = local_settings.AADHAAR_MOBILE_MEMBER_SUCCESS_URL
        failureUrl = local_settings.AADHAAR_MOBILE_MEMBER_FAILURE_URL

    saCode = local_settings.AADHAAR_SACODE
    salt = local_settings.AADHAAR_SALT
    Hash_Sequence = str(saCode)+'|'+str(aadhaar_number)+'|'+str(request_id)+'|'+str(salt)
    hash_code = hashlib.sha256(Hash_Sequence).hexdigest()
    data = {
        'saCode' : saCode,
        'requestId' : request_id,
        'hash' : hash_code,
        'aadhaarId' : aadhaar_number,
        'purpose' : 'To verify the Identity.',
        'modality' : 'otp',
        'channel': 'BOTH',
        'successUrl' : successUrl,
        'failureUrl' : failureUrl,
    }
    return data

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def create_aadhaar_form_data(request):
    '''
    Description: Navigating to Aadhaar server.
        --> creating transaction in AadhaarTransactions table
    '''
    aadhaar_number = request.POST.get('aadhaar_no',None)
    if aadhaar_number:
        user_profile = request.user.profile
        user_profile_obj = UserProfile.objects.filter(adhaar_card = aadhaar_number)
        if not user_profile_obj:
            data = prepare_request_for_aadhaar_bridge(user_profile, aadhaar_number, local_settings.AADHAAR_ADVISOR_STR)
            logger.info(
                logme('aadhaar:create aadhaar form data successful', request)
            )
            return JSONResponse(data,status=200)
        else:
            logger.info(
                logme('aadhaar:aadhaar number already exists in uplyf or upwrdz', request)
            )
            return JSONResponse({'data':'Aadhaar number is already exist'},status=200)
    logger.info(
        logme('aadhaar:aadhaar number not found', request)
    )
    return JSONResponse({'data':'Please send aadhar number'}, status =200)

def get_user_data_from_aadhar(uuid,reqid):
    saCode = local_settings.AADHAAR_SACODE
    uuid = uuid
    requestId = reqid
    uplyf_url = local_settings.UPLYF_URL
    source_media = ''
    if uuid and requestId:
        aadhaar_transaction_id = requestId[6:]
        salt = local_settings.AADHAAR_SALT
        # getting aadhaar transaction object for aadhaar number
        aadhaa_transaction = AadhaarTransactions.objects.get(id = aadhaar_transaction_id)
        # data for sending to aadhaar to get the user information
        Hash_Sequence = str(uuid)+'|'\
            +str(saCode)+'|'+str(aadhaa_transaction.aadhaar_number)+'|'+str(requestId)+'|'+str(salt)
        hash_code = hashlib.sha256(Hash_Sequence).hexdigest()
        final_req = dict()
        final_req['saCode'] = saCode
        final_req['uuid'] = uuid
        final_req['requestId'] = requestId
        final_req['aadhaarId'] = aadhaa_transaction.aadhaar_number
        final_req['hash'] = hash_code
        final_req = json.dumps(final_req)
        aadhar_response = requests.post(
            local_settings.AADHAAR_FETCH_KYC_URL,
            final_req
        )
        aadhaa_transaction.ekyc_details = str(aadhar_response.content)
        aadhaa_transaction.save()
        return aadhar_response, aadhaa_transaction
    else:
        return None

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def success(request):
    '''
    Description: Getting User information from aadhaar server.
        --> updating success or failure status in AadhaarTransactions table.
    '''
    uuid  = request.POST.get('uuid', None)
    reqid = request.POST.get('reqid',None)
    aadhar_response, aadhaa_transaction = get_user_data_from_aadhar(uuid,reqid)
    logger.info(
        logme('aadhaar:fetched data from aadhaar', request)
    )
    result = json.loads(aadhar_response.content)
    if result :
        user_information = result['success']
        status_code = None
        status_code = result['aadhaar-status-code']
        if user_information:
            reference_code = result['aadhaar-reference-code']
            user = request.user
            user_profile = user.profile
            kyc_photo = result['kyc']['photo']
            documents = kyc_photo
            missing_padding = len(documents) % 4
            if missing_padding != 0:
                documents += b'='* (4 - missing_padding)
            d = documents.encode('ascii','ignore')
            s=user_profile.id
            #d = d[22:]
            server_domains = ['dev.reiaglobal.com','test.reiaglobal.com','reiaglobal.com','localhost', 'test.upwrdz.com','dev.upwrdz.com','prod.upwrdz.com','upwrdz.com','www.upwrdz.com']
            if any(n in settings.DEFAULT_HOST for n in server_domains):
                '''
                ACTION: use to store file / profile picture in AWS S3 storage
                '''
                picture_path = "reia/"+str(user_profile.id)+"/ProfilePicture"+str(user_profile.registration_id)+".png"
                default_storage.exists(picture_path)
                file = default_storage.open(picture_path, 'w+')
                file.write(d.decode('base64'))
                file.close()
            else:
                picture_path = "uploads/reia/"+str(user_profile.id)+"/ProfilePicture"+str(user_profile.registration_id)+".png"
                fh = open(picture_path, "wb")
                fh.write(d.decode('base64'))
                fh.close()
            user_profile.picture =  picture_path
            upload_documents, created = UploadDocuments.objects.get_or_create(
                user_profile = user_profile,
                documents_type  = constants.PROFILE_PICTURE
            )
            upload_documents.registration_number = user_profile.registration_id
            upload_documents.documents = picture_path
            upload_documents.save()
            # is_mail_sent = registered_advisor_email(user_profile.user.id)
            if 'poa' in result['kyc']:
                address = ""
                kyc_poa = result['kyc']['poa']
                if 'house' in result['kyc']['poa']:
                    house = result['kyc']['poa']['house']
                    user_profile.door_no = house
                    address = address+" "+str(house)+","
                if 'lm' in result['kyc']['poa']:
                    lm = result['kyc']['poa']['lm']
                    user_profile.landmark = lm
                if 'street' in result['kyc']['poa']:
                    street = result['kyc']['poa']['street']
                    user_profile.street_name = street
                if 'po' in result['kyc']['poa']:
                    po = result['kyc']['poa']['po']
                    if str(po)+"," not in address:
                        address = address+" "+str(po)+","
                if 'vtc' in result['kyc']['poa']:
                    vtc = result['kyc']['poa']['vtc']
                    if str(vtc)+"," not in address:
                        address = address+" "+str(vtc)+","
                if 'dist' in result['kyc']['poa']:
                    dist = result['kyc']['poa']['dist']
                    if str(dist)+"," not in address:
                        address = address+" "+str(dist)+","
                if 'state' in result['kyc']['poa']:
                    state = result['kyc']['poa']['state']
                    user_profile.state = state
                if 'pc' in result['kyc']['poa']:
                    pc = result['kyc']['poa']['pc']
                    user_profile.pincode = pc
                    # Get city name from datacenter_indiapincode table using pincode
                    city_obj = India_Pincode.objects.filter(pin_code = pc).first()
                    if city_obj:
                        user_profile.city = city_obj.district_name
                        city_name = " "+str(user_profile.city)+","
                        if city_name in address:
                            address = address.replace(city_name,"")
                if 'co' in result['kyc']['poa']:
                    co = result['kyc']['poa']['co']
                    if "S/O" in co:
                        co = co.replace("S/O ", "")
                        co = co.replace("S/O: ", "")
                    if "D/O" in co:
                        co = co.replace("D/O ", "")
                        co = co.replace("D/O: ", "")
                    user_profile.father_name = co
                user_profile.address = address
            if 'poi' in result['kyc']:
                poi = result['kyc']['poi']
                if 'dob' in result['kyc']['poi']:
                    dob = result['kyc']['poi']['dob']
                    datetime_object = datetime.strptime(dob, '%d-%m-%Y')
                    dob = datetime_object
                    user_profile.birthdate = dob
                if 'gender' in result['kyc']['poi']:
                    gender = result['kyc']['poi']['gender']
                    user_profile.gender = gender
                if 'name' in result['kyc']['poi']:
                    name = result['kyc']['poi']['name']
                if 'phone' in result['kyc']['poi']:
                    user_profile.mobile = result['kyc']['poi']['phone']
            user_profile.resedential_status = 'indian'
            user_profile.nationality = constants.INDIAN_NATIONALITY
            user_profile.adhaar_card = result['aadhaar-id']
            source_media = user_profile.source_media
            advisor = user_profile.advisor
            logger.info(
                logme('aadhaar:aadhaar details stored in user profile', request)
            )
            user.save()
            user_profile.save()
            advisor.save()
        else:
            reference_code = None

        aadhaa_transaction.aadhaar_status_code = status_code
        aadhaa_transaction.success_status = user_information
        aadhaa_transaction.aadhaar_reference_code = reference_code
        aadhaa_transaction.save()  
    return JSONResponse({'data':source_media},status = 200)


# def send_aadhaar_error_to_email(context, request):
#     try:
#         send_mandrill_email(
#             local_settings.AADHAAR_FAILURE_EMAIL_TO_ADMIN,
#             [local_settings.AADHAAR_FAILURE_EMAIL_SEND_TO],
#             context = context
#         )
#     except Exception as e:
#         logger.info(
#             logme('aadhaar: aadhaar failure - semd mail unsuccessful exception {}'.format(e), request)
#         )
#         pass


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def failure(request):
    '''
    Description: If aadhaar transaction failes we are storing failed in success_status
    '''
    requestId = request.POST.get('reqid', None)
    user_profile_id = None
    user_email = None
    if requestId:
        aadhaar_transaction_id = requestId[6:]
        aadhaar_transaction = AadhaarTransactions.objects.get(id = aadhaar_transaction_id)
        aadhaar_transaction.success_status = False
        aadhaar_transaction.save()
        user_profile_id = aadhaar_transaction.user_profile_id
        user_email = aadhaar_transaction.email
        reia_home = settings.LOGIN_REDIRECT_URL

    error_code = request.GET.get('err', None)
    if error_code:
        if error_code in local_settings.AADHAAR_ERROR_CODE:
            context = {
                'error_code':error_code,
                'error_code_meaning':local_settings.AADHAAR_ERROR_CODE_MEANING[error_code],
                'user_profile_id':user_profile_id,
                'user_email':user_email
            }
            send_aadhaar_error_to_email(context,request)
    logger.info(
        logme('aadhaar : error happened during verifying ekyc for request id {}, error code is {}'.format(requestId, error_code), request)
    )
    return JSONResponse({'data':'Aadhar Details Storing unsuccessful'},status = 200)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def check_aadhaar_present(request):
    '''
    This api is to check weather aadhaar number is present in our system or not
    '''
    aadhaar_number = request.POST.get('aadhaar_no', None)
    if aadhaar_number:
        url = settings.UPLYF_SERVER+"/api/aadhar/check_aadhaar_present"
        data = {"aadhaar_no" : aadhaar_number}
        response = requests.post(url,data = data, verify=constants.SSL_VERIFY)
        status_code = response.status_code
        json_res_data = json.loads(response.text)
        if status_code == 200:
            user_profile = user_profile = request.user.profile
            data = prepare_request_for_aadhaar_bridge(user_profile, aadhaar_number, local_settings.AADHAAR_MEMBER_STR)
            logger.info(
                logme('aadhaar:checked aadhaar number not present in UPLYF', request)
            )
            return JSONResponse(data, status = 200)
        logger.info(
            logme('aadhaar:checked aadhaar number is present in UPLYF', request)
        )
        return JSONResponse(json_res_data, status = status_code)
    else:
        logger.info(
            logme('aadhaar:aadhaar number not found', request)
        )
        return JSONResponse({"data":"Aadhaar number not provided"}, status=401)


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def member_success(request):
    '''
    Description: If aadhaar transaction failes we are storing failed in success_status
    '''
    uuid  = request.POST.get('uuid', None)
    reqid = request.POST.get('reqid',None)
    aadhar_response, aadhaa_transaction = get_user_data_from_aadhar(uuid,reqid)
    logger.info(
        logme('aadhaar:fetched data from aadhaar in member success', request)
    )
    data = {}
    data['email_from_aadhaar'] = None
    data['is_kyc_success'] = None
    data['ekyc_verified_data'] = None
    data['is_ekyc_verified_data_present'] = None
    data['aadhaar_mobile'] = None
    data['aadhaar_transaction_id'] = aadhaa_transaction.id
    result = json.loads(aadhar_response.content)
    user_information = result['success']
    status_code = None
    status_code = result['aadhaar-status-code']
    if user_information:
        data['is_ekyc_verified_data_present'] = True
        data['is_kyc_success'] = True
        if 'poi' in result['kyc']:
            poi = result['kyc']['poi']
            if 'email' in poi:
                email = result['kyc']['poi']['email']
                if email:
                    data['email_from_aadhaar'] = email
            if "phone" in poi:
                phone = result['kyc']['poi']['phone']
                data['aadhaar_mobile'] = phone
            logger.info(
                logme('aadhaar: fetched data and stored in session in member success', request)
            )
            return JSONResponse({'data':data},status=200)
    else:
        logger.info(
            logme('aadhaar:ekyc success status failed', request)
        )
        data['is_kyc_success'] = False
    return JSONResponse({'data':data},status=200)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def member_failed(request):
    '''
    Description: If aadhaar transaction failes we are storing failed in success_status
    '''
    data = {}
    data['is_kyc_success'] = None
    data['is_adhaar_no_invalid'] = None
    error_code = request.GET.get('err', None)
    if error_code:
        if error_code in local_settings.AADHAAR_ERROR_CODE:
            user_profile_id = None
            user_email = None
            context = {
                'error_code':error_code,
                'error_code_meaning':local_settings.AADHAAR_ERROR_CODE_MEANING[error_code],
                'user_profile_id':user_profile_id,
                'user_email':user_email
            }
            send_aadhaar_error_to_email(context, request)

        if error_code == "AB-210":
            data['is_adhaar_no_invalid'] = True
        else:
            data['is_kyc_success'] = False
    logger.info(
        logme('aadhaar : error happened during verifying ekyc error code is {}'.format(error_code), request)
    )
    return JSONResponse({'data':data},status=200)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_smsalert_status(request):
    '''
    Description: Get advisor sms notification status
    '''
    sms_status = request.user.profile.advisor.sms_alert
    return JSONResponse({'data':sms_status},status=200)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def change_sms_status(request):
    '''
    Description: Toggle advisor sms notification status
    '''
    advisor = request.user.profile.advisor
    advisor.sms_alert = not advisor.sms_alert
    advisor.save()
    return JSONResponse({'data':advisor.sms_alert},status=200)

@api_view(['GET'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_icore_categories(request):
    USERNAME = settings.ICORE_ADMIN
    PASSWORD = settings.ICORE_ADMIN_PWD
    url      = settings.ICORE_API_URL+'/taxonomies/category/terms/'
    headers  = {'Content-Type': 'application/json'}
    req      = requests.get(url, auth=(USERNAME, PASSWORD), headers=headers, verify=SSL_VERIFY)
    json_res = req.content.encode('UTF-8')
    token_obj = json.loads(json_res)
    category = token_obj
    return JSONResponse({'data':category},status=200)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def icore_add_media(request):
    USERNAME = settings.ICORE_ADMIN
    PASSWORD = settings.ICORE_ADMIN_PWD
    wp = Client(settings.ICORE_XMLRPC, USERNAME, PASSWORD)
    filename = request.FILES['media']
    data = {
        'name' : filename.name,
        'type':  filename.content_type,
    }
    imgdata=None
    for chunk in filename.chunks():
        imgdata = xmlrpc_client.Binary(chunk)
    data['bits']=imgdata
    response = wp.call(media.UploadFile(data))
    attachment_id = response['attachment_id']
    attachment_url = response['url']
    context_dict = attachment_id+"::"+attachment_url
    logger.info(
        logme('added media = %s to icore'%(filename.name), request)
    )
    return JSONResponse({'data':context_dict},status=200)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def icore_add_post(request):
    advisor_details = Advisor.objects.get(user_profile = request.user.profile)
    wordpress_user  = advisor_details.wordpress_user_id
    # creating tag list
    list_tag = []
    if request.POST['add_tag']:
        str_tag = request.POST['add_tag']
        list_tag = str_tag.split(',')
    else:
        list_tag = []
    # creating category list
    list_category = []
    if request.POST['add_category']:
        str_category = request.POST['add_category']
        list_category = str_category.split(',')
    else:
        list_category = []
    USERNAME = settings.ICORE_ADMIN
    PASSWORD = settings.ICORE_ADMIN_PWD
    url      = settings.ICORE_API_URL+'/posts/'
    headers  = {'Content-Type': 'application/json'}
    wp = Client(settings.ICORE_XMLRPC, USERNAME, PASSWORD)
    post = WordPressPost()
    post.title = request.POST['title']
    post.content = request.POST['content_raw']
    post.post_status = 'publish'
    post.comment_status = 'open'
    post.user = wordpress_user
    post.terms_names = {'post_tag': list_tag,'category': list_category,}
    post.thumbnail = request.POST['featured_image']
    post.id = wp.call(posts.NewPost(post))
    logger.info(
        logme('submitted icore post id =%s successfully'%(str(post.id)), request)
    )
    return JSONResponse({'data':post.id},status=200)

#==========================================================
# Create comment for respective posted articles
#==========================================================
@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def icore_add_comment(request):
    USERNAME = settings.ICORE_ADMIN
    PASSWORD = settings.ICORE_ADMIN_PWD
    post_id = request.POST['post_id']
    url      = settings.ICORE_API_URL+'/posts/'+post_id+'/comment/'
    headers  = {'Content-Type': 'application/json'}
    comment_data = {}
    comment_data['post_id'] = post_id
    comment_data['comment_author_name'] = request.user.profile.first_name
    comment_data['comment_author_email'] = request.user.profile.email
    comment_data['comment_content'] = request.POST['comment']
    comment_data['user_id'] = request.user.profile.advisor.wordpress_user_id
    comment_json_data = json.dumps(comment_data)
    req = requests.post(url, auth=(USERNAME, PASSWORD), headers=headers, data=comment_json_data, verify=SSL_VERIFY)
    logger.info(
        logme('commented icore post id=%s'%(str(post_id)), request)
    )
    return JSONResponse({'data':req},status=200)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def upload_file(request):
    required_documents = 0
    uploaded_mandatory_documents = 0
    user_ob = request.user.profile
    advisor_obj = Advisor.objects.get(user_profile=user_ob)
    documents_type = request.POST['documents_type']
    if documents_type == "Profile Picture":
        profile_pic_document = request.POST['profile_pic']
        missing_padding = len(profile_pic_document) % 4
        if missing_padding != 0:
            profile_pic_document += b'='* (4 - missing_padding)
        d = profile_pic_document.encode('ascii','ignore')
        d = d[22:]
        if any(n in settings.DEFAULT_HOST for n in constants.SERVER_DOMAINS):
            '''
            ACTION: use to store file / profile picture in AWS S3 storage
            '''
            picture_path = "reia/"+str(user_ob.id)+"/"+request.user.profile.registration_id+"pic.png"
            default_storage.exists(picture_path)
            file = default_storage.open(picture_path, 'w')
            file.write(d.decode('base64'))
            file.close()
        else:
            picture_path = "uploads/reia/"+str(user_ob.id)+"/"+request.user.profile.registration_id+"pic.png"
            fh = open(picture_path, "wb")
            fh.write(d.decode('base64'))
            fh.close()
        user_ob.picture =  picture_path
    user_ob.save()
    chk_document_type = UploadDocuments.objects.filter(
        user_profile=user_ob).filter(
        documents_type=str(documents_type)
    )
    if chk_document_type:
        chk_document_type.delete()
    user_profile = UserProfile.objects.get(user=request.user)
    documents_new_upload = UploadDocuments.objects.create(
        user_profile=user_profile
    )
    if documents_type == "Profile Picture" or documents_type == "EIPV":
        documents_new_upload.documents = picture_path
        documents_new_upload.documents_type = documents_type
        documents_new_upload.save()
    else:
        documents_new_upload.documents = request.FILES['document']
        documents_new_upload.documents_type = documents_type
        documents_new_upload.save()
    response = JSONResponse(
        {
            'url': documents_new_upload.documents.url,
            'id': documents_new_upload.id,
            'required_documents': required_documents,
            'uploaded_mandatory_documents': uploaded_mandatory_documents
        }
    )
    logger.info(
        logme('%s document uploaded'% (documents_type), request)
    )
    return response


# ========================
# Get save Profile modal
# ========================
@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def save_profile(request):
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
        if not user_profile.mobile.replace(" ", "") == request.POST['mobile_number'].replace(" ", ""):
            advisor_details.crisil_application_status = constants.CRISIL_EXPIRED_BY_USER
            advisor_details.is_crisil_verified = False
    else:
        user_profile.mobile = request.POST['mobile_number']
    user_profile.locality = request.POST['locality']
    user_profile.city = request.POST['city']
    user_profile.language_known = request.POST['languages_known_speak']
    user_profile.languages_known_read_write = request.POST['languages_known_read_write']
    user_profile.my_belief = request.POST['my_belief']
    user_profile.qualification = request.POST['qualifications']
    user_profile.year_passout = request.POST['year_passout']
    user_profile.college_name = request.POST['college']
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
    if request.POST.get('sebi_registration_no',None):
        sebi_number = request.POST['sebi_registration_no']
    if request.POST.get('irda_registration_no',None):
        irda_number = request.POST['irda_registration_no']
    if request.POST.get('amfi_registration_no',None):
        amfi_number = request.POST['amfi_registration_no']
    if request.POST.get('other_organisation',None):
        other_organisation = request.POST['other_organisation']
    if request.POST.get('other_registration_no',None):
        other_registered_number = request.POST['other_registration_no']
    sebi_expiry_date = None
    amfi_expiry_date = None
    irda_expiry_date = None
    other_expiry_date = None
    if request.POST.get('sebi_expiry_date',None):
        sebi_expiry_date = datetime.datetime.strptime(request.POST['sebi_expiry_date'], '%d-%m-%Y').strftime('%Y-%m-%d')
    if request.POST.get('amfi_expiry_date',None):
        amfi_expiry_date = datetime.datetime.strptime(request.POST['amfi_expiry_date'], '%d-%m-%Y').strftime('%Y-%m-%d')
    if request.POST.get('irda_expiry_date',None):
        irda_expiry_date = datetime.datetime.strptime(request.POST['irda_expiry_date'], '%d-%m-%Y').strftime('%Y-%m-%d')
    if request.POST.get('other_expiry_date',None):
        other_expiry_date = datetime.datetime.strptime(request.POST['other_expiry_date'], '%d-%m-%Y').strftime('%Y-%m-%d')
    # Changing CRISIL certificate to expired when advisor try to change IRDA or SEBI Details after getting CRISIL Certificate
    if is_crisil_valid:
        if not old_sebi_number == sebi_number\
            or not old_irda_number == irda_number\
            or not old_amfi_number == amfi_number\
            or not old_other_registered_number == other_registered_number\
            or not old_other_registered_organisation == other_organisation:
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
    if request.POST.get('sebi_registration_no',None) \
        or request.POST.get('amfi_registration_no',None) \
        or request.POST.get('irda_registration_no',None) \
        or request.POST.get('other_organisation',None) \
        or request.POST.get('hidden_value',None) \
        or request.POST.get('dsa_hidden_input_field',None):
            advisor_details.is_registered_advisor = True
    advisor_details.my_promise = request.POST['my_promise']
    advisor_details.my_sales = request.POST['sales_accomplishments']
    advisor_details.total_clients_served = request.POST['total_clients_served']
    if not advisor_details.total_clients_served:
        advisor_details.total_clients_served = None
    advisor_details.total_advisors_connected = request.POST['total_advisors_connected']
    if not advisor_details.total_advisors_connected:
        advisor_details.total_advisors_connected = None
    advisor_details.financial_instruments = request.POST['product_experience']
    if request.POST.get('hidden_value',None):
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
    if request.POST.get('dsa_hidden_input_field',None):
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
    return JSONResponse('success',status=200)

# ================================================================
# Downloding advisor profile as a PDF
# ================================================================
@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def download_advisor_profile(request):
    user = User.objects.get(username = request.user.username)
    filename = user.first_name
    user_profile = UserProfile.objects.get(user = request.user)
    advisor = Advisor.objects.get(user_profile =request.user.profile)
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
    office_address=''
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

    server_url =settings.DEFAULT_DOMAIN_URL
    feedbacks=None
    feedbacks = AdvisorRating.objects.filter(
        advisor=advisor,
        user_type='member').exclude(feedback__isnull=True)
    # Fetching all Company profiles who all are approved
    company_obj = CompanyAdvisorMapping.objects.filter(\
        advisor_user_profile = request.user.profile,
        status = constants.APPROVED).values('company_user_profile')
    company_profile = UserProfile.objects.filter(id__in = company_obj)
    aprroved_companies = AffiliatedCompany.objects.filter(user_profile__in = company_profile)
    # Giving Position to the Advisor according to their gole
    advisor_level = ''
    clients_level = ''
    level_advisor = ''
    advisor = request.user.profile.advisor
    # Fetching Referred registered advisors
    refered_members = Advisor.objects.filter(\
        is_register_advisor=True,
        user_profile__referred_by=request.user).count()
    # Fetching count who rated minimum avg rating with 3.0
    rating_count = AdvisorRating.objects.filter(\
        avg_rating__gte = constants.MINIMUM_AVG_RATING,
        advisor=advisor,
        user_type="advisor").count()
    # Fetching count who ranked minimum avg rating with 3.0
    ranking_count = AdvisorRating.objects.filter(\
        avg_rating__gte = constants.MINIMUM_AVG_RATING,
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
    if ranking_count >=constants.SECOND_LEVEL_MINIMUM_ADVISOR_COUNT:
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

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def save_new_member(request):
    '''
    Description: Sending Client/Member Details to UPLYF for saving.
    '''
    user = User.objects.filter(username=request.POST.get('email',None))
    if not user:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        user = request.user
        advisor = user.profile.advisor
        member_data = {
            'first_name' : first_name,
            'last_name' : last_name,
            'user_email' : email,
            'mobile_number' : mobile,
            'advisor_name' : user.first_name+' '+user.last_name,
            'advisor_email' : user.username,
            'advisor_id': advisor.id,
            'sm_source':constants.UPWRDZ_MEDIA,
        }
        token = auth_token(settings.UPLYF_USER_NAME, settings.UPLYF_PASSWORD)
        headers = {'Authorization': 'JWT %s' %token['token']}
        user_response = requests.post(\
            api_constants.ADD_MEMBER,
            headers = headers,
            data = member_data,
            verify = constants.SSL_VERIFY
        )
        if user_response.status_code == 200 or user_response.status_code == 201:
            message = json.loads(user_response.content)
            message = message['message']
            logger.info(
                logme("saved client data into UPLYF database",request)
            )
            return JSONResponse({'data':message,'status':200})
        else:
            logger.info(
                logme("unable to save clients details into UPLYF database",request)
            )
            return JSONResponse({'data':'unable to save details','status':202})
    else:
        message="User is an Advisor"
        logger.info(
                logme("the advisor is already looped and registered in UPWRDZ",request)
            )
        return JSONResponse({'data':message,'status':202})

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def manage_client_transactions(request):
    response = manage_uplyf_transaction(request)
    return JsonResponse({'data':response},status=200)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def register_user(request):
    response = register(request)
    if response =="success":
       return JSONResponse({"data" : "success"},status = 200)
    else:
        return  JSONResponse({"data" : "failed"},status = 500)



@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def user_profile_basicdetails_details(request):
    response = user_profile_basicdetails(request)
    if response =="success":
       return JSONResponse({"data" :"success"},status =200)
    else:
        return  JSONResponse({"data" : "failed"},status = 500)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def country_details(request):
    array =[]
    country_list = serializers.serialize('json',Country.objects.all())
    country_list = json.loads(country_list)
    for i in country_list:
        array.append({'name':i['fields']['name']})
    return JSONResponse({'data' : array},status = 200)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def m_submit_eipv(request):
    response = submit_eipv(request)
    return JSONResponse({'data':response},status=200)


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def m_upload_eipv_documents(request):
    response = upload_eipv_documents(request)
    return JSONResponse(response,status=200)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def delete_uploaded_documents(request):
    response = delete_upload_file(request)
    return JSONResponse(response,status=200)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_myidentity_details(request):
    user = request.user.profile
    serializer = UserProfileSerializer(user)
    response = my_identity.views.index(request)
    return JSONResponse({'profile':serializer.data,'otherdetails':response},status=200)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_myhub_details(request):
    user_profile = request.user.profile
    advisor = user_profile.advisor
    serializer = UserProfileSerializer(user_profile)
    response = dashboard.views.index(request)
    advisor_serializer = AdvisorSerializer(advisor)
    invited_members = 0
    total_invited_members = 0
    if  not total_invited_members:
        total_invited_members =0

    return JSONResponse({
        'profile':serializer.data,
        'advisor':advisor_serializer.data,
        'otherdetails':response,
        'total_invited_members':total_invited_members,
         'calendly_link': advisor.calendly_link},status=200)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def list_enquiried_clients(request):
    response = dashboard.views.list_enquiried_clients(request)
    return JSONResponse({'data':response},status=200)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def list_client_enquiry(request):
    response = dashboard.views.view_client_enquiry(request)
    return JsonResponse({'data':response},status=200)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_client_details(request):
    user = request.user
    members = get_all_members(user.username)
    invited_members = get_invited_members(user.username)
    view_members = ''
    view_invited_members = ''
    if members:
        view_members = members['content']
    if invited_members:
        view_invited_members = invited_members['content']
    logger.info(
        logme("member modal view opened",request)
    )
    return JSONResponse({'member_list':view_members,'invited_member_list':view_invited_members},status=200)

@api_view(['GET'])
@permission_classes((AllowAny,))
def get_geo_location(request):
    lat = request.GET.get("lat",None)
    lng = request.GET.get("lng",None)
    key = request.GET.get("key","kantanand")
    res = {"status": "404", "polstal_code":"not found"}
    if lat and lng:
       geonames_url = "http://api.geonames.org/findNearbyPostalCodes?lat="+str(lat)+"&lng="+str(lng)+"&username="+str(key)+"&type=json"
       res = requests.get(geonames_url)
       if res.status_code == 200:
           res_json = json.loads(res.text)
           res = res_json
       else:
           res = {"status": "404", "polstal_code":"not found"}
    return JSONResponse(res,status=200)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def advisor_video_upload_api(request):
    '''
    update flag video_shoot_request and triggers email
    '''
    response = dashboard.views.video_shoot_request(request)
    if response:
        return JSONResponse({'response':'success'}, status=200)
    else:
        return JSONResponse({'response':'no content'}, status=204)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def advisor_video_publish_api(request):
    '''
    Saving Advisor published youtube video link and description
    '''
    response = dashboard.views.advisor_video_upload(request)
    if response:
        return JSONResponse({'response':'success'}, status=200)
    else:
        return JSONResponse({'response':'no content'}, status=204)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def send_meetup_invitation_mail(request):
    response = send_meetup_invitation(request)
    if response:
        return JSONResponse({'response':'success'}, status=200)
    else:
        return JSONResponse({'response':'no content'}, status=204)


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def m_eipv_form(request):
    response = personal_info_forms(request)
    return JSONResponse(response,status=200)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def m_send_otp(request):
    pincode = request.POST['pincode']
    chk = India_Pincode.objects.filter(pin_code = pincode).first()
    if chk:
       response =  send_otp(request)
       return JSONResponse(response,status=200)
    else:
        return JSONResponse({"data":"pincode error"},status=200)


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def m_verify_otp(request):
    response = verify_otp(request)
    return JSONResponse(response,status=200)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def m_geteipv_data(request):
    response = submit_eipv_doc(request)
    return JSONResponse(response,status=200)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def save_language_details(request):
    languages_known_speak = request.POST.get('languages_known_speak',None)
    languages_known_read_write = request.POST.get('languages_known_read_write',None)
    user_profile = request.user.profile
    user_profile.language_known = languages_known_speak
    user_profile.languages_known_read_write = languages_known_read_write
    user_profile.save()
    return JSONResponse({'response':'success'}, status=200)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def save_mypromise(request):
    my_promise = request.POST.get('my_promise', None)
    user_profile = request.user.profile
    advisor_details = Advisor.objects.filter(user_profile = user_profile).first()
    advisor_details.my_promise = my_promise
    advisor_details.save()
    return JSONResponse({'response':'success'}, status=200)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def save_mybelief(request):
    my_belief = request.POST.get('my_belief', None)
    user_profile = request.user.profile
    user_profile.my_belief = my_belief
    user_profile.save()
    return JSONResponse({'response':'success'}, status=200)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def save_contectdetails(request):
    response = update_contact_details(request)
    return JSONResponse({'response':'success'}, status=200)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def education_details(request):
    response = educational_qualification(request)
    return JSONResponse({'data':'success'}, status=200)    

@api_view(['POST'])
@permission_classes((AllowAny,))
def direct_signup(request):
    response = email_signup(request)
    return response

@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def checkEmail(request):
    response = check_email(request)
    return response
    

@api_view(['POST'])
@permission_classes((AllowAny,))
def signup_send_otp(request):
    response = send_signup_otp(request)
    return response

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def calendly_save_link(request):
    response = save_calendly_link(request)
    return response

@api_view(['POST'])
@permission_classes((AllowAny,))
def resend_email_mobile_otps_mob(request):
    response = resend_email_mobile_otps(request)
    return response

@api_view(['POST'])
@permission_classes((AllowAny,))
def validate_otp_mob(request):
    response = validate_otp(request)
    return response  

@api_view(['GET'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def list_member_invitation_mobile(request):
    webinar_event = webinar_views.WebinarMemberRegistration()
    response = webinar_event.get(request)
    return JSONResponse({'data':response}, status=200)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def save_skillsdetails(request):
    '''
        Descrption: Advisor is Adding Skills/My Identity.
    '''
    user_profile = request.user.profile
    advisor = user_profile.advisor
    skills = request.POST.getlist('skills_content[]', None)
    skills_data = ','.join([x.encode('UTF') for x in skills])
    if skills_data:
        advisor.skills = skills_data
        advisor.save()
        return JSONResponse({'response':'success'}, status=200)
    else:
        return JSONResponse({'response':'no content'}, status=204)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def register_member_webinar_mobile(request):
    webinar_event = WebinarMemberRegistration()
    response = webinar_event.post(request)
    return JSONResponse({'data':response}, status=200)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def create_mygrowth_mobile(request):
    response =  my_growth_index(request)
    return JSONResponse({'data':response}, status=200)
    

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def my_webinar_room_name(request):
    response = webinar_views.check_room_name(request)
    return JSONResponse({'data':response}, status=200)
@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def save_advisory_specialization(request):
    advisor = request.user.profile.advisor
    if request.POST['financial_instruments']:
        advisor.financial_instruments = request.POST.get('financial_instruments', None)
        advisor.save()
        logger.info(
            logme('onchange saved financial instruments', request)
        )
        return JSONResponse({'data':"success"}, status=200)
    else:
        logger.error(
            logme('onchange failed to save financial instruments', request)
        )
        return JSONResponse({'data':"failed"}, status=202)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def save_additional_qualification(request):
    user_profile = request.user.profile
    college_name = request.POST.get('college_name', None)
    qualification = request.POST.get('qualification', None)
    year_of_passout = request.POST.get('year_of_passout', None)
    additional_qualification = request.POST.get('additional_qualification', None)
    if college_name and qualification and year_of_passout:
        user_profile = request.user.profile
        user_profile.college_name = college_name
        user_profile.qualification = qualification
        user_profile.year_passout = year_of_passout
        if additional_qualification:
            user_profile.additional_qualification = additional_qualification
        user_profile.save()
        return JSONResponse({'data':"success"}, status=200)
    else:
        logger.error(
            logme('onchange failed to save additional qualification', request)
            )


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def regulatory_certification_registration(request):
    regulatory_certification_data = request.body
    if regulatory_certification_data:
        regulatory_certification = json.loads(regulatory_certification_data)
        advisor_details = Advisor.objects.get(user_profile_id=request.user.profile.id)
        sebi_regi = 'sebi_regi'
        amfi_regi = 'amfi_regi'
        irda_regi = 'irda_regi'
        other_regi = 'other_regi'
        rera_values = 'rera_state'
        dsa_result = 'dsa_bank_name'
        if sebi_regi in regulatory_certification and regulatory_certification['sebi_regi']!="":
            advisor_details.sebi_number = regulatory_certification['sebi_regi']
            if regulatory_certification.get('sebi_validity', None):
                advisor_details.sebi_expiry_date = datetime.strptime(regulatory_certification.get('sebi_validity',None), '%Y-%m-%d').strftime('%Y-%m-%d')
            if regulatory_certification.get('sebi_valid_from', None):
                advisor_details.sebi_start_date = datetime.strptime(regulatory_certification.get('sebi_valid_from', None), '%Y-%m-%d').strftime('%Y-%m-%d')
        else:
            advisor_details.sebi_number =""
            advisor_details.sebi_expiry_date = None
            advisor_details.sebi_start_date = None
        if amfi_regi in regulatory_certification and regulatory_certification['amfi_regi']!="":
            advisor_details.amfi_number = regulatory_certification['amfi_regi']
            if regulatory_certification.get('amfi_validity', None):
                advisor_details.amfi_expiry_date = datetime.strptime(regulatory_certification.get('amfi_validity', None), '%Y-%m-%d').strftime('%Y-%m-%d')
            if regulatory_certification.get('amfi_valid_from', None):
                advisor_details.amfi_start_date = datetime.strptime(regulatory_certification.get('amfi_valid_from', None), '%Y-%m-%d').strftime('%Y-%m-%d')
        else:
            advisor_details.amfi_number =""
            advisor_details.amfi_expiry_date = None
            advisor_details.amfi_start_date = None
        if irda_regi in regulatory_certification and regulatory_certification['irda_regi']!="":
            advisor_details.irda_number = regulatory_certification['irda_regi']
            if regulatory_certification.get('irda_validity', None):
                advisor_details.irda_expiry_date = datetime.strptime(regulatory_certification.get('irda_validity', None), '%Y-%m-%d').strftime('%Y-%m-%d')
            if regulatory_certification.get('irda_valid_from', None):
                advisor_details.irda_start_date = datetime.strptime(regulatory_certification.get('irda_valid_from', None), '%Y-%m-%d').strftime('%Y-%m-%d')
        else:
            advisor_details.irda_number =""
            advisor_details.irda_expiry_date = None
            advisor_details.irda_start_date = None
        if other_regi in regulatory_certification and regulatory_certification['other_authotity']!="":
            advisor_details.other_registered_organisation = regulatory_certification['other_authotity']
            if regulatory_certification['other_regi']:
                advisor_details.other_registered_number = regulatory_certification['other_regi']
            if regulatory_certification['other_validity']:
                advisor_details.other_expiry_date = regulatory_certification['other_validity']
        else:
            advisor_details.other_registered_organisation =""
            advisor_details.other_registered_number=""
            advisor_details.other_expiry_date = None
        if regulatory_certification['rera_values']:
            if regulatory_certification['rera_values'][0]['rera_state']:
                rera_values = json.dumps(regulatory_certification['rera_values'])
                advisor_details.rera_details = rera_values
                advisor_details.is_rera = True
            else:
                rera_values = ''
                advisor_details.rera_details = rera_values
                advisor_details.is_rera = False
        if regulatory_certification['dsa_result']:
            if regulatory_certification['dsa_result'][0]['dsa_bank_name']:
                dsa_values = json.dumps(regulatory_certification['dsa_result'])
                dsa_json = dsa_values
            else:
                dsa_json = ''
            advisor_details.dsa_details = dsa_json
        advisor_details.save()
        logger.info(
            logme('saved regulatory certification registration', request)
        )
        return JSONResponse({'data':"success"}, status=200)
    else:
        logger.error(
            logme('failed unable to save regulatory certification registration', request)
        )
        return JSONResponse({'data':"failed"}, status=202)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def save_clients(request):
    response = save_total_clients_served_count(request)
    return JSONResponse(response,status=200)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def save_advisor(request):
    response = save_total_advisors_connected_count(request)
    return JSONResponse(response,status=200)


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def save_aboutme(request):
    response = save_self_declaration(request)
    return JSONResponse(response, status=200)

@api_view(['GET'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_digital_link(request):
    user_profile = request.user.profile
    get_data = DigitalFootPrint.objects.filter(user_profile = user_profile)
    list_data = []
    if get_data:
        for i in get_data:
            list_data.append(i.digital_links)
    return JSONResponse(list_data, status=200)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def save_digital_link(request):
    response = save_foot_print_verification(request)
    return JSONResponse(response, status=200)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def delete_foot_print(request):
    response = delete_foot_print_verification(request)
    return JSONResponse(response, status=200)


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def advisor_profile_answer(request):
    response = user_profile_answer(request)
    return Response(response)

@api_view(['GET'])
@permission_classes((AllowAny,))
def get_profile_card(request):
    '''
    Description: Getting Batch card details and sending response as javascript to load the
        batch card in third parties websites.
    '''
    if request.method == 'GET':
        batch_code = request.GET.get('batch', None)
        user_profile = UserProfile.objects.filter(
            batch_code=batch_code).first()
        if user_profile:
            user_profile = user_profile
            title = user_profile.first_name + " "+user_profile.last_name
            location = user_profile.city
            pic = get_binary_image(user_profile)
        else:
            title = None
            location = None
            pic = None
        return HttpResponse("myCallbackFunction({'tit': "+"'"+title+"'"+", 'loc':"+"'"+location+"'"+",'pic':"+"'"+pic+"'"+"})",
            content_type='application/x-javascript'
        )

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,SessionAuthentication))
@permission_classes((IsAuthenticated,))
def check_and_register(request):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    if request.method == 'POST':
        serializer = AdvisorRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user_email = serializer.data.get('email')
            first_name = serializer.data.get('first_name')
            mobile = serializer.data.get('mobile')
            direct_signup = LoginCommonFunctions({'request':request})
            data = {
                'password' : None,
                'email': user_email,
                'first_name' : first_name,
                'mobile' : mobile,
            }
            is_created = direct_signup.createuser(
                object = data
            )
            status_code = is_created.get('status')
            user = User.objects.get(username=user_email)
            user_message = 'Advisor already exists and Session Created'        
            user_profile = user.profile
            users_role = serializer.data.get('user_role')
            if status_code == 200 or status_code == 201:
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                response_object = None
                if user.is_active and user.is_staff:
                    '''
                    set username and token in response object if the user need to continue
                    '''
                    login(request, user)
                    payload = jwt_payload_handler(user)
                    token = jwt_encode_handler(payload)
                    response_object = {
                        'token': token,
                        'first_name': user.profile.first_name,
                        'email': user.profile.email,
                        'source_media': user.profile.source_media,
                        'message': user_message,
                        'new_user': status_code,
                        'status': 'success',
                        'users_role': users_role
                    }
                    logger.info(
                        logme(
                            'set username and token in response object if the user need to continue', request)
                    )
                    return JSONResponse(response_object, status=200)
                else:
                    user_message = "Your Account is Locked, Please Contact UPWRDZ Admin"
                    response_object = {
                        'message': user_message,
                        'new_user': status_code,
                        'status': 'false',
                    }
                    logger.info(
                        logme(
                            'user details are not proper, user cannot continue', request)
                    )
                    return JSONResponse(response_object, status=200)
            else:
                user_message ="Account cannot not be created at this moment"
                response_object = {
                        'message': user_message,
                        'new_user': status_code,
                        'status': 'false',
                    }
                return JSONResponse(response_object, status=500)
        else:
            return JSONResponse(serializer.errors, status=400)


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication, ))
@permission_classes((AllowAny, ))
def check_auth_and_redirect(request):
    '''
    Check auth Token and update session and redirect to upwrdz
    '''
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    if request.method == 'POST':
        users_role = request.POST.get('users_role', None)
        username = request.POST.get('username', None)
        token = request.POST.get('token', None)
        city = request.POST.get('users_city', None)
        first_name = request.POST.get('users_first_name', None)
        country = request.POST.get('users_country', None)
        zipcode = request.POST.get('users_zipcode', None)
        address = request.POST.get('users_address', None) 
        user = User.objects.get(username = username)
        if user:
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            payload = jwt_payload_handler(user)
            user_token = jwt_encode_handler(payload)
            user_profile = user.profile
            advisor = user_profile.advisor
            fasia_company_details(user_profile, advisor)
            # Generating registration id and saving
            if not user_profile.registration_id:
                while(True):
                    num =  uuid.uuid4().hex[:10]
                    if not UserProfile.objects.filter(registration_id = num):
                        user_profile.registration_id = num
                        user_profile.save()
                        break
                    else:
                        continue
            if not advisor.is_register_advisor and not advisor.ipv_status:
                upload_documents = UploadDocuments.objects.filter(user_profile = user_profile)
                eipv_face_capture = upload_documents.filter(
                    documents_type='eipv_face_capture')
                eipv_face_capture = upload_documents.filter(documents_type = 'eipv_face_capture')
                eipv_aadhaar = upload_documents.filter(documents_type='eipv_aadhaar')
                if eipv_aadhaar:
                    eipv_aadhaar = eipv_aadhaar.first()
                if first_name and country and zipcode and address and city:
                    personal_info = 0
                return render(request, 'signup/submit_eipv.html', locals())
            claimed_status = check_advisor_claimed(request)
            if claimed_status:
                if advisor.is_submitted_all and advisor.is_submitted_questions:
                    return HttpResponseRedirect('/dashboard/')
                else:
                    return HttpResponseRedirect('/signup/aadhaar_verification/')
                logger.info(logme(
                    'user redirected to the desired page', request)
                )
            else:
                logger.info(
                    logme(
                        'user redirected to the desired page', request)
                )
                return HttpResponseRedirect('/advisor_check/get_advisor_card/')
        else:
            logger.info(
                logme(
                    'user is not authorized to log in', request)
            )
            return HttpResponse('You are not authorized to log in.')
    else:
        return HttpResponse('You are not Logged in.')


def fasia_company_details(user_profile, advisor):
    if user_profile and advisor:
        user, create = User.objects.get_or_create(username=FASIA_COMPANY_EMAIL,email=FASIA_COMPANY_EMAIL)
        user_profiles = user.profile
        user_profiles.is_company=True
        user_profiles.save()
        if create:
            company_user_profile = AffiliatedCompany.objects.create(user_profile = user_profiles)
        else:
            company_user_profile = AffiliatedCompany.objects.filter(user_profile = user_profiles).first()
        company_user_profile.company_name = FASIAAMERICA
        company_user_profile.website_url = FASIA_DOMAIN
        company_user_profile.save()
        affiliate_company_child, status = CompanyAdvisorMapping.objects.get_or_create(
            advisor_user_profile = user_profile,
            company_user_profile = user_profiles
        )
        if status:
            company_user_profile.users_count = company_user_profile.users_count + 1
            company_user_profile.save()
            affiliate_company_child.status = constants.APPROVED
            affiliate_company_child.save()
    return True


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def save_adhaar(request):
    adhaar_number = request.POST.get('adhaar_number', None)
    if adhaar_number:
        user_profile = request.user.profile
        user_profile.adhaar_card = adhaar_number
        user_profile.save()
        return JSONResponse({'data':"aadhaar number saved successfully","status":200})
    else:
        return JSONResponse({'data':"aadhaar number could not be saved.","status":500})


@api_view(['GET'])
@permission_classes((AllowAny, ))
def get_server_ip(request):
    ip_info = get_ipinfo(request)
    return Response(data={'ip_info':ip_info}, status=200)


@api_view(["POST"])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def save_country(request):
    country = request.data.get('country', '')
    if country:
        user_profile = request.user.profile
        user_profile.country = country
        user_profile.save()
        return Response({'data':"Country saved successfully"}, status=200)
    else:
        return Response({'data':"country not saved successfully"}, stauts=400)

@api_view(["POST"])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def logout_user(request):
        userLogout = user_logout(request)
        return Response({'data':"successfully"}, status=200)

