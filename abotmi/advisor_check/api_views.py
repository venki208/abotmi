# Python Lib
import json

# Django Modules
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

# Database Models
from advisor_check.models import AdvisorData

# Rest Framework imports
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

# Local Imports
from advisor_check.serializers import AdvisorCheckSerializer


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def search_advisors(request):
    '''Search advisors by name, city, mobile or email'''
    advisor_data = request.POST.get('individual', None)
    if advisor_data:
        advisor_obj = AdvisorData.objects.filter(
            Q(email__icontains=advisor_data)
            | Q(name__icontains=advisor_data)
            | Q(city__icontains=advisor_data)
            | Q(mobile__icontains=advisor_data)
            | Q(mobile2__icontains=advisor_data)
        )
        serializer = AdvisorCheckSerializer(instance=advisor_obj, many=True)
        return Response(serializer.data, status=200)
    else:
        return Response(data={}, status=204)


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def advisor_connect(request):
    '''Member can connect with advisor'''
    if request.method == 'POST':
        member_id = request.POST.get('member_id', None)
        advisor_id = request.POST.get('advisor_id', None)
        if advisor_id:
            try:
                advisor_obj = AdvisorData.objects.filter(id=advisor_id).first()
                if advisor_obj.connected_members:
                    advisor_obj.connected_members = advisor_obj.connected_members \
                        + ',' + member_id
                else:
                    advisor_obj.connected_members = member_id
                advisor_obj.save()
            except ObjectDoesNotExist:
                return Response('Failed', status=204)
