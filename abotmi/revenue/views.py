# python lib
import json
import logging
import requests

# Django lib
from django.conf import settings
from django.db.models import Sum,Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Rest framework lib
from rest_framework import status
from rest_framework.decorators import (api_view, authentication_classes, 
    permission_classes)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

# Database models
from datacenter.models import (Advisor, UserProfile, ClientPlatform, ClientDetails, 
    RevenueType, TypeRevenuePlatformMapping, RevenueTransactions)

# Constatns
from common import api_constants
from common import constants as common_constants
from revenue import constants

# Local imports
from common.utils import sequence_number, JSONEncoder
from common.views import logme, auth_token
from login.decorators import allow_nfadmin
from revenue.serializers import (RevenueTransactionsSerializer, RevenueTypeSerializer, 
    PlatformSerializer, ClientSerializer)

logger = logging.getLogger(__name__)


def index(request):
    if settings.UPWRDZ_USERNAME and settings.UPWRDZ_PASSWORD:
        auth_credentials = {
            'username' : settings.UPWRDZ_USERNAME,
            'password' : settings.UPWRDZ_PASSWORD
        }
        auth_response = requests.post(
            api_constants.UPWRDZ_AUTH_URL,
            data = auth_credentials,
            verify = common_constants.SSL_VERIFY
        )
        token = json.loads(auth_response.content.encode('UTF-8'))
        if token:
            authorization = "JWT "+token['token']
            headers = {
                'Authorization' : authorization
            }
            rev_res = requests.post(
                api_constants.ADVISOR_REVENUE_DETAILS_API,
                data={ 'email': request.user.profile.email },
                headers=headers
            )
            total_details = json.loads(rev_res.content) 
            rev_details = total_details['revenue_transactions_data']
            pay = total_details['total_payable']
            receive = total_details['total_receivable']
            wallet = total_details['total_wallet']

            parent_email = None
            grand_parent_email = None
            if request.user.profile.referred_by:
                parent_obj = request.user.profile.referred_by.profile
                parent_email = parent_obj.email
                if parent_obj.referred_by:
                    grand_parent_email = parent_obj.referred_by.profile.email
    return render(request, 'revenue/revenue_transaction_success_view.html', locals())


@allow_nfadmin
def revenue_statement_by_email(request):
    """
    Describtion : This function helps to bring revenue statement by email. nfadmin able 
        to use this feature.
    """
    if request.method == "GET":
        return render(request, 'revenue/revenue_statement_by_email.html', locals())

    if request.method == "POST":
        email = request.POST.get('email', None)
        if settings.UPWRDZ_USERNAME and settings.UPWRDZ_PASSWORD:
            auth_credentials = {
                'username' : settings.UPWRDZ_USERNAME,
                'password' : settings.UPWRDZ_PASSWORD
            }
            auth_response = requests.post(\
                api_constants.UPWRDZ_AUTH_URL,
                data = auth_credentials,
                verify = common_constants.SSL_VERIFY
            )
            token = json.loads(auth_response.content.encode('UTF-8'))
            if token:
                authorization = "JWT "+token['token']
                headers = {
                    'Authorization' : authorization
                }
                rev_res = requests.post(
                    api_constants.ADVISOR_REVENUE_DETAILS_API,
                    data={ 'email': email },
                    headers=headers
                )
                total_details = json.loads(rev_res.content) 
                rev_details = total_details['revenue_transactions_data']
                pay = total_details['total_payable']
                receive = total_details['total_receivable']
                wallet = total_details['total_wallet']

                parent_email = None
                grand_parent_email = None
                user_profile = UserProfile.objects.filter(email=email).first()
                if user_profile.referred_by:
                    parent_obj = user_profile.referred_by.profile
                    parent_email = parent_obj.email
                    if parent_obj.referred_by:
                        grand_parent_email = parent_obj.referred_by.profile.email
        return render(request, 'revenue/statement_view.html', locals())


def add_client(request):
    """
    For Demo purpose: add client form
    """
    if request.method == 'GET':
        return render(request, 'revenue/create_revenue_transaction_view.html', locals())


def list_client(request):
    """
    For Demo purpose: list client details
    """
    clients_obj = ClientDetails.objects.all()
    if request.method == 'GET':
        return render(request, 'revenue/list_clients_view.html', locals())


def open_transaction(request):
    """
    For Demo purpose: trnasaction statement detials
    """
    if request.method == 'POST':
        client_id = request.POST.get('client_id', None)
        email = ClientDetails.objects.filter(id = client_id).first().email
        return render(request, 'revenue/make_transaction_view.html', locals())


def create_transaction(request):
    """
    For Demo purpose: create transaciton
    """
    if request.method == 'POST':
        product_id = request.POST.get('product_id', None)
        transaction_value = request.POST.get('transaction_value', None)
        client_email = request.POST.get('client_email', None)
        client_obj = ClientDetails.objects.filter(email = client_email).first()
        params = {
            'product_id': product_id,
            'service_advisor_email': request.user.profile.email,
            'client_email': client_email,
            'platform_name':'uplyf',
            'transaction_value': transaction_value
        }

        if settings.UPWRDZ_USERNAME and settings.UPWRDZ_PASSWORD:
            auth_credentials = {
                'username' : settings.UPWRDZ_USERNAME,
                'password' : settings.UPWRDZ_PASSWORD
            }
            auth_response = requests.post(\
                api_constants.UPWRDZ_AUTH_URL,
                data = auth_credentials,
                verify = common_constants.SSL_VERIFY
            )
            token = json.loads(auth_response.content.encode('UTF-8'))
            if token:
                authorization = "JWT "+token['token']
                headers = {
                    'Authorization' : authorization
                }
                rev_res = requests.post(
                    api_constants.MAKE_TRANSACTIONS_API,
                    data = params,
                    headers=headers
                )
        return redirect('/revenue/')


# ==============
# Revenue API's
# ==============
@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def create_revenue_type(request):
    '''
    Description : To creating revenue type. "revenue" type is revenue from different kind 
        of activities/platform.
        1. Receiving arguments revenue_name, description, is active (True/False) default 
            is True
        2. creat revenue_type record by name and other details
    '''
    revenue_name = request.POST.get('revenue_name', None)
    is_active = request.POST.get('is_active', None)
    description = request.POST.get('description', None)
    revenue_type, created = RevenueType.objects.get_or_create(revenue_name=revenue_name)
    if created:
        revenue_type.revenue_code = sequence_number("Revenue","RVN")
        revenue_type.is_active = True
        revenue_type.description = description
        revenue_type.save()
        logger.info(
            logme('revenue type created successfully',request)
        )
        return JsonResponse({'status':'success'},status=200)
    else:
        logger.info(
            logme('failed, unable to create revenue type',request)
        )
        return JsonResponse({'status':'invalid data, unable to create revenue type'})


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_all_revenue_type(request):
    '''
    Description : Get all revenue type
    '''
    revenue_type = RevenueType.objects.all()
    serializer = RevenueTypeSerializer(revenue_type, many=True)
    return JsonResponse(serializer.data, status=200)


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def create_client_platform(request):
    '''
    Description : To creat platform, which platform are using advisor service
        for their client.
    '''
    platform_name = request.POST.get('platform_name', None)
    platform_email = request.POST.get('platform_email', None)
    is_active = request.POST.get('is_active', None)
    client_platform, created = ClientPlatform.objects.get_or_create (
        platform_email=platform_email,
        platform_name=platform_name
    )
    if created:
        client_platform.platform_code = sequence_number("Platform","PLT")
        client_platform.is_active = True
        client_platform.save()
        logger.info(
            logme('client platform created successfully',request)
        )
        return JsonResponse({'status':'success'},status=200)
    else:
        logger.info(
            logme('failed, unable to create client platform',request)
        )
        return JsonResponse({'status':'invalid data, unable to create client platform'})


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_all_platform(request):
    '''
    Description : Get all platform
    '''
    platform = ClientPlatform.objects.all()
    serializer = PlatformSerializer(platform, many=True)
    return JsonResponse(serializer.data, status=200)


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def create_client(request):
    '''
    Description : To creat client who wants to use service from upwrdz
    '''
    first_name = request.POST.get('first_name', None)
    last_name = request.POST.get('last_name', None)
    client_email = request.POST.get('email', None)
    client_mobile = request.POST.get('mobile', None)
    client_address = request.POST.get('address', None)
    platform_email = request.POST.get('platform_email', None)
    client_platform = ClientPlatform.objects.filter(platform_email=platform_email).first()
    if client_platform:
        client_details, created = ClientDetails.objects.get_or_create(
            email=client_email,
            client_platform=client_platform
        )
        if created:
            client_details.first_name = first_name
            client_details.last_name = last_name
            client_details.mobile = client_mobile
            client_details.address = client_address
            client_details.save()
            logger.info(
                logme('created client successfully',request)
            )
            return JsonResponse({'status':'success'}, status=201)
        else:
            return JsonResponse({'status':'exists'}, status=200)
    else:
        logger.info(
            logme('failed, unable to create client',request)
        )
        return JsonResponse({'status':'invalid data, unable to create client'})


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_all_client(request):
    '''
    Description : Get all client
    '''
    client = ClientDetails.objects.all()
    serializer = ClientSerializer(client, many=True)
    return JsonResponse(serializer.data, status=200)


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def map_revenuetype_platform(request):
    '''
    Description:
        Getting client platform email and revenue type
        Creating map table of that.
    '''
    platform_email = request.POST.get('platform_email', None)
    revenue_code = request.POST.get('revenue_code', None)
    receiver_email = request.POST.get('receiver_email', None)
    revenue_percentage = request.POST.get('revenue_percentage', None)
    is_active = request.POST.get('is_active', None)
    client_platform = ClientPlatform.objects.filter(platform_email=platform_email).first()
    receiver = ClientPlatform.objects.filter(platform_email=receiver_email).first()
    revenue_type = RevenueType.objects.filter(revenue_code=revenue_code).first()
    if revenue_type and client_platform and receiver:
        type_revenue_platform_mapping, created = TypeRevenuePlatformMapping.objects.get_or_create(
            platform=client_platform,
            revenue_type=revenue_type
        )
        if created:
            type_revenue_platform_mapping.revenue_percentage = revenue_percentage
            type_revenue_platform_mapping.is_active = True
            type_revenue_platform_mapping.receiver = receiver
            type_revenue_platform_mapping.save()
            logger.info(
                logme('revenueType and platform mapping successfully done', request)
            )
            return JsonResponse({'status':'success'}, status=200)
        else:
            logger.info(
                logme('failed, unable to map revenueType and platform', request)
            )
            return JsonResponse({'status':'invalid data, unable to map revenueType and platform'})
    else:
        logger.info(
            logme('failed, Invalid argument', request)
        )
        return JsonResponse({'status':'Invalid data, Given value not valid'})


def transaction(trans_info, revenue_info):
    '''
    Description : creating transaction records
    '''
    product_id = trans_info['product_id']
    trans_value = trans_info['trans_value']
    advisor_email = trans_info['advisor_email']
    client_email = trans_info['client_email']
    revenue_type = revenue_info['typ']
    platform_name = revenue_info['platform']
    revenue_source = revenue_info['revenue_from']
    pay_from = revenue_info['pay_from']
    pay_to = revenue_info['pay_to']
    parent_id = revenue_info['parent_id']
    user_profile = None
    service_advisor = None
    client_obj = None
    revenue_percentage = None
    revenue = None
    user_profile = UserProfile.objects.filter(email=advisor_email).first()
    if user_profile:
        service_advisor = Advisor.objects.filter(user_profile_id=user_profile.id).first()
    client_obj = ClientDetails.objects.filter(email=client_email).first()
    platform = ClientPlatform.objects.filter(platform_name=platform_name).first()
    revenue_type = RevenueType.objects.filter(revenue_name = revenue_type).first()
    if platform and revenue_type:
        revenue_platform = TypeRevenuePlatformMapping.objects.filter(
                platform=platform,
                revenue_type=revenue_type
        ).first()
        if revenue_platform and revenue_source:
            revenue_percentage = revenue_platform.revenue_percentage
            revenue = float(revenue_source) * (float(revenue_percentage)/float(100))

        transaction, created = RevenueTransactions.objects.get_or_create(
            product_id = product_id,
            transaction_value = trans_value,
            service_advisor = service_advisor,
            client = client_obj,
            pay_from = pay_from,
            pay_to = pay_to,
            source_revenue = revenue_source,
            revenue_in_percentage = revenue_percentage,
            revenue = revenue,
            revenue_platform = revenue_platform,
            parent_transaction_id = parent_id
        )
        if created:
            return transaction
        else:
            return None


def generate_payer_receiver(typ, plt_name, adv_mail):
    '''
    Description : Generate payer and receiver for tranaction
    '''
    holder = {}
    platform = ClientPlatform.objects.filter(platform_name=plt_name).first()
    if platform:
        holder['payer'] = platform.platform_email
    rev_typ = RevenueType.objects.filter(revenue_name=typ).first()
    if rev_typ and platform:
        rev_plt = TypeRevenuePlatformMapping.objects.filter(
            platform=platform,
            revenue_type=rev_typ
        ).first()
        if rev_plt.receiver.platform_email == constants.ADVISOR_GROUP:
            holder['receiver'] = adv_mail
        else:
            holder['receiver'] = rev_plt.receiver.platform_email
    return holder


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def revenue_transactions(request):
    '''
    Description:
        -> Getting service advisor object from advisor table using email through userprofile
            table
        -> Getting client object from clientDetails table using client_email
        -> Getting platform object by platform_name
        -> Getting revenue_type object by revenue_fee_type
        -> Type Revenue and PlatformMapping object by platform object and revenue_type 
            object
        -> Getting revenue percentage and revenue by Type Revenue and PlatformMapping 
            object
        -> Created Transaction by above value
    '''
    
    service_advisor = None
    client = None
    revenue_platform = None
    revenue_percentage = None
    revenue = None
    product_id = request.POST.get('product_id', None)
    advisor_email = request.POST.get('service_advisor_email', None)
    client_email = request.POST.get('client_email', None)
    platform_name = request.POST.get('platform_name', None)
    trans_value = request.POST.get('transaction_value', None)
    trasnaction_details = {}
    trasnaction_details['product_id'] = product_id
    trasnaction_details['advisor_email'] = advisor_email
    trasnaction_details['client_email'] = client_email
    trasnaction_details['platform_name'] = platform_name
    trasnaction_details['trans_value'] = trans_value
    revenue_details = {}
    
    # UPWRDZ_ADV_FEE 1% of transaction value
    typ = constants.TRANSACTION_MANAGEMENT_FEE
    plt_name = platform_name
    adv_mail = None
    holder = generate_payer_receiver(typ, plt_name, adv_mail)
    revenue_details['typ'] = typ
    revenue_details['platform'] = plt_name
    revenue_details['revenue_from'] = trans_value
    revenue_details['pay_from'] = holder['payer']
    revenue_details['pay_to'] = holder['receiver']
    revenue_details['parent_id'] = None 
    transaction_obj = transaction(trasnaction_details, revenue_details)
    if not transaction_obj:
        return JsonResponse({'status': 'duplicate'}, status=200)
    # FACILITATOR FEE  2% of transaction value
    typ = constants.FACILITATOR_FEE
    plt_name = constants.PLATFORM
    adv_mail = advisor_email
    holder = generate_payer_receiver(typ, plt_name, adv_mail)
    revenue_details['typ'] = typ
    revenue_details['platform'] = plt_name
    revenue_details['revenue_from'] = trans_value
    revenue_details['pay_from'] = holder['payer']
    revenue_details['pay_to'] = holder['receiver']
    revenue_details['parent_id'] = transaction_obj.id
    transaction(trasnaction_details, revenue_details)
    # Referral Transaction
    advisor_profile = UserProfile.objects.filter(email=advisor_email).first()
    if advisor_profile:
        reffer_advisor = UserProfile.objects.filter(
            user__id = advisor_profile.referred_by_id
        ).first()
        if reffer_advisor:
            typ1 = constants.TRX_LEAD_FEE
            refer_mail = reffer_advisor.email
            holder = generate_payer_receiver(typ1, plt_name, refer_mail)
            revenue_details['typ'] = typ1
            revenue_details['platform'] = plt_name
            revenue_details['revenue_from'] = transaction_obj.revenue
            revenue_details['pay_from'] = holder['payer']
            revenue_details['pay_to'] = holder['receiver']
            revenue_details['parent_id'] = transaction_obj.id
            transaction(trasnaction_details, revenue_details)
            # Transaciton manageger fee 5% of facilitator fee
            grand_refer_advisor = UserProfile.objects.filter(
                user__id = reffer_advisor.referred_by_id
            ).first()
            if grand_refer_advisor:
                typ2 = constants.TRX_MANAGER_FEE
                grand_refer_email = grand_refer_advisor.email
                holder = generate_payer_receiver(typ2, plt_name, grand_refer_email)
                revenue_details['typ'] = typ2
                revenue_details['platform'] = plt_name
                revenue_details['revenue_from'] = transaction_obj.revenue
                revenue_details['pay_from'] = holder['payer']
                revenue_details['pay_to'] = holder['receiver']
                revenue_details['parent_id'] = transaction_obj.id
                transaction(trasnaction_details, revenue_details)
            # Checking first transaction for 5% of facilitator fee
            advisor_obj = advisor_profile.advisor
            adv_trans_obj = RevenueTransactions.objects.filter(
                service_advisor = advisor_obj,
                parent_transaction_id = None
            )
            if len(adv_trans_obj) == constants.ADVISOR_FIRST_TRANSACTION:
                typ3 = constants.FIRST_TRX_BONUS_FEE
                holder = generate_payer_receiver(typ3, plt_name, refer_mail)
                revenue_details['typ'] = typ3
                revenue_details['platform'] = plt_name
                revenue_details['revenue_from'] = transaction_obj.revenue
                revenue_details['pay_from'] = holder['payer']
                revenue_details['pay_to'] = holder['receiver']
                revenue_details['parent_id'] = transaction_obj.id
                transaction(trasnaction_details, revenue_details)
    return JsonResponse({'status': 'success'}, status=200)


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def total_revenue(request):
    email = request.POST.get('email', None)
    if email:
        revenue_transactions = RevenueTransactions.objects.filter(
            Q(pay_from = email) | Q(pay_to = email)
        )
        total_revenue_transactions = None
        if revenue_transactions:
            serializer = RevenueTransactionsSerializer(revenue_transactions,many=True)
            total_revenue_transactions = serializer.data
            logger.info(
                logme('total revenue', request)
            )
        return JsonResponse({'total_revenue_transactions':total_revenue_transactions}, status=200)
    else:
        logger.info(
            logme('failed, email does not exist', request)
        )
        return JsonResponse({'status':'invalid data, email does not exist'})


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_advisor_transactions(request):
    '''
    Description: Getting service advisor transactions
    '''
    email = request.POST.get('email', None)
    if email:
        user_profile = UserProfile.objects.filter(email=email).first()
        if user_profile:
            revenue_transactions = RevenueTransactions.objects.filter(
                Q(pay_from = user_profile.advisor) | Q(pay_to = user_profile.advisor)
            )
            revenue_transactions_data = None
            data_obj = None
            total_payable = 0
            total_receivable = 0
            total_wallet = 0
            if revenue_transactions:
                serializer = RevenueTransactionsSerializer(
                    revenue_transactions, many=True)
                revenue_transactions_data = serializer.data
                logger.info(
                    logme('advisor transaction', request)
                )
                data = JSONEncoder().encode(revenue_transactions_data)
                data_obj = json.loads(data)
                for dt in data_obj:
                    dt['service_advisor'] = Advisor.objects.filter(
                        id = dt['service_advisor']).first().user_profile.email
                    dt['client'] = ClientDetails.objects.filter(
                        id = dt['client']).first().email
                    rev_map_obj = TypeRevenuePlatformMapping.objects.filter(
                        id = dt['revenue_platform']
                    ).first().revenue_type
                    dt['revenue_type'] = rev_map_obj.revenue_name
                    dt['wallet'] = rev_map_obj.is_wallet
                    if dt['pay_from'] == email:
                        dt['status'] = 'Payable'
                        total_payable = float(total_payable) + float(dt['revenue'])
                    if dt['pay_to'] == email:
                        dt['status'] = 'Receivable'
                        if rev_map_obj.is_wallet:
                            total_wallet = float(total_wallet) + float(dt['revenue'])
                        else:
                            total_receivable = float(total_receivable) + float(
                                                                            dt['revenue'])
            value = {
                'revenue_transactions_data':data_obj,
                'total_payable': total_payable,
                'total_receivable' : total_receivable,
                'total_wallet' : total_wallet
            }
            return JsonResponse(value, status=200)
        else:
            logger.info(
                logme('failed, advisor not found', request)
            )
            return JsonResponse({'status':'invalid data, advisor not found'})
    else:
        logger.info(
            logme('failed, user not exist', request)
        )
        return JsonResponse({'status':'invalid data, user not exist'})


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_certified_revenue(request):
    '''
    Description: for certified revenue transactions
    '''
    advisor_email = request.POST.get('advisor_email',None)
    fee = request.POST.get('fee',None)
    platform_name = constants.ADVISOR_GROUP
    main_revenue_type = constants.GET_CERTIFIED_REVENUE_FEE
    sub_revenue_type =constants.CERTIFIED_PROVIDER_FEE
    pay_from = advisor_email
    pay_to = common_constants.UPWRDZ_ADMIN_EMAIL
    rev_typ = TypeRevenuePlatformMapping.objects.filter(
        platform__platform_name=platform_name,
        revenue_type__revenue_name=main_revenue_type
    ).first()
    response = make_revenue_transactions(
        request,
        advisor_email,
        platform_name,
        fee,
        main_revenue_type,
        pay_from,
        pay_to,sub_revenue_type
    )
    return response


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_qualified_revenue(request):
    '''
    Description :for qualified revenue transactions
    '''
    advisor_email = request.POST.get('advisor_email',None)
    fee = request.POST.get('fee',None)
    platform_name = constants.ADVISOR_GROUP
    main_revenue_type = constants.GET_QUALIFIED_REVENUE_FEE
    sub_revenue_type =constants.QUALIFIED_PROVIDER_FEE
    pay_from = advisor_email
    pay_to = common_constants.UPWRDZ_ADMIN_EMAIL
    rev_typ = TypeRevenuePlatformMapping.objects.filter(
        platform__platform_name=platform_name,
        revenue_type__revenue_name=main_revenue_type
    ).first()
    response = make_revenue_transactions(
        request,
        advisor_email,
        platform_name,
        fee,
        main_revenue_type,
        pay_from,
        pay_to,
        sub_revenue_type
    )
    return response


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_connected_revenue_fee(request):
    '''
    Description : for connected revenue fee transactions
    '''
    advisor_email = request.POST.get('advisor_email',None)
    fee = request.POST.get('fee',None)
    platform_name = constants.ADVISOR_GROUP
    main_revenue_type = constants.GET_CONNECTED_REVENUE_FEE
    sub_revenue_type =None
    pay_from = advisor_email
    pay_to = common_constants.UPWRDZ_ADMIN_EMAIL
    rev_typ = TypeRevenuePlatformMapping.objects.filter(
        platform__platform_name=platform_name,
        revenue_type__revenue_name=main_revenue_type
    ).first()
    response = make_revenue_transactions(
        request,
        advisor_email,
        platform_name,
        fee,
        main_revenue_type,
        pay_from,
        pay_to,
        sub_revenue_type
    )
    return response


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_listing_revenue_fee(request):
    '''
    Description : for listing revenue fee transactions
    '''
    advisor_email = request.POST.get('advisor_email',None)
    fee = request.POST.get('fee',None)
    platform_name = constants.ADVISOR_GROUP
    main_revenue_type = constants.LISTING_REVENUE_FEE
    sub_revenue_type =None
    pay_from = advisor_email
    pay_to = common_constants.UPWRDZ_ADMIN_EMAIL
    rev_typ = TypeRevenuePlatformMapping.objects.filter(
        platform__platform_name=platform_name,
        revenue_type__revenue_name=main_revenue_type
    ).first()
    response = make_revenue_transactions(
        request,
        advisor_email,
        platform_name,
        fee,
        main_revenue_type,
        pay_from,
        pay_to,
        sub_revenue_type
    )
    return response


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_facilitation_revenue_fee(request):
    '''
    Description : for facilitation revenue fee transactions
    '''
    advisor_email = request.POST.get('advisor_email',None)
    fee = request.POST.get('fee',None)
    platform_name = constants.ADVISOR_GROUP
    main_revenue_type = constants.FACILITATION_REVENUE_FEE
    sub_revenue_type =None
    pay_from = advisor_email
    pay_to = common_constants.UPWRDZ_ADMIN_EMAIL
    rev_typ = TypeRevenuePlatformMapping.objects.filter(
        platform__platform_name=platform_name,
        revenue_type__revenue_name=main_revenue_type
    ).first()
    response = make_revenue_transactions(
        request,
        advisor_email,
        platform_name,
        fee,
        main_revenue_type,
        pay_from,
        pay_to,
        sub_revenue_type
    )
    return response


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_product_education_fee(request):
    '''
    Description : for product education fee transactions
    '''
    advisor_email = request.POST.get('advisor_email',None)
    fee = request.POST.get('fee',None)
    platform_name = constants.ADVISOR_GROUP
    main_revenue_type = constants.PRODUCT_EDUCATION_REVENUE_FEE
    sub_revenue_type =constants.PRODUCT_EDUCATION_PROVIDER_FEE
    pay_from = advisor_email
    pay_to = common_constants.UPWRDZ_ADMIN_EMAIL
    rev_typ = TypeRevenuePlatformMapping.objects.filter(
        platform__platform_name=platform_name,
        revenue_type__revenue_name=main_revenue_type
    ).first()
    response = make_revenue_transactions(
        request,
        advisor_email,
        platform_name,
        fee,
        main_revenue_type,
        pay_from,
        pay_to,
        sub_revenue_type
    )
    return response


def make_revenue_transactions(request,advisor_email,platform_name,fee,main_revenue_type,
                                pay_from,pay_to,sub_revenue_type):
    '''
    Description : for making revenue transactions
    '''
    trasnaction_details = {}
    trasnaction_details['product_id'] = None
    trasnaction_details['advisor_email'] = advisor_email
    trasnaction_details['client_email'] = None
    trasnaction_details['platform_name'] = platform_name
    trasnaction_details['trans_value'] = fee
    revenue_details = {}
    revenue_details['typ'] = main_revenue_type
    revenue_details['platform'] = platform_name
    revenue_details['revenue_from'] = fee
    revenue_details['pay_from'] = pay_from
    revenue_details['pay_to'] = pay_to
    revenue_details['parent_id'] = None
    transaction_obj = transaction(trasnaction_details, revenue_details)
    if transaction_obj:
        if sub_revenue_type!=None:
            rev_typ1 = TypeRevenuePlatformMapping.objects.filter(
                platform__platform_name=constants.PLATFORM,
                revenue_type__revenue_name=sub_revenue_type
            ).first()
            percentage = float(rev_typ1.revenue_percentage)
            revenue = float(transaction_obj.revenue) * float(percentage/100)
            revenue_details = {}
            revenue_details['typ'] = sub_revenue_type
            revenue_details['platform'] = constants.PLATFORM
            revenue_details['revenue_from'] = transaction_obj.revenue
            revenue_details['pay_from'] = "admin@upwrds.com"
            revenue_details['pay_to'] = rev_typ1.receiver.platform_email
            revenue_details['parent_id'] = transaction_obj.id
            transaction(trasnaction_details, revenue_details)
            logger.info(
                logme('created revenue transactions',request)
            )
            return JsonResponse({'data':'success'},status=200)
        else:
            logger.info(
                    logme('created revenue transactions',request)
                )
            return JsonResponse({'data':'success'},status=200)
    else:
        logger.info(
            logme('failed, unable to create revenue transactions',request)
        )
        return JsonResponse({
            'data':'invalid data, unable to create revenue transactions'})
