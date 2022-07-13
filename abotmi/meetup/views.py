# python lib
import datetime
import json
import logging
import requests
import math

# Django lib
from django.conf import settings
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from math import floor
from django.utils import timezone

# Database models
from datacenter.models import MeetUpEvent, Advisor, UserProfile, Member

# Constants
from common import constants, api_constants

# Local imports
from api.serializers import UserProfileSerializer, MeetupUpdateSerializer
from common.views import auth_token, get_all_members, logme, get_all_client,\
    mlegion_auth_token
from common.utils import generate_key, send_sms_alert
from forms import MeetupForm
from signup.djmail import send_mandrill_email

logger = logging.getLogger(__name__)


def get_events_list(request):
    user_profile = request.user.profile
    event_data_list = MeetUpEvent.objects.filter(
        user_profile=user_profile, is_deleted=False, scheduled__gte=timezone.now())
    return event_data_list


def list_meetup_events(request):
    ''' get all the events created by the logged in advisor '''
    message = ""
    req_type = request.GET.get('req_type', None)
    title = constants.MEETUP
    event_data_list = get_events_list(request)
    if req_type == "mobile":
        return event_data_list
    if not event_data_list:
        no_meetup_events = constants.NO_MEETUP_EVENTS
    logger.info(
        logme('returned list of all meetup events', request)
    )
    return render(request, 'meetup/list_meetup_events.html', locals())


@login_required(login_url='/')
def create_meetup_event(request):
    ''' create a event in the meetup site and in our database '''
    message = ''
    if request.method == "POST":
        req_type = request.POST.get('req_type', None)
        meetup_form = MeetupForm(request.POST)
        user_profile = request.user.profile
        if meetup_form.is_valid():
            event_date = request.POST.get('scheduled', None)
            event_address = request.POST.get('address', None)
            name = request.POST.get('name', None)
            location = request.POST.get('location', None)
            landmark = request.POST.get('landmark', None)
            uplyf_project = request.POST.get('project', None)
            event_date = datetime.datetime.strptime(event_date, '%Y-%m-%d %H:%M:%S')
            event_description = request.POST.get('description', None)
            description = '<html><body>' + request.POST.get('description', None) + \
                '<b>address:</b>  ' + request.POST.get('address', None) + '</body></html>'
            h = int(request.POST.get('hours', None))
            m = int(request.POST.get('minutes', None))
            '''convert the hours and minutes into milliseconds'''
            duration = int(3600000 * h + 60000 * m)
            '''
            create meetup event
            '''
            headers = {
                "Content-type": "application/x-www-form-urlencoded",
            }
            event_data = {
                'organizer_email': user_profile.email,
                'organizer_name': user_profile.first_name,
                'organizer_mobile': user_profile.mobile,
                'event_name': name,
                'event_description': event_description,
                'event_landmark': landmark,
                'event_location': location,
                'event_date': event_date,
                'category': constants.MLEGION_CATEGORY,
                'sub_category': constants.MLEGION_SUB_CATEGORY,
                'address': event_address,
                'duration': duration
            }
            '''
            compile and make the request
            '''
            try:
                token = mlegion_auth_token(
                    settings.MLEGION_USERNAME, settings.MLEGION_PASSWORD)
                headers = {'Authorization': 'Bearer %s' % token['auth_token']}
                create_event = requests.post(
                    api_constants.CREATE_EVENTS,
                    headers=headers,
                    data=event_data,
                    verify=constants.SSL_VERIFY)
                event_obj = json.loads(create_event.content)
                event_id = event_obj['event_id']
                status_code = event_obj['status_code']
                if status_code:
                    meetup_obj, status = MeetUpEvent.objects.get_or_create(
                        user_profile=user_profile, meetup_event_id=event_id)
                    if status:
                        meetup_obj.scheduled = event_date
                        meetup_obj.address = event_address
                        meetup_obj.name = name
                        meetup_obj.meetup_event_id = event_id
                        meetup_obj.description = event_description
                        meetup_obj.duration = duration
                        meetup_obj.uplyf_project = uplyf_project
                        meetup_obj.meetup_location = location
                        meetup_obj.meetup_landmark = landmark
                        meetup_obj.save()
                if not req_type:
                    messages.success(request, constants.MEETUP_CREATE_EVENT_SUCCESS)
                ''' Gets all the advisors/members referred by the logged in advisor
                    to send mail invitation for the created meetup
                '''
                logger.info(
                    logme('meetup event saved successfully', request)
                )
                if req_type == "mobile":
                    return "success"
                else:
                    return HttpResponseRedirect('/meetup/list_meetup_events/')
            except Exception as e:
                print e
                json_obj = ""
                logger.info(
                    logme('failed to create meetup event', request)
                )
                return HttpResponse(
                    'Unable to create event Please try again after some time')
        else:
            return form.errors
    else:
        req_type = request.GET.get('req_type', None)
        form = MeetupForm()
        project_name = ''
        token = auth_token(settings.UPLYF_USER_NAME, settings.UPLYF_PASSWORD)
        headers = {'Authorization': 'JWT %s' % token['token']}
        project_name = requests.get(
            api_constants.UPLYF_PROJECT_NAMES,
            headers=headers,
            verify=constants.SSL_VERIFY)
        if project_name.status_code == 200:
            project_name = json.loads(project_name.content)
            project_name = project_name['data']
            if req_type == "mobile":
                return project_name
            else:
                hours = constants.EVENT_HOURS
                minuts = constants.EVENT_MINUTES
                logger.info(
                    logme('rendered create meetup event form', request)
                )
        return render(request, 'meetup/create_event.html', locals())


@login_required()
def send_meetup_invitation(request):
    '''This function sends mail/ invitation to the selected mail ids '''
    message = ""
    SEND_MEETUP_INVITATION_SUCCESS = constants.SEND_MEETUP_INVITATION_SUCCESS
    meetup_details = MeetUpEvent.objects.filter(
        user_profile__user=request.user).latest('created_date')
    event_data_list = get_events_list(request)
    emails = []
    req_mobile = request.POST.get("req_type", None)
    if req_mobile == "mobile":
        emails = request.POST.getlist('email_list[]')
    else:
        emails = request.POST.getlist('email_list')
    for email in emails:
        value_split = email.split(',')
        name = value_split[0]
        email_id = value_split[1]
        contact = value_split[2]
        context_dict = {
            'event_name': meetup_details.name,
            'event_description': meetup_details.description,
            'address': meetup_details.address,
            'scheduled': meetup_details.scheduled.strftime("%Y-%m-%d %H:%M"),
            'duration': meetup_details.duration,
            'advisor_contact_number': contact,
            'name': name
        }
        send_mandrill_email('REIA_15_01', [email_id], context=context_dict)
        if not req_mobile == "mobile":
            messages.success(request, constants.SEND_MEETUP_INVITATION_SUCCESS)
    meetup_events = MeetUpEvent.objects.filter(user_profile__user=request.user)
    if not meetup_events:
        no_meetup_events = constants.NO_MEETUP_EVENTS
    logger.info(
        logme('sent invitation email for the meetup to selected emailids', request)
    )
    return render(request, 'meetup/list_meetup_events.html', locals())


def list_mail_invitation(request):
    '''This function selects the advisors/ members referred by the logged in advisor '''
    view_members = ''
    user_profile_obj = UserProfile.objects.filter(
        advisor__is_register_advisor=True,
        referred_by=request.user)
    view_members = get_all_client(request.user.profile)
    if request.GET.get('req_type', None) == "mobile":
        serializer = UserProfileSerializer(user_profile_obj, many=True)
        data = {
            'advisor_data': serializer.data if user_profile_obj else '',
            'member_data': view_members if view_members else ''
        }
        return data
    logger.info(
        logme('returned list of advisor and members in meetup', request)
    )
    return render(request, 'meetup/list_invite_members_advisors.html', locals())


def delete_meetup(request):
    '''
    Deleting Meetup event from database
    '''
    event_id = request.POST.get('event_id', None)
    meetup_event = MeetUpEvent.objects.filter(meetup_event_id=event_id).first()
    if meetup_event:
        meetup_event.is_deleted = True
        meetup_event.save()
        logger.info(
            logme('deleted meetup event id =%s' % (str(event_id)), request)
        )
    return "success"


def delete_meetup_event(request, event_id):
    '''
    Deleting meetup event
    '''
    delete_meetup(event_id)
    if request.data.get("req_type", None) == "mobile":
        return "success"
    else:
        return HttpResponseRedirect('/meetup/list_meetup_events')


def delete_meetup_event_from_post(request):
    '''
    Deleting meetup event
    '''
    title = constants.MEETUP
    event_id = request.POST.get('event_id', None)
    user_profile = request.user.profile
    token = mlegion_auth_token(
        settings.MLEGION_USERNAME, settings.MLEGION_PASSWORD)
    headers = {'Authorization': 'Bearer %s' % token['auth_token']}
    organizer_data = {
        'organizer_email': user_profile.email, 'event_id': event_id}
    events_status = requests.post(
        api_constants.DELETE_EVENTS,
        headers=headers,
        data=organizer_data,
        verify=constants.SSL_VERIFY)
    events_status = events_status.content
    events_status = json.loads(events_status)
    status = events_status['status']
    if status:
        delete_local = delete_meetup(request)
        if delete_local == "success":
            token = auth_token(settings.UPLYF_USER_NAME, settings.UPLYF_PASSWORD)
            headers = {'Authorization': 'JWT %s' % token['token']}
            send_email = requests.post(
                api_constants.SEND_DELETED_EVENT_DATA,
                headers=headers,
                data={"meetup_event_id": event_id},
                verify=False)
            return JsonResponse({'data': events_status})
        else:
            return JsonResponse({'status': False, "error": "delete failed in upwrdzdb"})
    else:
        return JsonResponse({'status': False, "error": "delete failed in mlegiondb"})


def update_events(request):
    '''
    Update the event form list function
    '''   
    if request.method == "POST":
        event_id = request.POST.get('event_id', None)
        req_type = request.POST.get('req_type', None)
        form = MeetupForm(request.POST)
        if form.is_valid():
            event_date = request.POST.get('scheduled', None)
            event_address = request.POST.get('address', None)
            name = request.POST.get('name', None)
            location = request.POST.get('location', None)
            landmark = request.POST.get('landmark', None)
            uplyf_project = request.POST.get('project', None)
            description = request.POST.get('description', None)
            h = int(request.POST.get('hours', None))
            m = int(request.POST.get('minutes', None))
            '''convert the hours and minutes into milliseconds'''
            duration = int(3600000 * h + 60000 * m)
            user_profile = request.user.profile
            event_data = {
                'organizer_email': user_profile.email,
                'event_id': event_id,
                'event_name': name,
                'event_description': description,
                'event_landmark': landmark,
                'event_location': location,
                'event_date': event_date,
                'duration': duration,
                'address': event_address
            }
            token = mlegion_auth_token(
                settings.MLEGION_USERNAME, settings.MLEGION_PASSWORD)
            headers = {'Authorization': 'Bearer %s' % token['auth_token']}
            update_mlegion = requests.post(
                api_constants.UPDATE_EVENTS,
                headers=headers,
                data=event_data,
                verify=constants.SSL_VERIFY)
            update_mlegion_obj = json.loads(update_mlegion.content)
            if update_mlegion_obj['status']:
                meetup_list = MeetUpEvent.objects.filter(
                    user_profile=user_profile, meetup_event_id=event_id).select_related(
                        'user_profile').first()
                if meetup_list:
                    meetup_list.scheduled = event_date
                    meetup_list.address = event_address
                    meetup_list.name = name
                    meetup_list.meetup_event_id = event_id
                    meetup_list.description = description
                    meetup_list.duration = duration
                    meetup_list.uplyf_project = uplyf_project
                    meetup_list.meetup_location = location
                    meetup_list.meetup_landmark = landmark
                    meetup_list.save()
                token = auth_token(settings.UPLYF_USER_NAME, settings.UPLYF_PASSWORD)
                headers = {'Authorization': 'JWT %s' % token['token']}
                event_data = MeetupUpdateSerializer(
                    meetup_list)
                event_data = event_data.data
                send_email = requests.post(
                    api_constants.SEND_UPDATED_EVENT,
                    headers=headers,
                    data=event_data,
                    verify=constants.SSL_VERIFY)
        if req_type == "mobile":
            return "success"
        else:
            return HttpResponseRedirect('/meetup/list_meetup_events')
    else:
        form = MeetupForm()
        event_id = request.GET.get('id', None)
        hours = constants.EVENT_HOURS
        minuts = constants.EVENT_MINUTES
        event_data_list = MeetUpEvent.objects.filter(meetup_event_id=event_id).first()
        seconds = math.floor(int(event_data_list.duration)/1000)
        minute = math.floor(seconds/60)
        seconds = seconds % 60
        hour = math.floor(minute/60)
        event_data_list.minute = int(minute % 60)
        event_data_list.minute = str(event_data_list.minute)
        day = math.floor(hour/24)
        event_data_list.hours = int(hour % 24)
        event_data_list.hours = str(event_data_list.hours)
        form = MeetupForm(initial={'scheduled': event_data_list.scheduled})
        token = auth_token(settings.UPLYF_USER_NAME, settings.UPLYF_PASSWORD)
        headers = {'Authorization': 'JWT %s' % token['token']}
        project_name = requests.get(
            api_constants.UPLYF_PROJECT_NAMES,
            headers=headers,
            verify=constants.SSL_VERIFY)
        if project_name.status_code == 200:
            project_name = json.loads(project_name.content)
            project_name = project_name['data']
        return render(request, 'meetup/create_event.html', locals())