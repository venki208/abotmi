# Python lib
import logging
import os
import json
import requests, hashlib
import datetime
import random
import traceback, datetime ,base64
import cStringIO as StringIO

# django libs
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import logout
from django.conf import settings
from django.core.files.storage import default_storage
from django.utils.crypto import get_random_string
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

# models
from django.contrib.auth.models import User
from datacenter.models import UserProfile, India_Pincode, AadhaarTransactions, UploadDocuments,\
    PromoCodes, Advisor, ReferralPointsType, ReferralPoints, AdvisorType

# Local imports
from aadhaar import conf as local_settings
from common import constants
from nfadmin.views import registered_advisor_email
from signup.djmail import send_mandrill_email, send_mandrill_email_with_attachement
from common.views import referral_points, logme, get_sms_status
from common.utils import send_sms_alert

# Create your views here.
logger = logging.getLogger(__name__)

def get_user_data_from_aadhar(request):
    '''
    Description: Function gets aadhaar transaction object 
        and sends to aadhaar to get the user information
    '''
    saCode = local_settings.AADHAAR_SACODE
    uuid = request.GET.get("uuid", None)
    requestId = request.GET.get("requestId", None)
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
        if "aadhaar_transaction_id" in request.session:
            del request.session['aadhaar_transaction_id']
        request.session['aadhaar_transaction_id'] = aadhaar_transaction_id
        aadhaa_transaction.save()
        return aadhar_response, aadhaa_transaction
    else:
        return None


def success(request):
    '''
    Description: Getting User information from aadhaar server.
        --> updating success or failure status in AadhaarTransactions table.
    '''
    aadhar_response, aadhaa_transaction = get_user_data_from_aadhar(request)
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
                    datetime_object = datetime.datetime.strptime(dob, '%d-%m-%Y')
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
            user_profile.country = constants.INDIAN_NATIONALITY
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
    return render(request, 'aadhar/success.html', locals())


# def send_aadhaar_error_to_email(context, request):
#     '''
#     Discription: sents the mail conatins error message
#     '''
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

def failed(request):
    '''
    Description: If aadhaar transaction failes we are storing failed in success_status
    '''
    requestId = request.GET.get('requestId', None)
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
    return render(request, 'aadhar/failure.html', locals())


def member_failed(request):
    '''
    Description: If aadhaar transaction failes we are storing failed in success_status
    '''
    request.session['is_kyc_success'] = None
    request.session['is_adhaar_no_invalid'] = None
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
            request.session['is_adhaar_no_invalid'] = True
        else:
            request.session['is_kyc_success'] = False
    logger.info(
        logme('aadhaar : error happened during verifying ekyc error code is {}'.format(error_code), request)
    )
    return HttpResponseRedirect('/dashboard/')


def member_success(request):
    '''
    Description: If aadhaar transaction failes we are storing failed in success_status
    '''
    aadhar_response, aadhaa_transaction = get_user_data_from_aadhar(request)
    logger.info(
        logme('aadhaar:fetched data from aadhaar in member success', request)
    )
    request.session['email_from_aadhaar'] = None
    request.session['is_kyc_success'] = None
    request.session['ekyc_verified_data'] = None
    request.session['is_ekyc_verified_data_present'] = None
    request.session['aadhaar_mobile'] = None
    result = json.loads(aadhar_response.content)
    user_information = result['success']
    status_code = None
    status_code = result['aadhaar-status-code']
    if user_information:
        # request.session['ekyc_verified_data'] = str(aadhar_response.content)
        request.session['is_ekyc_verified_data_present'] = True
        request.session['is_kyc_success'] = True
        if 'poi' in result['kyc']:
            poi = result['kyc']['poi']
            if 'email' in poi:
                email = result['kyc']['poi']['email']
                if email:
                    request.session['email_from_aadhaar'] = email
            if "phone" in poi:
                phone = result['kyc']['poi']['phone']
                request.session['aadhaar_mobile'] = phone
            logger.info(
                logme('aadhaar: fetched data and stored in session in member success', request)
            )
            return HttpResponseRedirect('/dashboard/')
    else:
        logger.info(
            logme('aadhaar:ekyc success status failed', request)
        )
        request.session['is_kyc_success'] = False
    return HttpResponseRedirect('/')


def prepare_request_for_aadhaar_bridge(user_profile, aadhaar_number, type):
    '''
    Description: It gathers data for aadhaar bridge request
    '''
    if type == local_settings.AADHAAR_ADVISOR_STR :
        random_no=random.randint(100000,999999)
        aadhaar_transaction = AadhaarTransactions.objects.create(
            user_profile_id = user_profile.id,
            email = user_profile.email,
            aadhaar_number = aadhaar_number,
            api_type = 'AADHAAR_SEND_OTP'
        )
        request_id = str(random_no)+str(aadhaar_transaction.id)
        successUrl = local_settings.AADHAAR_SUCCESS_URL
        failureUrl = local_settings.AADHAAR_FAILURE_URL
    else:
        random_no=random.randint(100000,999999)
        aadhaar_transaction = AadhaarTransactions.objects.create(
            user_profile_id = user_profile.id,
            email = user_profile.email,
            aadhaar_number = aadhaar_number,
            api_type = 'MEM_OTP'
        )
        request_id = str(random_no)+str(aadhaar_transaction.id)
        successUrl = local_settings.AADHAAR_MEMBER_SUCCESS_URL
        failureUrl = local_settings.AADHAAR_MEMBER_FAILRE_URL

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
        'channel' : 'BOTH',
        'successUrl' : successUrl,
        'failureUrl' : failureUrl,
    }
    return data

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
            return JsonResponse(data,status=200)
        else:
            logger.info(
                logme('aadhaar:aadhaar number already exists', request)
            )
            return JsonResponse({'data':'Aadhaar number is already exist.'},status=401)
    logger.info(
        logme('aadhaar:aadhaar number not found', request)
    )
    return JsonResponse({'data':'Please send aadhar number'}, status =400)


def check_aadhaar_present(request):
    '''
    Description: This api is to check weather aadhaar number is present in our system or not
    '''
    aadhaar_number = request.POST.get('aadhaar_no', None)
    if aadhaar_number:
        url = settings.UPLYF_SERVER+"/api/aadhar/check_aadhaar_present"
        data = {"aadhaar_no" : aadhaar_number}
        response = requests.post(url,data = data, verify=constants.SSL_VERIFY)
        status_code = response.status_code
        json_res_data = json.loads(response.text)
        if status_code == 200:
            user_profile = request.user.profile
            data = prepare_request_for_aadhaar_bridge(user_profile, aadhaar_number, local_settings.AADHAAR_MEMBER_STR)
            logger.info(
                logme('aadhaar:checked aadhaar number not present in UPLYF', request)
            )
            return JsonResponse(data, status = 200)
        logger.info(
            logme('aadhaar:checked aadhaar number is present in UPLYF', request)
        )
        return JsonResponse(json_res_data, status = status_code)
    else:
        logger.info(
            logme('aadhaar:aadhaar number not found', request)
        )
        return JsonResponse({"data":"Aadhaar number not provided"}, status=401)

def create_client_in_uplyf(request):
    '''
    Description: Function hits UPLYF to create a client with relevant details.
    '''
    email = request.POST.get('email',None)
    alternate_email = request.POST.get('alternate_email',None)
    aadhaar_transaction_id = request.POST.get('aadhaar_transaction_id',None)
    if aadhaar_transaction_id:
        aadhaar_transaction = AadhaarTransactions.objects.filter(id=aadhaar_transaction_id)
    else:
        aadhaar_transaction = AadhaarTransactions.objects.filter(id=request.session['aadhaar_transaction_id'])
    advisor_id = request.user.profile.advisor.id
    advisor_name = request.user.first_name+' '+request.user.last_name,
    advisor_email = request.user.username
    status_code = 400
    if aadhaar_transaction:
        ekyc_data = aadhaar_transaction.first().ekyc_details
        if email and ekyc_data and alternate_email:
            url = settings.UPLYF_SERVER+"/api/aadhar/reai_advisor_creating_member"
            data = {"result" : ekyc_data, "email":email, "alternate_email":alternate_email, "advisor_id": advisor_id, "advisor_email":advisor_email,"advisor_name":advisor_name}
            response = requests.post(url, data = data, verify=constants.SSL_VERIFY)
            status_code = response.status_code
            json_res_data = json.loads(response.text)
            if 'aadhaar_transaction_id' in request.session:
                del request.session['aadhaar_transaction_id']
            logger.info(
                logme('aadhaar:created member(added client) in UPLYF', request)
            )
            return JsonResponse(json_res_data, status = status_code)
    logger.info(
        logme('aadhaar:aadhaar transaction not found', request)
    )
    return JsonResponse({"result":"Data not provided."}, status = status_code)


def delete_session_aadhaar_values(request):
    '''
    Description: It deletes the session 
    '''
    if "aadhaar_transaction_id" in request.session:
        del request.session['aadhaar_transaction_id']
    return JsonResponse({"result":"success"}, status = 200)


def upwrdz_aadhaar_check(request):
    '''
    Description: To check in UPWRDZ DB this particular aadhaar is present or not
    '''
    if request.method == "POST":
        aadhaar_no = request.POST['aadhaar_no']
        try:
            user_adr = UserProfile.objects.get(adhaar_card=aadhaar_no)
            logger.info(
                logme('validation-checked aadhaar present in UPWRDZ', request)
            )
            return HttpResponse('false')
        except:
            logger.info(
                logme('validation-checked aadhaar not present in UPWRDZ', request)
            )
            return HttpResponse('true')
    if request.method == "GET":
        logger.info(
            logme('GET request - access forbidden to check aadhaar present in UPWRDZ', request)
        )
        return HttpResponse('sorry cannot process')
