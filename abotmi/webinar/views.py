# python lib
import datetime
import json
import logging

# Django lib
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.utils.crypto import get_random_string
from django.views.generic import View

# Database models
from datacenter.models import TrackWebinar, ClientAdvisorMapping

# Constatns
from webinar.constants import WEBINAR_API_KEY
from common.constants import WEBINAR

# ClickMeeting API
from webinar.ClickMeetingRestClient import ClickMeetingRestClient
# Local imports
from webinar.forms import CreateWebinarForm
from webinar.serializers import WebinarUserProfileData
from common.views import (get_uplyf_project_list, logme, AdvisorCommonFunction,
    get_all_client)

# logger for this app
logger = logging.getLogger(__name__)


def dashboard(request):
    '''
    Listing all Webinar events
    '''
    context = RequestContext(request)
    title = WEBINAR
    list_of_webinars = None
    list_of_webinars = TrackWebinar.objects.filter(
        user_profile=request.user.profile
    ).order_by('-pk')
    is_webinar_created = request.session.get('is_webinar_created', None)
    if is_webinar_created: del request.session['is_webinar_created']
    req_type_mob = request.GET.get('req_type', None)
    if req_type_mob == "mobile":
        return list_of_webinars
    context_dict = {
        'list_of_webinars': list_of_webinars,
        'TABLE_ID': 'webinar_list',
        'title': title,
        'is_webinar_created': is_webinar_created
    }
    logger.info(
        logme('all webinar event list returned for this user',request)
    )
    return render_to_response(
        "webinar/webinar_meetings_list.html", context_dict, context)


def create_webinar(request):
    '''
    Create a Webinar
    POST:
        -> Creating the Webinar in ClickMeeting and saving details
    GET:
        -> Loading Create Webinar form
    '''
    PAGE_TITLE = 'Create Webinar'
    req_type= request.POST.get("req_type",None)
    if request.method == 'POST':
        client = ClickMeetingRestClient({'api_key': WEBINAR_API_KEY})
        webinar_from = CreateWebinarForm(request.POST)
        if webinar_from.is_valid():
            room_id = None
            room_name = webinar_from.cleaned_data['name']
            lobby_description = webinar_from.cleaned_data.get('lobby_description', None)
            starts_at = webinar_from.cleaned_data['starts_at']
            starts_at = starts_at.strftime("%Y-%m-%d %H:%M:%S")
            duration = webinar_from.cleaned_data['duration']
            duration_hh_mm = str(datetime.timedelta(minutes=duration))[:-3]
            meeting_password = get_random_string(length=8)
            uplyf_project = webinar_from.cleaned_data.get('uplyf_project', None)
            params = {
                'name': room_name,
                'room_type': 'webinar',
                'permanent_room': 0,
                'starts_at': starts_at,
                'duration': duration_hh_mm,
                'access_type': 2,
                'password': meeting_password,
                'lobby_enabled': 1,
                'lobby_description': lobby_description,
                'registration' : {
                    'enabled': 1
                },
                'settings': {
                    'show_on_personal_page': 1,
                    'thank_you_emails_enabled': 1,
                    'connection_tester_enabled': 1,
                    'phonegateway_enabled': 0,
                    'recorder_autostart_enabled': 0,
                    'room_invite_button_enabled': 0,
                    'social_media_sharing_enabled': 1,
                    'connection_status_enabled': 1,
                    'thank_you_page_url': settings.DEFAULT_DOMAIN_URL+'/'
                }
            }
            room = None
            try:
                # Creat A Room
                room = client.addConference(params)
                room_id = room['room']['id']
                # Add Presenter
                params = {
                    'email' : request.user.username,
                    'nickname' : request.user.profile.first_name+' '\
                        +request.user.profile.last_name,
                    'role' : 'host',
                    'password': room['room']['password']
                }
                host_user = client.conferenceAutologinHash(room_id, params)
                # Register That Persion and save deatils in TrackWebinar
                webinar_object, status = TrackWebinar.objects.get_or_create(
                    room_id=room_id)
                if status:
                    webinar_object.room_name = room['room']['name']
                    webinar_object.room_url  = room['room']['room_url']
                    webinar_object.room_pin  = room['room']['room_pin']
                    webinar_object.room_type = room['room']['room_type']
                    webinar_object.starts_at = starts_at
                    webinar_object.duration  = datetime.timedelta(minutes=duration)
                    webinar_object.password  = room['room']['password']
                    webinar_object.user_profile = request.user.profile
                    webinar_object.auto_login_host_url = host_user['autologin_hash']
                    webinar_object.uplyf_project = uplyf_project
                    webinar_object.save()
                    request.session['is_webinar_created'] = True
                    logger.info(
                        logme('created/updated webinar', request)
                    )
                    if  req_type =="mobile":
                         return "success"
                    else:
                        return redirect('webinar:dashboard')
            except Exception as e:
                try:
                    ex_message = json.loads(str(e))
                    if ex_message:
                        if ex_message['name'] == "INVALID_DATES":
                            webinar_from.add_error(
                                'starts_at',
                                "Please enter the valid Date and Time."
                            )
                    else:
                        messages = e
                except:
                    pass
                logger.info(
                    logme('failed to create/update webinar form %s'%(str(e)),request)
                )
        else:
            logger.info(
                logme('invalid create/update webinar form', request)
            )
    if request.method == 'GET':
        initial_data = {
            'name': request.user.username,
            'lobby_description': 'Please Give your lobby description ',
            'duration': 'HH:mm'
        }
        webinar_from = CreateWebinarForm()
        logger.info(
            logme('create webinar form opened', request)
        )
    return render(request,"webinar/webinar_create_session.html",locals())


def delete_webinar(request):
    '''
    Delete Webinar in ClickMeeting and database
    '''
    context = RequestContext(request)
    req_type_mob = request.POST.get('req_type',None)
    if request.method == 'POST':
        client = ClickMeetingRestClient({'api_key': WEBINAR_API_KEY})
        try:
            room_data = TrackWebinar.objects.get(
                room_id=request.POST['room_id'],
                user_profile=request.user.profile
            )
            if room_data:
                client.deleteConference(request.POST['room_id'])
                room_data.delete()
        except:
            logger.info(
                logme('room %s not found in TrackWebinar for deleting the room' %(
                    str(request.POST['room_id'])),request)
            )
            return HttpResponse('false')
        else:
            logger.info(
                logme('webinar with room id = %s deleted'%(
                    str(request.POST['room_id'])), request)
            )
            if  req_type_mob =="mobile":
                return "success"
            else:
                return HttpResponse('success')
    if request.method == 'GET':
       return HttpResponse('Access forbidden', status=405)


def check_room_name(request):
    '''
    Checking Room name already exists or not
    '''
    room_name_mobile = request.POST.get('room_name', None)
    req_type_mob = request.POST.get('req_type', None)
    if req_type_mob == "mobile":
        room_name = room_name_mobile
    else:
        room_name = request.POST['name']
    client = ClickMeetingRestClient({'api_key': WEBINAR_API_KEY})
    webinar_object = None
    room_list = None
    try:
        webinar_object = TrackWebinar.objects.get(room_name=room_name)
    except ObjectDoesNotExist:
        try:
            room_list = client.conferences()
            logger.info(
                logme('validation - room list accessed from click2meeting to check room exists or not', request)
            )
        except Exception, e:
            logger.info(
                logme('validation- unable to access room list from clickmeeting to check room exists or not', request)
            )
            raise e
        else:
            status = any(room_data['name'] == room_name for room_data in room_list)
            if status:
                logger.info(
                    logme('validation -webinar room already exists in click2meeting \
                        webinar account', request)
                )
                if req_type_mob == "mobile":
                    return "false"
                return HttpResponse('false')
        logger.info(
            logme('webinar room does not exist in click2meeting account',request)
        )
        if req_type_mob == "mobile":
            return "true"
        return HttpResponse('true')
    else:
        logger.info(
            logme('room exist', request)
        )
        if req_type_mob == "mobile":
            return "false"
        return HttpResponse('false')


class WebinarMemberRegistration(View):
    client = ClickMeetingRestClient({'api_key': WEBINAR_API_KEY})

    def get(self, request, *args, **kwargs):
        '''
        Descrption: Fetching Reffered advisors and Added members by the requested advisor
            -> Fetching Registered Members from Webinar event
            -> Listing out not Registered members from Reffered advisors and Added Clients
        '''
        title = WEBINAR
        room_id = kwargs.get('room_id')
        req_type_mob = request.GET.get('req_type',None)
        if req_type_mob == "mobile":
            room_id=request.GET.get('room_id',None)
        final_total_members = []
        final_total_advisors = []
        registered_member_in_webinar = 0
        registered_advisor_in_webinar = 0
        registered_webinar_members = None
        user = request.user
        if room_id:
            common_obj = AdvisorCommonFunction(request)
            ref_advisors = common_obj.get_reffred_advisors(user)
            reffered_advisors_serializer = WebinarUserProfileData(ref_advisors, many=True)
            reffered_advisors = reffered_advisors_serializer.data
            # Commented temporarily to stop addind clients/members into webinar
            # total_members = common.get_all_added_clients(user)
            # client_details=''
            # client_details = ClientAdvisorMapping.objects.filter(user_profile = request.user.profile)
            # client_list = []
            # if client_details:
            #     for client_detail in client_details:
            #         temp = {}
            #         temp['first_name'] = client_detail.client.first_name
            #         temp['email'] = client_detail.client.email
            #         temp['mobile'] = client_detail.client.mobile
            #         client_list.append(temp)
            total_members = get_all_client(request.user.profile)
            try:
                registered_webinar_members = self.client.conferenceRegistrations(room_id, 'all')
                webinar_members = [m['email']for m in registered_webinar_members]
                for mem in total_members:
                    if not mem['email'] in webinar_members:
                        final_total_members.append(mem)
                for ref_advisor in reffered_advisors:
                    if not ref_advisor['email'] in webinar_members:
                        final_total_advisors.append(ref_advisor)

                del(client)
                del(common_obj)
            except Exception, error_message:
                logger.info(
                    logme('Getting webinar event registered members error: %s'\
                        %(str(error_message)),request)
                )
            if req_type_mob == "mobile":
                data = {
                    'advisor_data' : final_total_advisors,
                    'member_data' : final_total_members,
                    'webinar_data': registered_webinar_members,
                    'room_id':room_id
                }
                return data
        return render(request, 'webinar/list_members_and_advisors.html', locals())

    def post(self, request, *args, **kwargs):
        '''
        Descrption: Regestering Member/Advisor in to Webinar event
        '''
        req_type_mob = request.POST.get('req_type',None)
        member=request.POST.get('member_details',None)
        if req_type_mob == "mobile":
            details_split = member.split(',')
            room_id = details_split[2]
            room_id=room_id.strip()
            member_details=details_split[0]+","+details_split[1]
        else:
            room_id = kwargs.get('room_id')
            member_details = request.POST.get('member_details', None)

        if member_details and room_id:
            details = member_details.split(',')
            participant_details = {
                'registration': {
                    1: details[0],
                    2: details[0],
                    3: details[1]
                }
            }
            try:
                participant_registration = self.client.addConferenceRegistration(\
                    room_id,
                    participant_details
                )
                logger.info(
                    logme('Added %s in webinar room id: %s'\
                        %(str(details[1]), room_id), request)
                )
                if req_type_mob == "mobile":
                    return "success"

                return HttpResponse('success')
            except Exception, error_message:
                logger.info(
                    logme('unable to added %s in webinar room id: %s--error message:%s'\
                        %(str(details[1]), room_id, error_message), request)
                )
                if req_type_mob == "mobile":
                    return "unable to add"
                return HttpResponse('unable to add')
        logger.info(
            logme('unable to added %s in webinar room id: %s'\
                %(str(details[1]), room_id), request)
        )
        return HttpResponse('unable to add')
