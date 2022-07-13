# REST APIS
# from reputation_index.common_functions import advisor_certification
# file moved to common_functions review and remove uwanted files
# python lib
import ast
import json
import logging
import requests

# Django lib
from django.http import JsonResponse
from django.shortcuts import render

# Rest framework lib
from rest_framework import status
from rest_framework.authentication import (SessionAuthentication, TokenAuthentication)
from rest_framework.decorators import (api_view, authentication_classes, 
    permission_classes)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

# Database models
from datacenter.models import UserProfile, AdvisorReputationIndex, ReputationIndexMetaData

from common.regular_expressions import valid_email, validate_pin
from common.views import get_number_of_language
from reputation_index import constants as rp_constants
# reputation index common file
from reputation_index.common_functions import (advisor_age, advisor_certification,
    advisor_eipv, advisor_loop_refer, advisor_meetup, advisor_office_address, 
    advisor_rating, advisor_rating_and_ranking, advisor_webinar, crisil_verification, 
    languages_known, languages_known_to_read_write, member_ranking, 
    social_media_communication, social_signup, advisor_scoring_fb, 
    advisor_scoring_linkedin, reputation_constants, 
    totol_clients_served_and_advisors_connected, save_advisor_reputation_index, 
    store_advisor_insurance_meta_data, get_insurance_metadata_by_user_profile, 
    advisor_hyperlocal_scoring, get_user_profile_by_email, advisors_rank_api)
from reputation_index.serializers import AdvisorReputationIndexSerializer
from reputation_index_signals.common_functions import (
    user_profile_get_insurance_meta_obj_to_store)
from reputation_index_signals.tasks import hyperlocal_advisor_scoring

logger = logging.getLogger(__name__)


def advisor_scoring_fb_api(request):
    '''
    Advisor Scoring facebook connect to textient
    '''
    advisor_email = request.POST.get('email', None)
    access_token = request.POST.get('access_token', None)
    if advisor_email and access_token:
        if valid_email(email=advisor_email):
            # kept for debugging purpose
            logger.info("user_profile_email :", advisor_email)
            logger.info("access_token :", access_token)
            res = advisor_scoring_fb(email=advisor_email, access_token=access_token)
            success_result = {
                'status': True,
                'message': 'request sent success: %s' %(res.text)
            }
            return JsonResponse(success_result, status=200)
        else:
            error_result = {
                'status': False,
                'message': 'email is not valid '
            }
            return JsonResponse(error_result, status=200)
    else:
        error_result = {
            'status': False,
            'message': 'email and access_token is required !'
        }
        return JsonResponse(error_result, status=200)


def advisor_scoring_linkedin_api(request):
    '''
    Advisor Scoring linkedin connect to textient
    '''
    advisor_email = request.POST.get('email', None)
    headLine = request.POST.get('headLine', None)
    summary = request.POST.get('summary', None)
    if advisor_email and headLine:
        if valid_email(email=advisor_email):
            send_summary = None
            if summary != "" or summary != None:
                send_summary = summary
            # kept for debugging purpose
            logger.info("user_profile_email:", advisor_email)
            logger.info("headLine :", headLine)
            logger.info("summary :", send_summary)
            res = advisor_scoring_linkedin(email=advisor_email, headLine=headLine, summary=send_summary)
            success_result = {
                'status': True,
                'message': 'request sent success: %s' %(res.text)
            }
            return JsonResponse(success_result, status=200)
        else:
            error_result = {
                'status': False,
                'message': 'email is not valid '
            }
            return JsonResponse(error_result, status=200)
    else:
        error_result = {
            'status': False,
            'message': 'email, headLine and summary is required !'
        }
        return JsonResponse(error_result, status=200)


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def advisor_scoring_points_api(request):
    """
    Advisor
    """
    pass


def check_social_email(request):
    """
    check_social_email for calculating scoring for social media
    """
    email = request.POST.get('email', None)
    if email:
        if email == request.user.profile.email:
            return JsonResponse({'status' : True}, status=200)
        else:
            return JsonResponse({'status' : False}, status=200)
    return JsonResponse({'status' : "Email is not provided"}, status=404)


def get_reputation_index_data(request):
    """
    Display reputation index of user
    """
    user_profile = request.user.profile
    rpi_data = AdvisorReputationIndex.objects.filter(user_profile=user_profile).first()
    general_data = None
    if rpi_data:
        serializer = AdvisorReputationIndexSerializer(rpi_data)
        rpi_data = serializer.data
        general_data = rpi_data.get('insurance',None)
        general_data = json.loads(general_data)
    return render(request, 'dashboard/reputation_index_modal.html', locals())


def create_insurance_meta_if_not_existed(request):
    """
    create insurance meta data obj if its not existed for user profile
    """
    user_profile = request.user.profile
    meta_data = get_insurance_metadata_by_user_profile(user_profile)
    if not meta_data:
        user_profile.total_languages = get_number_of_language(user_profile.language_known)
        user_profile.dob = ""
        meta_obj = user_profile_get_insurance_meta_obj_to_store(user_profile)
        logger.info(
            "Insurance meta data not present. So Create Insurance meta data object.")
        store_advisor_insurance_meta_data(meta_obj)
        return JsonResponse({'status' : True}, status=200)
    return JsonResponse({
            'status' : False, 
            'error':'ReputationIndexMetaData already present'
        }, status=200)


def advisor_reputation_for_hyperlocal(request):
    '''
    Call native reputation index api for advisor
    '''
    username = request.user.profile.email
    pincode = request.POST.get('pincode', None)
    hyperlocal_type = request.POST.get('hyperlocal_type', None)
    if username and pincode and hyperlocal_type:
        if valid_email(email=username) and validate_pin(pin=pincode):
            if get_user_profile_by_email(username):
                # kept for debugging purpose
                logger.info("username : ", username)
                logger.info("pincode :", pincode)
                logger.info("hyperlocal_type :", hyperlocal_type)
                hyperlocal_advisor_scoring.apply_async(
                    (username, pincode, hyperlocal_type,)
                )
                #commented for reference
                # res = advisor_hyperlocal_scoring(username=username, pincode=pincode, hyperlocal_type=hyperlocal_type)
                result = {
                    'status': True,
                    'message': 'Request sent successfully'
                }
            else:
                result = {
                    'status': False,
                    'message': 'username is not found '
                }
        else:
            result = {
                'status': False,
                'message': 'username is not valid '
            }
    else:
        result = {
            'status': False,
            'message': 'username, hyperlocal_type and pincode required !'
        }
    return JsonResponse(result, status=200)


def get_geo_pincode(request):
    '''
    Call native reputation index api for advisor
    '''
    lat = request.POST.get('lat', None)
    long = request.POST.get('long', None)
    if lat and long:
        pass
    else:
        result = {
            'status': False,
            'message': 'Lattitude and Longitude is required'
        }
    return JsonResponse(result, status=200)


def get_advisors_rank(request):
    '''
    Get Ranks for advisors for my repute page
    '''
    username = request.POST.get('username', None)
    pincode = request.POST.get('pincode', None)
    if username and pincode:
        if valid_email(email=username) and validate_pin(pin=pincode):
            if get_user_profile_by_email(username):
                logger.info(" get_advisors_rank Api call ")
                logger.info("username : ", username)
                logger.info("pincode :", pincode)
                res = advisors_rank_api(username=username, pincode=pincode)
                if res.status_code == 200:
                    res = json.loads(res.text)
                    if res['meta']['username'] == request.user.profile.email:
                        res['meta']['image'] = ""
                        if request.user.profile.picture:
                            res['meta']['image'] = str(request.user.profile.picture.url)
                        res['meta']['name'] = str(request.user.profile.first_name)
                    index = 0
                    for adv in res['advisors']:
                        if adv['username'] == request.user.profile.email:
                            res['advisors'][index]['is_current_user'] = 1
                        else:
                            res['advisors'][index]['is_current_user'] = 0
                        user_profile = get_user_profile_by_email(adv['username'])
                        res['advisors'][index]['image'] = ""
                        if user_profile:
                            if user_profile.picture:
                                res['advisors'][index]['image'] = str(user_profile.picture.url)
                            res['advisors'][index]['name'] = str(user_profile.first_name)
                            index = index + 1
                    result = {
                        'status': True,
                        'data':res
                    }
                else:
                    result = {
                        'status': False,
                        'message': 'Rank api response failed'
                    }
            else:
                result = {
                    'status': False,
                    'message': 'username is not found '
                }
        else:
            result = {
                'status': False,
                'message': 'username or pincode is not valid '
            }
    else:
        result = {
            'status': False,
            'message': 'username and pincode required !'
        }
    return JsonResponse(result, status=200)


def call_native(request):
    '''
    This method will call native raputaion index api
    '''
    up = request.user.profile
    if up:
        if up.pincode:
            pincode = up.pincode
            is_stored = store_pincode_in_ri_meta(up,pincode)
            if is_stored:
                result = {
                'status': 200,
                'message': 'Pincode present !'
                }
            else:
                result = {
                'status': 400,
                'message': 'Reputaion data not present. Please edit your profile!'
                }
        else:
            result = {
                'status': 500,
                'message': 'Pincode is null !'
            }
    else:
        result = {
            'status': 404,
            'message': 'User profile not present !'
        }
    return JsonResponse(result, status=200)


def store_pincode_in_ri_meta(up, pincode):
    '''
    Storing Pincode in meta table
    '''
    ri_meta = ReputationIndexMetaData.objects.filter(user_profile = up.id).first()
    if ri_meta:
        if ri_meta.pincodes:
            try:
                pincode_arr = ast.literal_eval(ri_meta.pincodes)
                if int(pincode) not in pincode_arr:
                    ri_meta.pincodes = str([int(pincode)])
                    # following code for practice locations
                    # ri_meta.pincodes = str(pincode_arr.append(int(pincode)))
            except:
                ri_meta.pincodes = str([int(pincode)])
        ri_meta.save()
        return True
    return False


def update_pincode(request):
    '''
    Updating the pincode
    '''
    pincode = request.POST.get('pincode', None)
    if pincode:
        if validate_pin(pin=pincode):
            up = UserProfile.objects.filter(id = request.user.profile.id).first()
            if up:
                up.pincode = pincode
                up.save()
                result = {
                    'status': 200,
                    'message': 'Pincode successfully updated.'
                }
            else:
                result = {
                    'status': 500,
                    'message': 'Invalide User'
                }
        else:
            result = {
                'status': 400,
                'message': 'pincode is not valid'
            }
    else:
        result = {
            'status': 400,
            'message': 'Please provide pincode'
        }
    return JsonResponse(result, status=200)
