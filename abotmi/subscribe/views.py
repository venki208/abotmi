# python lib
import datetime
import json
import logging

# Django lib
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

# Database models
from datacenter.models import (AdvisorSubscriptionPackageOrder, SubscriptionPackageMaster,
    MicroLearningVideoPkg, FeatureSubscriptionPkgMapping, FeatureListMaster,
    AllTransactionsDetails, SubscriptionCategoryMaster, ProfileShareMapping, UserProfile,
    MyWallet)

# Constants
from common import constants as common_constants
from subscribe import constants, sub_common_functions

# Local imports
from common.payment import Payment
from common.views import logme, customize_sorted_list
from mywallet.views import Wallet
from subscribe.sub_common_functions import generate_unique_reference_key

logger = logging.getLogger(__name__)


def index(request):
    """
    Steps: Display subscription package to activate
    """
    if request.method == 'GET':
        user = request.user
        activated_pack_obj = AdvisorSubscriptionPackageOrder.objects.filter(
            user_profile=user.profile,
            subscription_status=constants.ACTIVATED
        ).first()
        if activated_pack_obj:
            pack = activated_pack_obj.subscription_type.package_code
        return render(request, 'subscribe/subscription_package_view.html', locals())


def activate_package(request):
    '''
    Activating the Package
    '''
    if request.method == 'POST':
        pack = None
        package_code = request.POST['package']
        user = request.user
        master_pack_obj = SubscriptionPackageMaster.objects.filter(
            package_code=package_code
        ).first()
        activated_pack_obj = AdvisorSubscriptionPackageOrder.objects.filter(
            user_profile=user.profile,
            subscription_type__package_name=master_pack_obj.package_name,
            subscription_status=constants.ACTIVATED
        ).first()
        if activated_pack_obj:
            activated_pack_obj.subscription_status = constants.DEACTIVATED
            activated_pack_obj.save()
        order, created = AdvisorSubscriptionPackageOrder.objects.get_or_create(
            user_profile=user.profile,
            subscription_type=master_pack_obj,
            subscription_value=master_pack_obj.package_amount
        )
        if created:
            order.subscription_status = constants.ACTIVATED
        order.save()
        return HttpResponse("success", status=200)
    if request.method == 'GET':
        return HttpResponse("Acces forbidden", status=405)


def subscribe_package_order(request):
    """
    Description : To store order detials and requesting payment page on click of subscribe
        button in AdvisorSubscriptionTable
    """
    if request.method == 'POST':
        pkg_type = request.POST.get("pkg_type",None)
        sub_cat_id = request.POST.get("sub_cat_id",None)
        wallet = request.POST.get("wallet", 0)

        if pkg_type and sub_cat_id:
            unique_reference_key = generate_unique_reference_key()
            sub_pkg_master = SubscriptionPackageMaster.objects.filter(
                package_type=pkg_type,
                subscription_category=sub_cat_id
            ).first()
            # Checking micro learning pack
            if (sub_pkg_master.subscription_category.category_name == 
                constants.SUB_CAT_MICRO_LEARNING_PACK):
                adv_sub_pkg_order_created = AdvisorSubscriptionPackageOrder.objects.create(
                    user_profile=request.user.profile,
                    subscription_type=sub_pkg_master,
                    subscription_value=sub_pkg_master.package_amount,
                    subscription_status = constants.DEACTIVATED,
                    payment_status = constants.PAYMENT_PENDING,
                    unique_reference_key = unique_reference_key
                )
            # Checking identity pack
            elif (sub_pkg_master.subscription_category.category_name == 
                constants.SUB_CAT_IDENTITY_PACK):
                advisor_package_order_exists = AdvisorSubscriptionPackageOrder.objects.filter(
                    user_profile=request.user.profile,
                    subscription_type=sub_pkg_master,
                    subscription_status = constants.ACTIVATED
                ).first()
                if advisor_package_order_exists:
                    return HttpResponse("Already Activated", status=200)
                else:
                    adv_sub_pkg_order_created = \
                        AdvisorSubscriptionPackageOrder.objects.create(
                            user_profile=request.user.profile,
                            subscription_type=sub_pkg_master,
                            subscription_value=sub_pkg_master.package_amount,
                            unique_reference_key = unique_reference_key,
                            payment_status = constants.PAYMENT_PENDING,
                            subscription_status = constants.DEACTIVATED
                        )
            if adv_sub_pkg_order_created:
                payment_details = {
                    'order_id':adv_sub_pkg_order_created.id,
                    'transaction_value':float(sub_pkg_master.package_amount)-float(wallet),
                    'package_type':sub_pkg_master.package_type,
                    'transaction_type':common_constants.TR_TYPE_ONLINE,
                    'status':constants.PAYMENT_PENDING,
                    'service_type':constants.SERVICE_TYPE,
                    'unique_reference_key':unique_reference_key,
                    'category_name': sub_pkg_master.subscription_category.category_name
                }
                payment = Payment()
                paid_status, payment_obj = payment.payment_transaction(
                    payment_details, request)
                if paid_status:
                    return render(request, 'dashboard/online_payment.html', locals())
                else:
                    return HttpResponse("Transaction is failure", status=200)
        else:
            return HttpResponse('Data is not passed properly.', status=200)


@csrf_exempt
def subscribe_package_payment_success(request):
    '''
    Description : subscribe package payment response message handling
    '''
    if request.method == 'POST':
        payment_status = request.POST.get('ResponseMessage', None)
        unique_reference_key = request.POST.get('MerchantRefNo', None)
        if payment_status == constants.PAYMENT_COMPLETED:
            if unique_reference_key:
                status_code = 200
                adv_sub_pkg_order = AdvisorSubscriptionPackageOrder.objects.filter(
                    unique_reference_key=unique_reference_key
                ).first()
                all_transaction_details = AllTransactionsDetails.objects.filter(
                    unique_reference_key=unique_reference_key
                ).first()
                if adv_sub_pkg_order and all_transaction_details:
                    adv_sub_pkg_order.payment_status = constants.PAYMENT_COMPLETED
                    adv_sub_pkg_order.subscription_status = constants.ACTIVATED
                    adv_sub_pkg_order.save()
                    all_transaction_details.status = constants.PAYMENT_COMPLETED
                    all_transaction_details.payment_response = json.dumps(request.POST)
                    all_transaction_details.save()
                    no_of_videos = json.loads(
                        adv_sub_pkg_order.subscription_type.feature_data
                    ).get('no_of_videos',0)
                    if no_of_videos:
                        ml_video_pkg = MicroLearningVideoPkg.objects.create(
                            advisor_subscription_pkg=adv_sub_pkg_order,
                            video_count = no_of_videos
                        )
                    payment_status_code = 200
                    payment_result_data = 'Payment Completed successfully.'
                    refered_profile = request.user.profile.referred_by
                    reffer_u_p = refered_profile.profile if refered_profile else None
                    if reffer_u_p:
                        wallet = Wallet()
                        wallet.addWalletMoney(
                            reffer_u_p,
                            adv_sub_pkg_order.subscription_type.package_amount, all_transaction_details
                        )
                else:
                    payment_status_code = 400
                    payment_result_data = 'Unique data is missing'
            else:
                payment_status_code = 400
                payment_result_data = 'MerchantRefNo is not found.'
        else:
            payment_status_code = 400
            payment_result_data = 'Payment failed.'
    else:
        payment_status_code = 400
        payment_result_data = 'Payment failed. Method not allowed'
    return render(request, "dashboard/dashboard.html", locals())


class IdentityPack(View):
    '''
    Definition: Identity Pack Class
    GET:
        -> which helps to get all identity package with features and their respetive value
    '''

    def get(self, request, *args, **kwargs):
        category_obj = SubscriptionCategoryMaster.objects.filter(
            category_name=constants.SUB_CAT_IDENTITY_PACK
        ).first()
        package = SubscriptionPackageMaster.objects.filter(
            subscription_category = category_obj
        )
        package_data = {}
        activated_package = None
        for pkg in package:
            package_data[pkg.package_type] = json.loads(pkg.feature_data)
        activated_pack_obj = AdvisorSubscriptionPackageOrder.objects.filter(
            user_profile=request.user.profile,
            subscription_type__in = package,
            subscription_status = constants.ACTIVATED
        ).first()
        if activated_pack_obj:
            activated_package = activated_pack_obj.subscription_type.package_type
        feature_list = constants.FEATURE_ORDET_LIST
        package_data = sub_common_functions.get_dict_order_as_required(package_data)
        return render(request, 'subscribe/subscription_package_view.html', locals())


def profile_viewed_details(request):
    '''
    Getting Viewed Advisor profile list
    '''
    if request.method == 'GET':
        member_list = []
        user_profile = request.user.profile
        # check Activate pack
        viewed_obj = ProfileShareMapping.objects.filter(
            advisor = user_profile.advisor
        ).values('viewed_user_profile')
        member_profile_obj = UserProfile.objects.filter(id__in = viewed_obj)
        member_list = [{'pid': mem.id, 'member_name': str(
            mem.first_name + " " + mem.last_name)} for mem in member_profile_obj]
        logger.info(
            logme("Open viewed profile detials",request)
        )
        return render(request, "subscribe/profile_viewed_details.html", locals())


def memeber_data(pid, package, feature):
    """
    """
    member_profile = {}
    member_profile['Package'] = package
    member_obj = UserProfile.objects.filter(id=pid).first()
    #  name
    if feature['name'] == "True":
        if member_obj.first_name or member_obj.last_name:
            member_profile['Name'] = member_obj.first_name+" "+member_obj.last_name
        else:
            member_profile['Name'] = constants.DATA_NOT_AVAILABLE
    else:
        member_profile['Name'] = constants.UPGRADE_TO_REVEAL

    # Email
    if feature['email'] == "True":
        if member_obj.email:
            member_profile['Email'] = member_obj.email
        else:
            member_profile['Email'] = constants.DATA_NOT_AVAILABLE
    else:
        member_profile['Email'] = constants.UPGRADE_TO_REVEAL
        
    # Mobile
    if feature['contact_number'] == "True":
        if member_obj.mobile:
            member_profile['Mobile'] = member_obj.mobile
        else:
            member_profile['Mobile'] = constants.DATA_NOT_AVAILABLE
    else:
        member_profile['Mobile'] = constants.UPGRADE_TO_REVEAL

    # Last visited 
    if feature['when_they_visit'] == "True":
        share_obj = ProfileShareMapping.objects.filter(
            viewed_user_profile_id = pid).order_by('-modified_date').first()
        if share_obj.modified_date:
            member_profile['Last visited'] = share_obj.modified_date
        else: 
            member_profile['Last visited'] = constants.DATA_NOT_AVAILABLE
    else:
        member_profile['Last visited'] = constants.UPGRADE_TO_REVEAL
        
    # Social Media Link
    if feature['social_media_link'] == "True":
        member_profile['Social Media Link'] = constants.DATA_NOT_AVAILABLE
    else:
        member_profile['Social Media Link'] = constants.UPGRADE_TO_REVEAL
    
    # Location 
    if feature['location'] == "True":
        if member_obj.locality:
            member_profile['Location'] = member_obj.locality
        else:
            member_profile['Location'] = constants.DATA_NOT_AVAILABLE
    else:
        member_profile['Location'] = constants.UPGRADE_TO_REVEAL

    # viewer status
    if feature['viewer_registrations_status'] == "True":
        member_profile['Viewer Registrations Status'] = constants.DATA_NOT_AVAILABLE
    else:
        member_profile['Viewer Registrations Status'] = constants.UPGRADE_TO_REVEAL

    # purpsoe of visit
    if feature['pupose_of_visit'] == "True":
        member_profile['Purpose Of Visit'] = constants.DATA_NOT_AVAILABLE
    else:
        member_profile['Purpose Of Visit'] = constants.UPGRADE_TO_REVEAL
    
    # real time notificaiton
    if feature['real_time_notification'] == "True":
        member_profile['Real Time Notification'] = constants.DATA_NOT_AVAILABLE
    else:
        member_profile['Real Time Notification'] = constants.UPGRADE_TO_REVEAL

    # social graph
    if feature['social_graph'] == "True":
        member_profile['Social Graph'] = constants.DATA_NOT_AVAILABLE
    else:
        member_profile['Social Graph'] = constants.UPGRADE_TO_REVEAL
    
    # behavioural graph
    if feature['behavioural_graph'] == "True":
        member_profile['Behavioural Graph'] = constants.DATA_NOT_AVAILABLE
    else:
        member_profile['Behavioural Graph'] = constants.UPGRADE_TO_REVEAL
    member_profile = customize_sorted_list(member_profile, constants.ACTIVATED_KEYORDER)
    return member_profile


def get_member_details_by_id(request):
    """
    Get memeber detials by id based on package activation
    """
    if request.method == 'POST':
        user_profile = request.user.profile
        activated_package = None
        criteria = []
        pid = request.POST.get('pid', None)
        
        activated_obj = AdvisorSubscriptionPackageOrder.objects.filter(
            user_profile = user_profile,
            subscription_status = constants.ACTIVATED,
            subscription_type__subscription_category__category_name = \
                constants.SUB_CAT_IDENTITY_PACK
        ).select_related('subscription_type').first() 
        if activated_obj:
            activated_package = activated_obj.subscription_type.feature_data
            feature = json.loads(activated_package)

        checked_user = []
        if activated_obj.current_package_criteria:
            criteria = json.loads(activated_obj.current_package_criteria)
            checked_user = criteria['checked_user']
            activated_date = criteria['activated_date']
            if str(datetime.datetime.now().date()) != activated_date:
                activated_obj.current_package_criteria = ''
                activated_obj.save()

        if pid:
            if feature['number_of_viewer_details'] != "ALL":
                num_user = int(feature['number_of_viewer_details'])
            else:
                num_user = ProfileShareMapping.objects.filter(
                    advisor = user_profile.advisor
                ).values("viewed_user_profile").distinct().count()

            criteria_dict = {}
            if int(pid) not in checked_user:
                if num_user != len(checked_user):
                    checked_user.append(int(pid))
                    criteria_dict['checked_user'] = checked_user
                    criteria_dict['activated_date'] = str(datetime.datetime.now().date())
                    activated_obj.current_package_criteria = json.dumps(criteria_dict)
                    activated_obj.save()
                    member_profile = memeber_data(
                        pid, activated_obj.subscription_type.package_type, feature)
                    return HttpResponse(member_profile)
                else:
                    return HttpResponse("Not Access")
            else:
                member_profile = memeber_data(
                    pid, activated_obj.subscription_type.package_type, feature)
                return HttpResponse(member_profile)
        else:
            return HttpResponse('parameter missing', status=400)


def payment_summary_details(request):
    '''
    Getting Payment summery details of Subscribed Package
    '''
    if request.method == 'POST':
        pkg_code = None
        pkg_type = None
        pkg_amount = None
        wlt_money = 0
        wlt_name = None
        user_profile = request.user.profile
        pkg_type = request.POST.get("pkg_type",None)
        sub_cat_id = request.POST.get("sub_cat_id",None)
        sub_pkg_master = SubscriptionPackageMaster.objects.filter(
                package_type=pkg_type,
                subscription_category=sub_cat_id
        ).first()
        if sub_pkg_master:
            pkg_code = sub_pkg_master.package_code
            pkg_type = sub_pkg_master.package_type
            pkg_amount = sub_pkg_master.package_amount
            wallet_obj = MyWallet.objects.filter(user_profile = user_profile).first()
            if wallet_obj:
                wlt_name = wallet_obj.wallet_name
                wlt_money = wallet_obj.total_wallet
    return render(request, 'revenue/payment_summary_view.html', locals())
