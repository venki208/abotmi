import json, re

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone

from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import status

from dashboard.views import add_client_to_comapny, save_new_member
from common.notification.views import NotificationFunctions
from common.constants import APPROVED
from common.notification.constants import CLIENT_NOTIFICATION,\
    LEVEL_1_CLIENT_SIGNUP_NOTIFCATION, LEVEL_2_CLIENT_SIGNUP_NOTIFCATION,\
    LEVEL_1_CLIENT_REGISTER_NOTIFCATION, LEVEL_2_CLIENT_REGISTER_NOTIFCATION
from django.conf import settings

from datacenter.models import UserProfile, Advisor, AffiliatedCompany, CompanyAdvisorMapping,\
    TrackWebinar, MeetUpEvent

from api.serializers import ComapnySerializer, CompanyAdvisorsList, AdvisorSerializer, \
    WebinarSerializer, MeetupSerializer

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_companies_list(request):
    # Fetching registered companies
    companies = AffiliatedCompany.objects.filter(terms_and_conditions = True)
    serializer = ComapnySerializer(instance = companies, many=True)
    return Response(serializer.data, status=200)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def save_new_member_upwrdz(request):
    response = save_new_member(request)
    if response == "User already exists":
        return Response({'data':"client already exist","status":200})
    elif response == "User Created":
        return Response({'data':"success","status":201})
    elif response == "User is an Advisor":
        return Response({'data':"User already looped  and registered","status":202})
    elif  response == "unabletosave" :
        return Response({'data':'Client is already created in Uplyf',"status":203})
    else:
        return Response({'data':"failure","status":500})



@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication, ))
@permission_classes((IsAuthenticated, ))
def get_companies_advisors_list(request):
    '''
    Descrption: Sending Prefered Advisors List to UPLYF
    '''
    # Fetching Advisors regarding selected companies
    company_list = request.data.get('company_list', None)
    if company_list:
        # Splitting the company list with '-' or ',' and taking every second element in array list
        company_list = re.split('-|,' ,company_list)[1::2]
        # Getting advisors who got approved by company and registered by REIA
        company_advisor = CompanyAdvisorMapping.objects.filter(\
            company_user_profile_id__in = company_list,
            advisor_user_profile__advisor__is_register_advisor = True,
            status = APPROVED
        )
        if company_advisor:
            serializer = CompanyAdvisorsList(instance = company_advisor, many=True)
            return Response(serializer.data, status=200)
        else:
            return JsonResponse(data={}, status=201)
    else:
        data = {}
        return JsonResponse(data, status = 404)


@api_view(['GET'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def advisor_selection(request):
    '''
    Descrption:REIOM adivsor selection for opportunity booking
        we need to suggest user nearby advisors
    '''
    location = request.GET.get('location', None)
    if location:
        advisor_list = Advisor.objects.filter(\
            practice_location=location,
            is_register_advisor = True
        )
        if advisor_list:
            serializer = AdvisorSerializer(instance=advisor_list, many=True)
            return Response(serializer.data, status=200)
        else:
            return JsonResponse(data={}, status=200)
    else:
        data = {}
        return JsonResponse(data, status=404)


@api_view(['GET'])
@authentication_classes((JSONWebTokenAuthentication, ))
@permission_classes((IsAuthenticated, ))
def get_all_register_advisors(request):
    '''
    Descrption: Sending All Register Advisors to UPLYF
    '''
    advisor_list = Advisor.objects.filter(is_register_advisor = True)
    if advisor_list:
        serializer = AdvisorSerializer(instance = advisor_list, many=True)
        return Response(serializer.data, status=200)
    else:
        return JsonResponse(data={}, status=200)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication, ))
@permission_classes((IsAuthenticated, ))
def get_webniar_list(request):
    '''
    Used to Return webinar list
    '''
    project_id = request.POST.get('project_id', None)
    if project_id:
        webniar_list = TrackWebinar.objects.filter(uplyf_project__contains=project_id)
    else:
        webniar_list = TrackWebinar.objects.all()
    webniar_serializer = WebinarSerializer(webniar_list, many=True)
    return Response(webniar_serializer.data, status=200)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication, ))
@permission_classes((IsAuthenticated, ))
def get_meetup_list(request):
    '''
    Used to Return Mlegion event list
    '''
    project_id = request.POST.get('project_id', None)
    if project_id:
        meetup_list = MeetUpEvent.objects.filter(
            uplyf_project__contains=project_id, is_deleted=False, scheduled__gte=timezone.now())
    else:
        meetup_list = MeetUpEvent.objects.filter(
            is_deleted=False, scheduled__gte=timezone.now())
    meetup_serializer = MeetupSerializer(meetup_list, many=True)
    return Response(meetup_serializer.data, status=200)

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication, ))
@permission_classes((IsAuthenticated, ))
def get_advisor_profile_link(request):
    '''
    Used to return advisor profile link or Digital link
    '''
    email = request.POST.get('advisor_email', None)
    if email:
        user_profile = UserProfile.objects.filter(email = email)
        if user_profile:
            user_profile = user_profile.first()
            link = settings.DEFAULT_DOMAIN_URL+'/profile/'+user_profile.referral_code+'/'
            return Response(
                data = {'user_exists':True,'advisor_profile_link':link},
                status = status.HTTP_200_OK
            )
        else:
            return Response(data={'user_exists':False}, status = status.HTTP_204_NO_CONTENT)
    return Response(data={}, status = status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication, ))
@permission_classes((IsAuthenticated, ))
def save_client_notification_upwrdz(request):
    '''
    used to save client signup/registration notifcation for advisor
    '''
    client_name = request.POST.get('client_name', None)
    reg_status = request.POST.get('reg_status', False)
    advisor_id = request.POST.get('advisor_id', None)
    if client_name and advisor_id:
        advisor = Advisor.objects.filter(
            id = advisor_id).select_related('user_profile').first()
        user_profile = advisor.user_profile
        parent_user_profile = user_profile.referred_by.profile
        notif = NotificationFunctions(request, user_profile)
        if not reg_status:
            level_1_notif = LEVEL_1_CLIENT_SIGNUP_NOTIFCATION %(client_name)
            level_2_notif = LEVEL_2_CLIENT_SIGNUP_NOTIFCATION %(
                client_name, user_profile.first_name)
        else:
            level_1_notif = LEVEL_1_CLIENT_REGISTER_NOTIFCATION %(client_name)
            level_2_notif = LEVEL_2_CLIENT_REGISTER_NOTIFCATION %(
                client_name, user_profile.first_name)
        notif.save_notification(level_1_notif, CLIENT_NOTIFICATION)
        notif.save_notification(level_2_notif, CLIENT_NOTIFICATION)
        del(notif)
        return Response(data={}, status=status.HTTP_201_CREATED)
    else:
        return Response(data={'error:missing parameter'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication, ))
@permission_classes((IsAuthenticated, ))
def increament_registered_user_count_by_event_id(request):
    '''
    Updating the registered user count
    '''
    event_id = request.POST.get('event_id', None)
    if event_id:
        meetup_event = MeetUpEvent.objects.filter(meetup_event_id=event_id).first()
        if meetup_event:
            meetup_event.registered_user_count = meetup_event.registered_user_count + 1
            meetup_event.save()
            return Response(
                data={'status':True},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                data={'status':False},
                status=status.HTTP_400_BAD_REQUEST
           )
    else:
        return Response(
            data={'status':False},
            status=status.HTTP_404_NOT_FOUND
        )
