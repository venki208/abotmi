# Python lib
import base64
import datetime
import hashlib
import json
import logging
import requests

# Django Modules
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import default_storage
from django.db.models import Avg, Q, Sum, F
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import RequestContext
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from datetime import date
from num2words import num2words
# Database Models
from datacenter.models import (
    UserProfile, EmailVerification, UserReferral, NoticeBoard, ExternalUser,
    AdvisorRating, Member, Advisor, TrackReferrals, ReferralPoints, UploadDocuments,
    Country, TransactionsDetails, PromoCodes, GroupMaster, GroupMembers,
    CrisilCertifications, TrackWebinar, AdvisorVideoRequest, RevenueTransactions,
    AdvisorPublishedVideo, ClientDetails, ClientPlatform, ClientAdvisorMapping,
    MicroLearningVideoPkg, ActivityFollowers, AdvisorSubscriptionPackageOrder,
    ProfileShareMapping, AdvChkProfileConnectMap
)
# Local Imports
# Common app modules
from common import constants, api_constants
from common.notification.constants import (
    ADVISOR_FOLLOWING, ADVISOR_REJECTED, VIDEO_UPLOAD_SUCCESS, RANK_REQ, RATE_REQ
)
from common.views import (
    invoice_gen, auth_token, get_all_members, get_invited_members, client_enquiry,
    check_user_uplyf, logme, list_client_enquiry,
    upload_reingo_transaction_document, get_sms_status, invoice_bill_pdf,
    get_all_client, get_ipinfo, get_ip_region
)
from common.utils import (
    generate_key, send_sms_alert, calculate_discount_amount,
    calculate_tax_amount, calculate_certificate_value,
    calculate_final_amount_with_discount_and_tax_amount
)

# Local Imports
from common.notification.views import NotificationFunctions
from dashboard.forms import PaymentForm
from dashboard.serializers import TrackReferralsSerializer
from login.decorators import check_role_and_redirect
from signup.djmail import (
    send_mandrill_email, send_mandrill_email_with_attachement,
    send_mandrill_email_admin
)
from subscribe.sub_common_functions import get_pkg_list_by_type
from subscribe import constants as sub_constant
from wpb.views import get_all_wpb_course

# Rest Framework
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

# Third party modules
from boto.s3.connection import S3Connection
from boto.s3.key import Key

logger = logging.getLogger(__name__)


def index(request):
    '''
    This is the dashboard view, it returns noticeboard messages,
    forms for add member, invite advisor, request advisor to rate.
    rating and ranking counts, enquiry management, stream course details
    ICORE blog data.
    '''
    req_type = request.POST.get('req_type', None)
    user = request.user
    user_profile = user.profile
    advisor = user_profile.advisor
    title = constants.MY_HUB
    wpb_url = constants.WPB_URL
    if advisor.is_register_advisor:
        user_profile.login_count += 1
        # crisil_app_status = advisor.crisil_application_status
        notice = NoticeBoard.objects.all()
        notices = notice.filter(news_type="notice")
        news_content = notice.filter(news_type="news")
        # Member Deatils from UPLYF
        members = None  # get_all_members(user_profile.email)
        total_members_count = 0
        registered_members_count = 0
        un_registered_members_count = 0
        if members:
            total_members_count = len(members['content'])
            registered_members_count = members['members_registered_count']
            un_registered_members_count = total_members_count-registered_members_count
        # Enquiry management
        total_enquiries, enquiry_management_accepted = 0, 0,
        enquiry_management_rejected, enquiry_management_inprogress = 0, 0
        members_data = None
        # members_data = client_enquiry(
        #     user_profile.first_name+" "+user_profile.last_name,
        #     advisor.id,
        #     user_profile.email
        # )
        if members_data:
            enquiry_management_accepted = members_data['reingo_booking_accepted']
            enquiry_management_rejected = members_data['reingo_booking_rejected']
            enquiry_management_inprogress = members_data['reingo_booking_inprogress']
            total_enquiries = enquiry_management_accepted\
                + enquiry_management_rejected + enquiry_management_inprogress
        # Earnings
        # revenue_transactions = RevenueTransactions.objects.filter(
        #     pay_to = user_profile.email)
        total_advisor_earning = 0
        total_referral_earning = 0
        total_earnings = 0
        revenue_transactions = None
        if revenue_transactions:
            advisor_earning = revenue_transactions.filter(
                revenue_platform__revenue_type__revenue_name__in=[
                    'FACILITATOR_FEE',
                    'BY_CLI_ADV_FEE'
                ]).values('revenue')
            if advisor_earning:
                total_advisor_earning = ("%.0f" % advisor_earning.aggregate(
                    Sum('revenue'))['revenue__sum'])
            referral_earning = revenue_transactions.filter(
                revenue_platform__revenue_type__revenue_name__in=[
                    'TRX_MANAGER_FEE',
                    'SEQUENCE_TRX_MANAGER_CERTIFY_FEE',
                    'SEQUENCE_TRX_MANAGER_UNCERTIFY_FEE',
                    'TRX_MANAGER_FEE_G', 'SEQUENCE_TRX_MANAGER_CERTIFY_FEE_G',
                    'SEQUENCE_TRX_MANAGER_UNCERTIFY_FEE_G']
            ).values('revenue')
            if referral_earning:
                total_referral_earning = ("%.0f" % referral_earning.aggregate(
                    Sum('revenue'))['revenue__sum'])
        # total_earnings =int(total_advisor_earning) + int(total_referral_earning)

        # Profile picture
        if user_profile.picture:
            profile_pic = user_profile.picture.url
        # Rating and Ranking
        member_rating = 0.0
        peer_rating = 0.0
        total_advisor_rates = 0
        total_member_ranks = 0
        # Rating by advisors
        advisor_rate_invites = AdvisorRating.objects.filter(
            advisor=advisor
        )
        if advisor_rate_invites:
            rating_by_advisor = advisor_rate_invites.filter(user_type='advisor')
            rating_by_member = advisor_rate_invites.filter(user_type='Member')
            if rating_by_advisor:
                total_advisor_rates = rating_by_advisor.count()
                rated_invites = rating_by_advisor.exclude(
                    avg_rating__lte=0.0).count()
                peer_rating = rating_by_advisor.exclude(
                    avg_rating__lte=0.0).aggregate(
                    Avg('avg_rating'))['avg_rating__avg']
            # Rating by Member
            if rating_by_member:
                total_member_ranks = rating_by_member.count()
                ranked_invites = rating_by_member.exclude(
                    avg_rating__lte=0.0).count()
                member_rating = rating_by_member.exclude(
                    avg_rating__lte=0.0).aggregate(Avg('avg_rating'))['avg_rating__avg']
            # End Rating by Member
        user_obj = request.user
        all_wpb_course = None
        get_all_wpb_course_data = None
        get_all_wpb_course_message = None
        get_all_wpb_course_json = {}
        try:
            all_wpb_course = get_all_wpb_course(request, user_obj)
            if all_wpb_course:
                get_all_wpb_course_data = all_wpb_course['data']
                get_all_wpb_course_message = all_wpb_course['message']
            if get_all_wpb_course_message == 'already_exist':
                ico_status = None
                crypto_status = None
                ico_courses = []
                crypto_courses = []
                crypto_obj = get_all_wpb_course_data['crypto_obj']
                ico_obj = get_all_wpb_course_data['ico_obj']
                # Resourse study status
                if constants.STUDY_INPROGRESS in crypto_obj:
                    crypto_courses.append(crypto_obj[constants.STUDY_INPROGRESS])
                    crypto_status = "in_progress"
                else:
                    if (constants.STUDY_NEXT in crypto_obj) and (
                            crypto_obj[constants.STUDY_NEXT] not in crypto_courses):
                                crypto_courses.append(crypto_obj[constants.STUDY_NEXT])
                if constants.STUDY_INPROGRESS in ico_obj:
                    ico_courses.append(ico_obj[constants.STUDY_INPROGRESS])
                    ico_status = "in_progress"
                else:
                    if (constants.STUDY_NEXT in ico_obj) and (
                            ico_obj[constants.STUDY_NEXT] not in ico_courses):
                                ico_courses.append(ico_obj[constants.STUDY_NEXT])
                get_all_wpb_course_json['crypto_courses'] = crypto_courses
                get_all_wpb_course_json['ico_courses'] = ico_courses
                get_all_wpb_course_json['crypto_status'] = crypto_status
                get_all_wpb_course_json['ico_status'] = ico_status
            else:
                get_all_wpb_course_json = get_all_wpb_course_data
        except Exception as e:
            logger.error(
                logme('WPB Error:{}'.format(e), request)
            )
            pass
        # Advisor Referral Modal
        total_reffered_advisor_count = TrackReferrals.objects.filter(
            referred_by=user_profile
        ).count()
        referred_register_advisor_count = Advisor.objects.filter(
            is_register_advisor=True,
            user_profile__referred_by=user
        ).count()
        if total_reffered_advisor_count:
            referred_unregister_advisor_count = total_reffered_advisor_count \
                - referred_register_advisor_count
        else:
            total_reffered_advisor_count = referred_register_advisor_count
            referred_unregister_advisor_count = 0

        referral_points = 0
        referral_points = ReferralPoints.objects.filter(beneficiary_id=user_profile)
        if referral_points:
            referral_points = referral_points.first()
            referral_points = referral_points.points
        total_icore_posts = None
        token_obj_all = None
        # ip_details gets advisor's country
        user_agent_country = get_ip_region(request)
        no_of_years_selected = ''
        payment_status = ''
        transaction_object = TransactionsDetails.objects.filter(
            user_profile=user_profile).first()
        if transaction_object:
            description = json.loads(transaction_object.description)
            no_of_years_selected = int(description['no_of_years_selected']) \
                + int(description['offered_years'])
            payment_status = transaction_object.status
        # Fetching promocode from promocode table
        # promocode = PromoCodes.objects.filter(user_profile = user_profile)
        # if promocode:
        #     promocode = promocode[0]
        # if 'apply_for_crisil' in request.session:
        #     if request.session['apply_for_crisil']:
        #         apply_for_crisil = 1
        #         del request.session['apply_for_crisil']
        # Calculating days left for crisil certificate
        # crisil_days_left = None
        # if advisor.crisil_expiry_date:
        #     crisil_days_left = advisor.crisil_expiry_date - datetime.date.today()
        #     crisil_days_left = int(crisil_days_left.days)
        # Showing upcoming webinar activity
        # list_of_webinars = TrackWebinar.objects.filter(user_profile = user_profile)
        # Checking Advisor is Subscribed Identity Pack
        # sub_pkgs = AdvisorSubscriptionPackageOrder.objects.filter(
        #     user_profile = user_profile,
        #     subscription_status = sub_constant.ACTIVATED
        # )
        user.save()
        user_profile.save()
        advisor.save()
        views_profile = ProfileShareMapping.objects.filter(
            advisor=user_profile.advisor,
            viewed_page=constants.MY_IDENTITY
        ).values('viewed_user_profile').count()
        ad_chk_view_profile = AdvChkProfileConnectMap.objects.filter(
            action_type='view',
            email=user_profile.email
        ).values_list('user_profile').count()
        profile_view_count = views_profile + ad_chk_view_profile
        connect_profile_count = AdvChkProfileConnectMap.objects.filter(
            email=user_profile.email, action_type='connect').values('id').count()
        # Checking the user's account in UPLYF
        # user_status = check_user_uplyf(user_profile.email)
        # if user_status:
        #     user_status = user_status['user_status']
        uplyf_server_name = api_constants.UPLYF_USER_LOGIN
        email_from_aadhaar = None
        is_kyc_success = None
        is_adhaar_no_invalid = None
        is_ekyc_verified_data_present = None
        aadhaar_mobile = None
        if "is_ekyc_verified_data_present" in request.session:
            if request.session['is_ekyc_verified_data_present']:
                is_ekyc_verified_data_present = request.session[
                    'is_ekyc_verified_data_present']
        if "aadhaar_mobile" in request.session:
            if request.session['aadhaar_mobile']:
                aadhaar_mobile = request.session['aadhaar_mobile']
                del request.session['aadhaar_mobile']
        if "email_from_aadhaar" in request.session:
            if request.session['email_from_aadhaar']:
                email_from_aadhaar = request.session['email_from_aadhaar']
                del request.session['email_from_aadhaar']
        if "is_kyc_success" in request.session:
            is_kyc_success = request.session['is_kyc_success']
            del request.session['is_kyc_success']
        if "is_adhaar_no_invalid" in request.session:
            if request.session['is_adhaar_no_invalid']:
                is_adhaar_no_invalid = request.session['is_adhaar_no_invalid']
                del request.session['is_adhaar_no_invalid']
        if req_type == "mobile":
            enquired_members_data_present = 0
            enquired_members_data = list_client_enquiry(
                user_profile.first_name+" "+user_profile.last_name,
                advisor.id,
                user_profile.email
            )
            if enquired_members_data:
                enquired_members_data_present = enquired_members_data['content']
            data = {
                'total_members_count': total_members_count,
                'registered_members_count': registered_members_count,
                'un_registered_members_count': un_registered_members_count,
                'total_enquiries': total_enquiries,
                'enquiry_management_inprogress': enquiry_management_inprogress,
                'enquiry_management_accepted': enquiry_management_accepted,
                'enquiry_management_rejected': enquiry_management_rejected,
                'peer_rating': peer_rating,
                'member_rating': member_rating,
                'total_reffered_advisor_count': total_reffered_advisor_count,
                'total_icore_posts': total_icore_posts,
                'icore_posts': token_obj_all,
                'no_of_years_selected': no_of_years_selected,
                'referred_register_advisor_count': referred_register_advisor_count,
                'referred_unregister_advisor_count': referred_unregister_advisor_count,
                'loop_points': user_profile.total_points,
                'total_advisor_rates': total_advisor_rates,
                'total_member_ranks': total_member_ranks,
                'enquired_members_data_present': enquired_members_data_present,
                'total_advisor_earning': total_advisor_earning,
                'total_referral_earning': total_referral_earning,
                'total_earnings': total_earnings
            }
            return data
        else:
            logger.info(
                logme('dashboard page rendered', request)
            )
            return render(request, "dashboard/dashboard.html", locals())
    else:
        logger.info(
            logme("advisor not registered", request)
        )
        return HttpResponse(
            'You are not Register Advisor' +
            '<a href="/signup/face_capture/">click here</a>to become Register Advisor')


def view_member(request):
    '''
    Description :  View member displays member's details on click.
    '''
    if request.method == "GET":
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
            logme("member modal view opened", request)
        )
        return render(request, "dashboard/view_member_modal.html", locals())


def project_details(request):
    '''
    Description : This function gets all project details from UPLYF to the dashboard.
    '''
    if request.method == "GET":
        token = auth_token(settings.UPLYF_USER_NAME, settings.UPLYF_PASSWORD)
        headers = {'Authorization': 'JWT %s' % token['token']}
        project_details = requests.get(
            api_constants.UPLYF_PROJECT_DETAILS,
            headers=headers,
            verify=constants.SSL_VERIFY
        )
        project_detail = json.loads(project_details.content)
        logger.info(
            logme("returned all project details from UPLYF to the dashboard", request)
        )
        return render(request, "dashboard/project_details.html", locals())


def view_loop(request):
    '''
    Description: This opens the pop up containing looped user's details
    '''
    if request.method == "POST":
        req_type = request.POST.get('req_type', None)
        track_referrals = TrackReferrals.objects.filter(
            referred_by_id=request.user.profile)
        serializer = TrackReferralsSerializer(track_referrals, many=True)
        loop_list = serializer.data
        logger.info(
            logme("view loop modal - advisors referred", request)
        )
        if req_type == "mobile":
            return loop_list
        else:
            return render(request, "dashboard/view_loop_modal.html", locals())


def view_ranking_or_rating(request):
    '''
    Description: Fetching and showing Rating/Ranking received to the advisor
    '''
    if request.method == "POST":
        member_rank_list = []
        user_type = request.POST.get('user_type', None)
        req_type = request.POST.get('req_type', None)
        status_message = 'Rated' if user_type == 'advisor' else 'Ranked'
        if user_type:
            advisor = request.user.profile.advisor
            rated_or_ranked = AdvisorRating.objects.filter(
                user_type=user_type,
                advisor=advisor
            )
        for ranking in rated_or_ranked:
            rank_dict = {}
            if not ranking.existing_user_profile:
                rank_dict['member_name'] = ranking.external_user.name
                rank_dict['email'] = ranking.external_user.email
                rank_dict['phone'] = ranking.external_user.phone
                if ranking.avg_rating == 0:
                    rank_dict['status'] = 'Not yet '+status_message
                else:
                    rank_dict['status'] = status_message
                member_rank_list.append(rank_dict)
            else:
                rank_dict['member_name'] = ranking.existing_user_profile.first_name
                rank_dict['email'] = ranking.existing_user_profile.email
                rank_dict['phone'] = ranking.existing_user_profile.mobile
                if ranking.avg_rating == 0:
                    rank_dict['status'] = 'Not yet '+status_message
                else:
                    rank_dict['status'] = status_message
                member_rank_list.append(rank_dict)
        logger.info(
            logme("peers & clients ranking accessed", request)
        )
        if req_type == "mobile":
            return member_rank_list
        else:
            return render(request, "dashboard/view-rank-client-modal.html", locals())


def add_member(request):
    '''
    Description: It opens the add member model.
    '''
    if request.method == "POST":
        logger.info(
            logme("opened add member modal", request)
        )
        return render(request, "dashboard/add_member_modal.html", locals())


def view_client_enquiry(request):
    '''
    Description: It shows clients enquiry modal
    '''
    req_type = request.POST.get('req_type', None)
    user = request.user
    user_profile = user.profile
    advisor_name = user_profile.first_name+" "+user_profile.last_name
    advisor_id = user_profile.advisor.id
    advisor_email = user_profile.email
    enquiry_management = None
    members_data = client_enquiry(advisor_name, advisor_id, advisor_email)
    if members_data:
        enquiry_management = members_data['content']
    logger.info(
        logme("opened client enquiry list page", request)
    )
    if req_type == "mobile":
        return enquiry_management
    else:
        return render(request, "dashboard/client_enquiry_list.html", locals())


def refer_advisor(request):
    '''
    Description: Refer_advisor function is used to invite new user to join as an 
    advior with NF
    '''
    if request.method == "POST":
        ip_details = request.session['ip_info']
        user_agent_country = ip_details.get("country", constants.REGION_DEFAULT)
        logger.info(
            logme("redirected to refer advisor modal", request)
        )
        return render(request, "dashboard/refer_advisor_modal.html", locals())


def save_refer_advisor(request):
    '''
    Description: save_refer_advisor function saves newly refered user.
    '''
    if request.method == 'POST':
        user = request.user
        user_profile = user.profile
        communication_email = user_profile.email
        if user_profile.communication_email_id == 'secondary':
            communication_email = user_profile.secondary_email
        arraydata = request.POST.get('jsondata', None)
        req_type = request.POST.get('req_type', None)
        if arraydata:
            loop_dictdata = json.loads(arraydata)
            for k, looplist in loop_dictdata.items():
                if not user_profile.email == looplist[1]:
                    track_referral, created = TrackReferrals.objects.get_or_create(
                        email=looplist[1],
                        referral_user_type=constants.ADVISOR_ROLE,
                        referred_by=user_profile
                    )
                    if created:
                        track_referral.name = looplist[0]
                        track_referral.email = looplist[1]
                        track_referral.phone = looplist[2]
                        track_referral.location = looplist[3]
                        track_referral.products_serviced = looplist[4]
                        track_referral.registered_financial_advisor = looplist[5]
                        track_referral.sebi_reg_no = looplist[6]
                        track_referral.amfi_reg_no = looplist[7]
                        track_referral.irda_reg_no = looplist[8]
                        track_referral.crisil_verified_no = looplist[9]
                        if track_referral.know_duration:
                            track_referral.know_duration = looplist[10]
                        else:
                            track_referral.know_duration = 0
                        track_referral.believe_become_advisor = looplist[11]
                        track_referral.save()
                    info = 'Mail has been sent to your refferer'
                    advisor_name = user.get_full_name()
                    try:
                        context_dict = {
                            'referred_name': looplist[0],
                            'referred_by_name': advisor_name,
                            'advisor_mobile': user_profile.mobile,
                            'advisor_email': user_profile.email,
                            'url': api_constants.REFERRAL_LINK + user_profile.referral_code,
                        }
                        email = looplist[1]
                        send_mandrill_email(
                            'ABOTMI_13',
                            [email],
                            context=context_dict
                        )
                        # ip_details gets the advisor's country
                        ip_details = get_ipinfo(request)
                        user_agent_country = ip_details.get(
                            "country", constants.REGION_DEFAULT)
                        if user_agent_country == constants.REGION_IN:
                            # sending sms to new person
                            sms_status = get_sms_status(user_profile.status)
                            if sms_status:
                                message = 'Dear '+looplist[0]+', '+user.get_short_name()+' has joined ABOTMI and referred you to become an advisor. To know more www.abotmi.com.'
                                sms_response = send_sms_alert(
                                    mobile_number=looplist[2],
                                    message_template=message
                                )
                    except:
                        logger.info(
                            logme(
                                "failed to send sms or email to the referred user",
                                request
                            )
                        )
                        if req_type == "mobile":
                            return "Mail failure"
                        else:
                            return HttpResponse("Mail failure")
                    logger.info(
                        logme(
                            "referred user saved into track_referral table," +
                            " sent email & sms", request)
                    )
            if req_type == "mobile":
                return "success"
            else:
                return HttpResponse('success')
            logger.info(
                logme("redirected to refer advisor modal", request)
            )
        else:
            if req_type == "mobile":
                return "error"
            return HttpResponse('error', status=400)
    else:
        return HttpResponse('Access forbidden', status=405)


def invite_advisor_to_rate(request):
    '''
    Description : This function is to invite advisor to rate, sends the invite
    advisor form and saves the advisor details as external user, if he is not in our
    database.
    '''
    if request.method == 'POST':
        nf = NotificationFunctions(request)
        invited_advisor_data = "["+request.POST['invite_advisor_to_rate_form_data']+"]"
        invited_advisor_data = json.loads(invited_advisor_data)
        login_user_profile = request.user.profile
        communication_email = login_user_profile.email
        user_agent_country = get_ip_region(request)
        if login_user_profile.communication_email_id == 'secondary':
            communication_email = login_user_profile.secondary_email
        for user_details in invited_advisor_data:
            name = user_details['name']
            email = user_details['email']
            mobile = user_details['mobile']
            user_type = user_details['user_type']
            try:
                req_type = user_details['req_type']
            except:
                req_type = ''
            activation_key = generate_key()
            if AdvisorRating.objects.filter(activation_key=activation_key):
                activation_key = generate_key()
            user_profile = UserProfile.objects.filter(
                email=email
            )
            context_dict = {
                'advisor_name': login_user_profile.first_name,
                'advisor_mobile': login_user_profile.mobile,
                'advisor_email': login_user_profile.email,
                'peer_name': name,
                'url': settings.DEFAULT_DOMAIN_URL +
                '/signup/advisor_rating/' + activation_key
            }
            activation_key_value = settings.DEFAULT_DOMAIN_URL +'/signup/advisor_rating/'+activation_key
            if user_profile:
                user_profile = user_profile[0]
                if user_profile == login_user_profile:
                    logger.info(
                        logme("advisor can not invite himself to rate", request)
                    )
                    if req_type == "mobile":
                        return "You cannot invite yourself"
                    else:
                        return HttpResponse("You cannot invite yourself")
                already_invited = AdvisorRating.objects.filter(
                    advisor=login_user_profile.advisor,
                    existing_user_profile=user_profile,
                    user_type=user_type
                )
                # if not already_invited:
                if user_type == 'advisor':
                    AdvisorRating(
                        advisor=login_user_profile.advisor,
                        activation_key=activation_key,
                        existing_user_profile=user_profile,
                        user_type='advisor'
                    ).save()
                    nf.save_notification(
                        sender=login_user_profile,
                        receive=user_profile,
                        notification_type=RATE_REQ
                    )
                    send_mandrill_email(
                        'ABOTMI_08',
                        [email, ],
                        context=context_dict,
                    )
                    logger.info(
                        logme("sent invitation email to advisor=%s to rate " % (
                            str(user_profile)), request)
                    )
                    # SMS Sends to advisor based on their country.
                    if user_agent_country ==  constants.REGION_IN:
                        sms_status = get_sms_status(user_profile.status)
                        if sms_status:
                            message = 'Dear '+name+', Your peer '+request.user.profile.first_name+' has invited you to rate. Check your E-mail.'
                            sms_response = send_sms_alert(
                                mobile_number=mobile,
                                message_template=message
                            )
                            logger.info(
                                logme("sent invitation sms to advisor=%s to rate " % (
                                    str(mobile)), request)
                            )
                else:
                    if not user_profile.is_member:
                        logger.info(
                            logme("advisor can not be invited to rank", request)
                        )
                        if req_type == "mobile":
                            return "You cannot invite advisor to rank"
                        else:
                            return HttpResponse(
                                "You cannot invite advisor to rank")
                    AdvisorRating(
                        advisor=login_user_profile.advisor,
                        activation_key=activation_key,
                        existing_user_profile=user_profile,
                        user_type='member'
                    ).save()
                    nf.save_notification(
                        sender=login_user_profile,
                        receive=user_profile,
                        notification_type=RANK_REQ
                    )
                    send_mandrill_email(
                        'ABOTMI_12',
                        [email, ],
                        context=context_dict,
                    )
                    logger.info(
                        logme("sent invitation email to member=%s to \
                        rank" % (user_profile), request)
                    )
            else:
                external_user, created = ExternalUser.objects.get_or_create(
                    email=email)
                if created:
                    external_user.name = name
                    external_user.phone = mobile
                    external_user.save()
                already_invited = AdvisorRating.objects.filter(
                    advisor=login_user_profile.advisor,
                    external_user=external_user,
                    user_type=user_type
                )
                # if not already_invited:
                if user_type == 'advisor':
                    AdvisorRating(
                        advisor=login_user_profile.advisor,
                        activation_key=activation_key,
                        external_user=external_user,
                        user_type='advisor'
                    ).save()
                    send_mandrill_email(
                        'ABOTMI_10',
                        [email, ],
                        context=context_dict,
                    )
                    logger.info(
                        logme("sent invitation email to external advisor=%s to rate" % (
                            user_profile), request)
                    )
                    # SMS Sends to advisor based on their country.
                    if user_agent_country ==  constants.REGION_IN:
                        sms_status = get_sms_status(login_user_profile.status)
                        if sms_status:
                            message = 'Dear '+name+', Your peer '+login_user_profile.first_name+' has invited you to rate. Check your E-mail.'
                            sms_response = send_sms_alert(
                                mobile_number=mobile,
                                message_template=message
                            )
                            logger.info(
                                logme(
                                    "sent invitation sms to external advisor= %s to \
                                    rate" % (mobile), request)
                            )
                else:
                    AdvisorRating(
                        advisor=login_user_profile.advisor,
                        activation_key=activation_key,
                        external_user=external_user,
                        user_type='member'
                    ).save()
                    send_mandrill_email(
                        'ABOTMI_12',
                        [email, ],
                        context=context_dict,
                    )
                    logger.info(
                        logme(
                            "sent invitation email to external member=%s to \
                            rank" % (user_profile), request)
                    )
                    # SMS Sends to advisor based on their country.
                    if user_agent_country == constants.REGION_IN:
                        sms_status = get_sms_status(login_user_profile.status)
                        if sms_status:
                            message = 'Dear '+name+', Your advisor '+login_user_profile.first_name+' has invited you to rank.Check your E-mail'
                            sms_response = send_sms_alert(
                                mobile_number=mobile,
                                message_template=message
                            )
                            logger.info(
                                logme("sent invitation sms to external member=%s to \
                                rate" % (mobile), request)
                            )
        if req_type == "mobile":
            return "success"
        else:
            del(nf)
            return HttpResponse('success')
    else:
        user_type = request.GET.get('user_type')
        user_profile = UserProfile.objects.get(user=request.user)
        logger.info(
            logme("redirected to invite advisor to rate modal", request)
        )
        return render(
            request, 'dashboard/invite_advisor_to_rate_modal.html', locals())


def advisor_rating_list(request):
    '''
    Description: Function lists all advisors requested to be rated.
    '''
    advisor_to_rate_list = AdvisorRating.objects.filter(
        existing_user_profile=request.user.profile,
        activation_key__isnull=False,
    )
    if not advisor_to_rate_list:
        external_user = ExternalUser.objects.filter(email=request.user.profile.email)
        advisor_to_rate_list = AdvisorRating.objects.filter(
            external_user=external_user
        )
    logger.info(
        logme("opened modal of advisors requested to be rated", request)
    )
    return render(
        request, 'dashboard/rate_advisor_list_modal.html', locals())


def rate_advisor(request):
    '''
    Description: This view sends the advisor rating form
    and saves the rating to advisor rating table.
    '''
    activation_key = request.GET.get('activation_key', None)
    if request.method == 'GET':
        if activation_key:
            try:
                advisor_to_rate = AdvisorRating.objects.get(
                    activation_key=activation_key)
            except ObjectDoesNotExist:
                logger.warning(
                    logme("[rate_advisor] failed because of no\
                    advisor rating object found", request)
                    )
                return HttpResponse(
                    "You have been already invited by your colleague!!!")
            logger.info(
                logme('redirected to advisor rating form', request)
            )
            return render(
                request, 'dashboard/rate_advisor_modal.html', locals())
    else:
        req_type = request.POST.get('req_type', None)
        activation_key = request.POST.get('activation_key', None)
        advisor_to_rate = AdvisorRating.objects.get(
            activation_key=activation_key)
        advisor_to_rate.trust = request.POST.get('trust')
        advisor_to_rate.financial_knowledge = request.POST.get('financial')
        advisor_to_rate.communication = request.POST.get('communication')
        advisor_to_rate.advisory = request.POST.get('advisory')
        advisor_to_rate.ethics = request.POST.get('ethics')
        advisor_to_rate.customer_care = request.POST.get('customer')
        advisor_to_rate.avg_rating = request.POST.get('average')
        advisor_to_rate.activation_key = ''
        advisor_to_rate.save()
        context_dict = {
            'advisor_name': advisor_to_rate.advisor.user_profile.first_name,
            'peer_name': request.user.get_full_name(),
            'url': settings.DEFAULT_DOMAIN_URL + "/dashboard/"
        }
        if advisor_to_rate.user_type == 'advisor':
            send_mandrill_email(
                'ABOTMI_33',
                [advisor_to_rate.advisor.user_profile.email],
                context=context_dict,
            )
            # Commented temporerly - Greeting message for giving the rating.
            # send_mandrill_email(
            #     'reia-08-02-02',
            #     [request.user.username, ],
            #     context=context_dict,
            # )
        logger.info(
            logme("advisor rating saved and mail send to the advisor", request)
        )
        if req_type == "mobile":
            return "success"
        else:
            return HttpResponse("success")


def accept_or_decline_booking(request):
    '''
    Description: This view is for an advisor to accept/decline the booking enquiry
    the view does get the data from northfacing database, so
    we just change status to accepted/rejected.
    '''
    if request.method == "POST":
        status = request.POST.get('status')
        booking_id = request.POST['booking_id']
        reason = request.POST['reason']
        data = None
        if status == 'accept':
            data = {
                'booking_id': booking_id,
                'status': 1
            }
            logger.info(
                logme('booking enquiry got accepted', request)
            )
        elif status == 'decline':
            data = {
                'booking_id': booking_id,
                'status': 0,
                'reason': reason
            }
            logger.info(
                logme('booking enquiry got declined', request)
            )
        requests.post(
            api_constants.ENQUIRY_MANAGEMENT_ACCEPT_REJECT_STATUS,
            data=data,
            verify=constants.SSL_VERIFY
        )
        logger.info(
            logme("status of booking enquiry changed", request)
        )
        return HttpResponse("success")


def valid_email(request):
    '''
    Description: Checking email is already reffered by advisor.
        (i.e; advisor can't reffer one person more than once)
    '''
    email = None
    if request.method == 'POST':
        email = request.POST.get('email_id', None)
        req_type = request.POST.get('req_type', None)
        user = request.user
        user_profile = user.profile
        username = user.username
        if not username == email:
            if UserProfile.objects.filter(email=email):
                logger.info(
                    logme("validation - email has already exist", request)
                )
                if req_type == "mobile":
                    return 'Advisor already exist'
                return HttpResponse("Advisor already exist")
            else:
                logger.info(
                    logme(
                        "validation - email is new. advisor can able to refer/loop",
                        request
                    )
                )
                if req_type == 'mobile':
                    return "success"
                return HttpResponse("success")
        else:
            if req_type == 'mobile':
                return "You cannot loop/refer yourself"
            return HttpResponse("You cannot loop/refer yourself")


def valid_email_for_rating(request):
    '''
    Description: Checking, Advisor is sent already request for rating or ranking
        (i.e; Advisor can send Ranking or Rating Invitation once per user/advisor )
    '''
    email = None
    if request.method == 'POST':
        email = request.POST['email_id']
        user_type = request.POST['user_type']
        user_profile = UserProfile.objects.filter(email=email)
        external_user = ExternalUser.objects.filter(email=email)
        # user_type : advisor for rate and member for rank
        if user_type =='advisor':
            if AdvisorRating.objects.filter(existing_user_profile=user_profile,advisor=request.user.profile.advisor,user_type='advisor') or AdvisorRating.objects.filter(external_user=external_user,advisor=request.user.profile.advisor,user_type='advisor'):
                logger.info(
                    logme(
                        "validation - requested email advisor has already rated",
                        request
                    )
                )
                return HttpResponse("Advisor already referred")
            else:
                logger.info(
                    logme(
                        "validation - requested email advisor has not rated yet",
                        request
                    )
                )
                return HttpResponse("success")
        if user_type =='member':
            if Advisor.objects.filter(user_profile=user_profile) or AdvisorRating.objects.filter(existing_user_profile=user_profile,advisor=request.user.profile.advisor,user_type='member') or AdvisorRating.objects.filter(external_user=external_user,advisor=request.user.profile.advisor,user_type='member'):
                logger.info(
                    logme("validation - requested email user has already ranked",request)
                )
                return HttpResponse("Advisor already referred")
            else:
                logger.info(
                    logme("validation - requested email user has not ranked yet", request)
                )
                return HttpResponse("success")


def check_address_proof(request):
    '''
    Description: Checking weather the advisor has done EIPV or not
    '''
    if request.method == 'POST':
        if request.user.profile.advisor.ipv_status:
            logger.info(
                logme("advisor has completed EIPV",request)
            )
            return HttpResponse("true")
        else:
            logger.info(
                logme("advisor has not done EIPV",request)
            )
            return HttpResponse("false")
    else:
        logger.info(
            logme("GET request - access forbidden to the user for EIPV")
        )
        return HttpResponse("Access forbidden")


def appling_crisil(request):
    '''
    Description: Advisor is applying for CRISIL Certification.
    '''
    if request.method == 'POST':
        username = request.POST['username']
        promocode = request.POST['promocode']
        crisil_selected_years = request.POST['crisil_selected_years']
        crisil_offered_years = 0
        discount_percentage = 0
        user_profile = request.user.profile
        advisor = user_profile.advisor
        if int(crisil_selected_years) == constants.CERTIFICATE_YEARS:
            crisil_offered_years = constants.CRISIL_OFFERED_YEARS
        # checking promocode is valid or not
        valid_promocode = ''
        if request.POST['promocode_status'] == 'applied':
            valid_promocode = PromoCodes.objects.filter(
                user_profile=user_profile,
                promo_code=promocode
            )
        if valid_promocode:
            discount_percentage = constants.CRISIL_CERTIFICATE_DISCOUNT
            final_amount = calculate_final_amount_with_discount_and_tax_amount(
                    constants.CRISIL_CERTIFICATE_VALUE,
                    crisil_selected_years,
                    discount_percentage,
                    constants.TAX_PERCENTAGE_CRISIL
                )
        else:
            final_amount = calculate_final_amount_with_discount_and_tax_amount(
                    constants.CRISIL_CERTIFICATE_VALUE,
                    crisil_selected_years,
                    discount_percentage,
                    constants.TAX_PERCENTAGE_CRISIL
                )
        '''
        if the user has any previous transaction, then it is renewal
        for renewal update the object
        '''
        transaction_instance, status = TransactionsDetails.objects.get_or_create(
                                                user_profile=request.user.profile)
        new_invoice_no = invoice_gen(advisor, transaction_instance)
        if valid_promocode:
            transaction_instance.promo_code = promocode
        transaction_instance.discounted_amount = final_amount
        transaction_instance.invoice_number = new_invoice_no
        transaction_instance.amount = constants.CRISIL_CERTIFICATE_VALUE*int(
            crisil_selected_years)
        transaction_instance.transaction_type = constants.TR_TYPE
        transaction_instance.serial_no = int(new_invoice_no.split('-')[-1])
        description = {
            "remark": "",
            "no_of_years_selected": crisil_selected_years,
            "offered_years": crisil_offered_years
        }
        description = json.dumps(description)
        transaction_instance.description = description
        transaction_instance.save()
        # changing the status in crisil application status in advisor table
        advisor.crisil_application_status = constants.CRISIL_APPLIED
        advisor.save()
        logger.info(
            logme("advisor successfully applied for CRISIL certification", request)
        )
        # SEND EMAIL ALERT to Advisor================================
        communication_email = request.user.profile.email
        if user_profile.communication_email_id == 'secondary':
            communication_email = user_profile.secondary_email
        first_name = user_profile.first_name
        last_name = user_profile.last_name
        name = first_name + ' ' + last_name
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
            'final_amount': final_amount,
            'final_amount_in_words': amount_in_words
        }
        send_mandrill_email('REIA_17', [communication_email], context=context_dict)
        logger.info(
            logme(
                "bank details email sent for successfully applying for CRISIL \
                certification", request)
        )
        # SEND EMAIL ALERT TO ADMIN ===============================
        send_mandrill_email_admin(
            'reaf-contact-admin',
            [settings.REIA_ADMIN_EMAIL],
            communication_email,
            context={}
        )

        logger.info(
            logme("email sent to the reia admin, advisor applied for CRISIL \
                certification", request)
        )
        # ip_details gets advisor's country
        ip_details = get_ipinfo(request)
        user_agent_country = ip_details.get("country", constants.REGION_DEFAULT)
        if user_agent_country == constants.REGION_IN:
            # SEND SMS ALERT ==========================================
            if user_profile.mobile:
                mobile_number = user_profile.mobile
                sms_status = get_sms_status(user_profile.status)
                if sms_status:
                    message = 'Dear '+user_profile.first_name+' ('+user_profile.registration_id+'),Thank you for expressing interest to become a CRISIL verified Advisor. To proceed, upload the payment details.'
                    sms_response = send_sms_alert(
                        mobile_number=mobile_number,
                        message_template=message
                    )

        logger.info(
            logme("sent sms alert to Indaian advisors for successfully applying for \
                CRISIL certification", request)
        )
        return HttpResponse('success')


def submit_crisil_form(request):
    '''
    Description: For loading payment details form for crisil application.
    '''
    payment_form = PaymentForm()
    if request.method == 'GET':
        initial_data = {
            'user_profile': request.user.profile
        }
        transaction_details = TransactionsDetails.objects.filter(
            user_profile=request.user.profile).first()
        payment_form = PaymentForm(instance=transaction_details)
        no_of_years_selected = ''
        if transaction_details.description:
            description = json.loads(transaction_details.description)
            no_of_years_selected = int(description['no_of_years_selected']) + int(
                description['offered_years'])
        '''
        Load Modal Body with this form
        '''
        logger.info(
            logme("submit payment form for CRISIL Application modal opened", request)
        )
        return render(request, 'dashboard/submit_payment_form_modal.html', locals())

    if request.method == 'POST':
        '''
        Deal Transcation things
        '''
        tr_instance, tr_status = TransactionsDetails.objects.get_or_create(
            user_profile=request.user.profile)
        description = tr_instance.description
        discounted_amount = tr_instance.discounted_amount
        payment_form = PaymentForm(
            request.POST,
            request.FILES,
            instance=tr_instance
        )
        if payment_form.is_valid():
            documents_new_upload, status = UploadDocuments.objects.get_or_create(
                user_profile=request.user.profile,
                registration_number=request.POST['cheque_dd_no']
            )
            documents_new_upload.documents = request.FILES['scaned_doc']
            documents_new_upload.documents_type = "bank_details"
            documents_new_upload.save()
            payment_instance = payment_form.save(commit=False)
            payment_instance.user_profile = request.user.profile
            payment_instance.discounted_amount = discounted_amount
            payment_instance.upload_cheque_dd_id = documents_new_upload
            payment_instance.status = None
            payment_instance.description = description
            payment_instance.save()
            advisor = Advisor.objects.get(
                user_profile=request.user.profile)
            if not advisor.crisil_application_status == constants.CRISIL_RENEWAL_PAYMENT_RE_SUBMIT:
                advisor.crisil_application_status = constants.CRISIL_PAYMENT_SUBMITTED
            else:
                advisor.crisil_application_status = constants.CRISIL_RENEWAL_PAYMENT_SUBMITTED
            advisor.save()

            logger.info(
                logme(
                    "payment details updated for CRISIL certification application",
                    request
                )
            )
            # SEND EMAIL ALERT to Advisor ================================
            communication_email = request.user.profile.email
            if request.user.profile.communication_email_id == 'secondary':
                communication_email = request.user.profile.secondary_email
            first_name = request.user.profile.first_name
            last_name = request.user.profile.last_name
            advisor_name = first_name + ' ' + last_name
            context_dict = {
                'advisor_name': advisor_name
            }
            logger.info(
                logme(
                    "payment details updated for CRISIL certification application",
                    request
                )
            )
            return HttpResponse('success')
        else:
            logger.info(
                logme("CRISIL Application payment form invalid- Status Failed", request)
            )
            return HttpResponse('failure')


def check_promocode(request):
    '''
    Description: Return the relevant data, which includes final amount, status of the
    promocode, tax amount applicable.
    '''
    if request.method == 'POST':
        code = request.POST['code']
        crisil_selected_years = request.POST['crisil_selected_years']
        certificate_value = calculate_certificate_value(
                constants.CRISIL_CERTIFICATE_VALUE,
                crisil_selected_years
            )
        valid_promocode = PromoCodes.objects.filter(
            user_profile=request.user.profile,
            promo_code=code
        )
        if valid_promocode:
            discount_amount = calculate_discount_amount(
                certificate_value,
                constants.CRISIL_CERTIFICATE_DISCOUNT
            )
            tax_amount = calculate_tax_amount(
                discount_amount, constants.TAX_PERCENTAGE_CRISIL)
            final_amount = discount_amount + tax_amount
            status = 'valid'
        else:
            tax_amount = calculate_tax_amount(
                certificate_value, constants.TAX_PERCENTAGE_CRISIL)
            final_amount = certificate_value + tax_amount
            status = 'invalid'
        data = {
            'amount': final_amount,
            'promocode_status': status,
            'tax': tax_amount
        }
        data = JsonResponse(data)
        logger.info(
            logme("checked the promo code status %s" %(str(status)), request)
        )
        return data
    else:
        logger.info(
            logme("access forbidden to check promo code",request)
        )
        return HttpResponse('Access forbidden')


def submit_crisil_online_payment_form(request):
    '''
    Descrption: Settings values which is required for EBS Payment navigation
    '''
    user = request.user
    user_profile = user.profile
    advisor = user_profile.advisor
    crisil_payment = TransactionsDetails.objects.filter(
        user_profile = user_profile).first()
    secrete_key = settings.EBS_SECRETE_KEY
    account_id = settings.EBS_ACCOUNT_ID
    address = user_profile.address
    amount = crisil_payment.discounted_amount
    channel = settings.EBS_CHANNEL
    city = user_profile.city
    country = settings.EBS_COUNTRY
    currency = settings.EBS_COURENCY
    payment_description = constants.CRISIL_ONLINE_PAYMENT_DESCRIPTION
    email = user_profile.email
    phone = user_profile.mobile
    mode = settings.EBS_MODE
    name = constants.CRISIL_ONLINE_PAYMENT_NAME
    postal_code = user_profile.pincode
    reference_no = hashlib.md5(str(user_profile.id)+str(
        user_profile.email)).hexdigest()[:15]
    return_url = settings.DEFAULT_DOMAIN_URL+'/dashboard/crisil_payment_success/'
    hash_data = secrete_key+'|'+str(account_id)+'|'+address+'|'+str(amount)+'|'+\
        str(channel)+'|'+city+'|'+country+'|'+currency+'|'+payment_description+'|'+\
        email+'|'+mode+'|'+name+'|'+str(phone)+'|'+postal_code+'|'+str(reference_no)+'|'+return_url
    secure_hash_key = hashlib.sha512(hash_data).hexdigest().upper()
    if crisil_payment:
        if crisil_payment.description:
            description = json.loads(crisil_payment.description)
            description['country'] = country
            description['MerchantRefNo'] = reference_no
            crisil_payment.description = json.dumps(description)
            crisil_payment.transaction_type = constants.TR_TYPE_ONLINE
        crisil_payment.save()
    logger.info(
        logme('Advisor requested online payment for CRISIL,\
            Navigated to EBS payment from crisil_online_payment page', request)
    )
    return render(request, 'dashboard/crisil_online_payment.html', locals())


@csrf_exempt
def crisil_payment_success(request):
    '''
    Descrption: Getting the response from EBS payment.
    '''
    if request.method == 'POST':
        user_profile = request.user.profile
        advisor = user_profile.advisor
        payment_status = request.POST.get('ResponseMessage', None)
        error_code = request.POST.get('Error', None)
        request_id = request.POST.get('RequestID', None)
        payment_id = request.POST.get('PaymentID', None)
        transaction_id = request.POST.get('TransactionID', None)
        response_code = request.POST.get('ResponseCode', None)
        payment_received_date = request.POST.get('DateCreated', None)
        merchant_ref_no = request.POST.get('MerchantRefNo', None)
        name = name = user_profile.first_name+" "+user_profile.last_name
        crisil_application_status = advisor.crisil_application_status
        crisil_payment = TransactionsDetails.objects.filter(
            user_profile=user_profile).first()
        logger.info(
            logme('Got response from EBS for invoice bill no:- %s' % (
                crisil_payment.invoice_number), request)
        )
        logger.info(
            logme('EBS Payment Response:- %s' % (payment_status), request)
        )
        if crisil_payment:
            amount = crisil_payment.discounted_amount
            amount_in_words = num2words(float(amount), lang='en_IN')
            context_dict = {
                'advisor_name': name,
                'final_amount': amount,
                'final_amount_in_words': amount_in_words,
                'bank_name': '',
                'reference_number': merchant_ref_no,
                'date_of_payment': payment_received_date,
                'amount': amount,
                'URL': settings.LOGIN_URL
            }
            try:
                if crisil_payment.description:
                    description = json.loads(crisil_payment.description)
                    description['RequestID'] = request_id
                    description['PaymentID'] = payment_id
                    description['TransactionID'] = transaction_id
                    if payment_status:
                        description['ResponseMessage'] = payment_status
                    else:
                        description['ResponseMessage'] = 'Failed'
                    description['ResponseCode'] = response_code
                    description['Error'] = error_code
                    crisil_payment.description = json.dumps(description)
            except:
                logger.info(
                    logme('failed to save payment response recieved by EBS', request)
                )
            if payment_status == 'Transaction Successful':
                if crisil_application_status == constants.CRISIL_EXPIRED_BY_USER \
                    or crisil_application_status == constants.CRISIL_RENEWAL:
                        new_invoice_no = invoice_gen(advisor_obj, transaction_obj)
                        cri_app_status = constants.CRISIL_RENEWAL_CERTIFICATE_IN_PROCESS
                        paid_tran_status == constants.TR_RENEWAL_PAID
                        crisil_payment.serial_no = int(new_invoice_no.split('-')[-1])
                        crisil_payment.invoice_number = new_invoice_no
                else:
                    cri_app_status = constants.CRISIL_CERTIFICATE_IN_PROCESS
                    paid_tran_status = constants.TR_PAID
                    new_invoice_no = crisil_payment.invoice_number

                advisor.crisil_application_status = cri_app_status
                crisil_payment.credited_date = datetime.datetime.strptime(
                    payment_received_date, '%Y-%m-%d %H:%M:%S').date()
                crisil_payment.save()
                MESSAGE = 'Dear '+user_profile.first_name+' ('+user_profile.registration_id+'),Thanks for the payment towards CRISIL verification'
                invoice_bill_pdf(user_profile, new_invoice_no, 'REIA_17_04', context_dict)
                try:
                    # ip_details get country
                    ip_details = get_ipinfo(request)
                    user_agent_country = ip_details.get(
                        "country",constants.REGION_DEFAULT)
                    if user_agent_country == constants.REGION_IN:
                        if user_profile.mobile:
                            mobile_number = user_profile.mobile
                            sms_status = get_sms_status(user_profile.status)
                            if sms_status == True:
                                sms_response = send_sms_alert(mobile_number=mobile_number, message_template=MESSAGE)
                except:
                    logger.info(
                        logme('failed to send crisil payment success sms', request)
                    )
            else:
                paid_tran_status = constants.TR_INVALID
            crisil_payment.status = paid_tran_status
            crisil_payment.save()
            advisor.save()
        return render(request, 'dashboard/crisil_payment_success.html', locals())
    else:
        return HttpResponse('Access forbidden')


def add_group_name(request):
    '''
    Description: Adding new Group name
    '''
    if request.method == 'POST':
        group_name = request.POST['group_name']
        group_object, status = GroupMaster.objects.get_or_create(
            group_name=group_name,
            group_owner=request.user.profile
        )
        if status:
            response = {
                'result': 'success',
                'group_id': group_object.id,
            }
            logger.info(
                logme("advisor created group successfully", request)
            )
            return JsonResponse(response)
        else:
            response = {
                'result' : 'exists',
            }
            logger.info(
                logme("advisor couldn't create - group already exists", request)
            )
            return JsonResponse(response)
    else:
        logger.info(
            logme("access forbidden to create new groups", request)
        )
        return HttpResponse('Access forbidden')


def group_list_view(request):
    '''
    Description: Shows All Group Lists in Dashboard Client Management
    '''
    if request.method == 'POST':
        group_names_list = GroupMaster.objects.filter(group_owner=request.user.profile)
        total_members = Member.objects.filter(user_profile__created_by=request.user)
        client_list = ''
        client_list = get_all_client(request.user.profile)
        logger.info(
            logme("redirected to the list of all group page", request)
        )
        return render(request, 'dashboard/grouping_list.html', locals())


def group_members(request):
    '''
    Description: Showing All Group Lists in Dashboard Client Management
    '''
    if request.method == 'POST':
        group_id = request.POST['group_id']
        group_members = GroupMembers.objects.filter(group_id=group_id)
        # excluded_member's list - Commented for temporary purpose
        # excluded_members = Member.objects.filter(\
        #         group_profile_id__created_by = request.user
        #     ).exclude(\
        #         group_profile_id__in=GroupMembers.objects.filter(group_id = group_id).values('user_profile')\
        #     )
        logger.info(
            logme(
                "accessed list of all groups members in dashboard client management",
                request
            )
        )
        return render(request, 'dashboard/group_member_list_view.html', locals())
    else:
        logger.info(
            logme("GET request - access forbidden to manage client in groups")
        )
        return HttpResponse('Access forbidden')


def list_members_excluded(request):
    '''
    Description: Showing All Members which are not there inside Group in Dashboard 
    Client Management
    '''
    if request.method == 'POST':
        group_id = request.POST['group_id']
        excluded_members = Member.objects.filter(
                is_register_member=True,
                user_profile__created_by=request.user
            ).exclude(
                user_profile__in=GroupMembers.objects.filter(
                    group_id=group_id).values('user_profile')
            )
        logger.info(
            logme("returned all members list which are not in group",request)
        )
        return render(request, 'dashboard/list_new_group_members_view.html', locals())
    else:
        logger.info(
            logme(
                "GET request- access forbidden to list of all members not in their \
                groups", request
            )
        )
        return HttpResponse('Access forbidden')


def onchange_add_member_in_group(request):
    '''
    Description: Adding member using onchange in to Group
    '''
    if request.method == 'POST':
        group_id = request.POST['group_id']
        user_profile = request.POST['member']
        if group_id and user_profile:
            group_member, status = GroupMembers.objects.get_or_create(
                group_id=group_id,
                user_profile_id=user_profile
            )
            if status == True:
                logger.info(
                    logme("adding member onchange into group",request)
                )
                return HttpResponse('record_created')
            else:
                group_member.delete()
                logger.info(
                    logme("removing member onchange from group", request)
                )
                return HttpResponse('record_deleted')
        else:
            logger.info(
                logme("no group found for deleting/adding member", request)
            )
            return HttpResponse('no_data_found')
    else:
        logger.info(
            logme(
                "GET request - access forbidden to the user in adding/removing member \
                onchange in group", request)
        )
        return HttpResponse('Access forbidden')


def add_member_in_group(request):
    '''
    Description: Adding member to the Group
    '''
    if request.method == 'POST':
        group_id = request.POST['group_id']
        members = request.POST['members']
        members_list = members.split(",")
        for member in members_list:
            group_member, status = GroupMembers.objects.get_or_create(
                group_id=group_id, user_profile_id=member)
        logger.info(
            logme("added members into groups", request)
        )
        return HttpResponse('success')
    else:
        logger.info(
            logme(
                "GET request - access forbidden for adding members into groups", request)
        )
        return HttpResponse('Access forbidden')


def update_group(request):
    '''
    Description: Updating group name, members in group
    '''
    if request.method =='POST':
        group_id = request.POST.get('group_id', None)
        group_name = request.POST.get('group_name', None)
        members = request.POST.get('members', None)
        unselected_members = request.POST.get('unselected_members', None)
        group_object = GroupMaster.objects.filter(
            group_name=group_name,
            group_owner=request.user.profile).exclude(id=group_id)
        if not group_object:
            master_group = GroupMaster.objects.get(id=group_id)
            master_group.group_name = group_name
            master_group.save()
            if members:
                members_list = members.split(",")
                if members_list:
                    for member in members_list:
                        group_member, status = GroupMembers.objects.get_or_create(
                            group_id=group_id, group_profile_id=member)
            if unselected_members:
                unselected_list = unselected_members.split(",")
                if unselected_list:
                    for un_member in unselected_list:
                        exist_group_member = GroupMembers.objects.filter(
                            group_id=group_id, group_profile_id=un_member)
                        if exist_group_member:
                            exist_group_member[0].delete()
            logger.info(
                logme(
                    "updated successfully group name and updated members in the group",
                    request)
            )
            return HttpResponse('success')
        else:
            logger.info(
                logme("group does not exist for updating members", request)
            )
            return HttpResponse('exists')
    else:
        logger.info(
            logme("GET request - access forbidden for updating groups", request)
        )
        return HttpResponse('Access forbidden')


def delete_group(request):
    '''
    Description: Deleting the group with members present in that, from Grouping
    permenentaly
    '''
    if request.method == 'POST':
        group_id = request.POST.get('group_id', None)
        master_group = GroupMaster.objects.filter(id=group_id)
        group_members = GroupMembers.objects.filter(group_id=group_id)
        if group_members:
            group_members.delete()
        if master_group:
            master_group[0].delete()
        logger.info(
            logme("deleted group with members permanentaly", request)
        )
        return HttpResponse('success')
    else:
        logger.info(
            logme(
                "GET request - action forbidden for deleting group with members", request)
        )
        return HttpResponse('Access forbidden')


def create_new_group(request):
    '''
    Description: Creating Group with members form Grouping
    '''
    if request.method == 'POST':
        new_group_name = request.POST['new_group_name']
        selected_clients = request.POST['selected_clients']
        if new_group_name:
            group_object, status = GroupMaster.objects.get_or_create(
                    group_name=new_group_name,
                    group_owner=request.user.profile
                )
        if selected_clients:
            new_clients = selected_clients.split(",")
            for clients in new_clients:
                group_member, status = GroupMembers.objects.get_or_create(\
                    group = group_object, group_profile_id = clients)
        logger.info(
            logme("created new group with members", request)
        )
        return HttpResponse('success')
    else:
        logger.info(
            logme("GET request - access forbidden to create new groups", request)
        )
        return HttpResponse('Access forbidden')


def renewal_submit_crisil_form(request):
    '''
    Description: Function loads a form for renewal payment and submits the payment form
    '''
    tr_instance  = TransactionsDetails.objects.get(user_profile=request.user.profile)
    advisor_status = request.user.profile.advisor.crisil_application_status
    discount_percentage = 0
    if advisor_status =='crisil_certificate_expired':
        amount = calculate_final_amount_with_discount_and_tax_amount(\
                constants.CRISIL_CERTIFICATE_VALUE,
                constants.CERTIFICATE_RENEWAL_YEAR,
                discount_percentage,
                constants.TAX_PERCENTAGE_CRISIL
            )
    else :
        amount = calculate_final_amount_with_discount_and_tax_amount(\
                constants.CRISIL_CERTIFICATE_RENEWAL_VALUE,
                constants.CERTIFICATE_RENEWAL_YEAR,
                discount_percentage,
                constants.TAX_PERCENTAGE_CRISIL
            )
    '''
    Description: Loading the form for renewal payment
    '''
    if request.method == 'GET':
        initial_data = {
            'user_profile': request.user.profile
        }
        logger.info(
            logme('renwal CRISIL certificate modal opened', request)
        )
        return render(request, 'dashboard/submit_renewal_payment_form_modal.html', locals())

    '''
    Description: Submitting the payment form for renewal payment
    '''
    if request.method == 'POST':
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
        advisor = Advisor.objects.get(user_profile = request.user.profile)
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
            logme("CRISIL Application renewal payment details submitted", request)
        )
        return HttpResponse('success')
    else:
        logger.info(
            logme("failed to submit the CRISIL certificate renewal payment details",request)
        )
        return HttpResponse('failure')


def add_client_to_comapny(client_data, headers):
    '''
    Description: It maps a client to the company
    '''
    cli_res = requests.post(api_constants.ADD_CLIENT_API, data = client_data, headers = headers)
    return cli_res.status_code

def save_add_client(email,first_name,last_name,mobile,user_profile):
    '''
    Description: Saving the add clinet details  to ClientDetails,  ClientPlatform table
    '''
    user = User.objects.filter(username=email)
    message = None
    if not user:
        auth_token = {
            "username":settings.UPWRDZ_USERNAME,
            "password":settings.UPWRDZ_PASSWORD
        }
        res = requests.post(
            api_constants.UPWRDZ_AUTH_URL,
            data = auth_token,
            verify = constants.SSL_VERIFY
        )
        token = "JWT "+json.loads(res.content)['token']
        headers = {
            'Authorization' : token
        }
        client_data = {
            'first_name':first_name,
            'last_name':last_name,
            'email': email,
            'mobile': mobile,
            'platform_email' : constants.UPLYF_ADMIN_EMAIL
        }
        status_code = add_client_to_comapny(client_data, headers)
        if status_code == 201:
            message = "User Created"
            client_pt = ClientPlatform.objects.filter(platform_email = constants.UPLYF_ADMIN_EMAIL).first()
            client_details = ClientDetails.objects.filter(email = email, client_platform = client_pt).first()
            client_mapping, created = ClientAdvisorMapping.objects.get_or_create(
                client = client_details, user_profile = user_profile)
            if created:
                client_mapping.client = client_details
                client_mapping.user_profile = user_profile
                client_mapping.save()
        elif status_code == 200:
            message = "You have already added"
    else:
        message = "User already exists"


def view_client_details(request):
    '''
    Description: It gets all the client details from UPLYF
    '''
    if request.method == "GET":
        client_list = ''
        client_list = get_all_client(request.user.profile)
        return render(request, "dashboard/view_member_modal.html", locals())


def save_new_member(request):
    '''
    Description: Sending Client/Member Details to UPLYF for saving.
    '''
    if request.method == 'POST':
        user = User.objects.filter(username=request.POST.get('email',None))
        req_type = request.POST.get('req_type',None)
        if not user:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            mobile = request.POST['mobile']
            user = request.user
            advisor = user.profile.advisor
            # For storing in upwrdz table
            save_add_client(email,first_name,last_name,mobile,user.profile)
            # End of upwrdz table
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
                if req_type == "mobile":
                   return message
                else:
                   return HttpResponse(message)
            else:
                logger.info(
                    logme("unable to save clients details into UPLYF database",request)
                )
                if req_type == "mobile":
                   return "unabletosave"
                else:
                   return HttpResponse('unable to save')
        else:
            message="User is an Advisor"
            logger.info(
                    logme("the advisor is already looped and registered in UPWRDZ",request)
                )
            if req_type == "mobile":
                return message
            else:
                return HttpResponse(message)


def advisor_member_maping(request):
    '''
    Description: Sending Advisor Confirmation Status to Map Advisor to Client
    '''
    user = request.user
    user_email = request.POST['user_email']
    accepted = request.POST['accepted']
    advisor_email = user.username
    member_data = {
        'user_email' : user_email,
        'advisor_email' : advisor_email,
        'accepted' : accepted,
        'advisor_id' : user.profile.advisor.id,
        'advisor_name' : user.first_name+' '+user.last_name,
    }
    token = auth_token(settings.UPLYF_USER_NAME, settings.UPLYF_PASSWORD)
    headers = {'Authorization': 'JWT %s' %token['token']}
    user_response = requests.post(
        api_constants.ADVISOR_MEMBER_MAPING,
        headers = headers,
        data = member_data,
        verify = constants.SSL_VERIFY
    )
    if not user_response.status_code == 200:
        logger.info(
            logme("mapping failed for advisor to existing client in UPLYF",request)
        )
        return HttpResponse('unable to map')
    else:
        message = json.loads(user_response.content)
        message = message['message']
        logger.info(
            logme("sent mapping request to existing client in UPLYF",request)
        )
    return HttpResponse(message)


def launch_uplyf(request):
    '''
    Description: Launching UPLYF from UPWRDZ(REIA) with advisor account
    '''
    context = RequestContext(request)
    if request.method == 'POST':
        if request.user.profile.advisor:
            uplyf_server_name = api_constants.UPLYF_USER_LOGIN
            token = auth_token(settings.UPLYF_USER_NAME, settings.UPLYF_PASSWORD)
            headers = {'Authorization': 'JWT %s' %token['token']}
            register_advisor = api_constants.UPLYF_USER
            users_profile = request.user.profile
            advisor = users_profile.advisor
            advisor_data = {
                'first_name':users_profile.first_name,
                'email':users_profile.email,
                'mobile':users_profile.mobile,
                'gender':users_profile.gender,
                'birthday': str(users_profile.birthdate),
                'sm_source':constants.UPWRDZ_MEDIA,
                # Commented - Since aadhaar number is not available
                # 'aadhaar_no':users_profile.adhaar_card,
                'eipv_status':advisor.ipv_status,
                'user_role':request.POST.get('user_role', None)
            }
            advisor_response = requests.post(
                register_advisor,
                headers = headers,
                data = advisor_data,
                verify = constants.SSL_VERIFY
            )
            advisor_json_res  = advisor_response.content
            json_res = json.loads(advisor_json_res)
            if json_res:
                if json_res['new_user']:
                    print 'new advisor created with session'
                else:
                    print 'advisor already exists and session created'
            response_dict = {
                'status': True,
                'username': json_res['email'],
                'token': json_res['token'],
                'user_token':json_res['user_token'],
                'users_role':json_res['users_role']
            }
            logger.info(
                logme("launching UPLYF from UPWRDZ account as advisor", request)
            )
            return JsonResponse(response_dict)
        else:
            logger.info(
                logme("unable to launch UPLYF as not a advisor", request)
            )
            return HttpResponse('You do not have access to this page')

    if request.method == 'GET':
        logger.info(
            logme("GET request - access forbidden to launch UPLYF from UPWRDZ as advisor", request)
        )
        return HttpResponse('you do not have access to this page \
        <a href="/">click here to return home</a>')


def manage_uplyf_transaction(request):
    '''
    Description: showing adviosrs all transactions from uplyf
    '''
    req_type = request.POST.get('req_type',None)
    user_profile = request.user.profile
    advisor = user_profile.advisor
    token = auth_token(settings.UPLYF_USER_NAME, settings.UPLYF_PASSWORD)
    headers = {'Authorization': 'JWT %s' %token['token']}
    advisor_data = {
        'advisor_id' : advisor.id,
        'advisor_name' : user_profile.first_name +' '+ user_profile.last_name,
        'advisor_email' : user_profile.email
    }
    advisor_response = requests.post(
        api_constants.GET_UPLYF_TRANSACTIONS,
        headers = headers,
        data = advisor_data,
        verify = constants.SSL_VERIFY
    )
    if advisor_response.status_code == 200:
        advisor_transactions = json.loads(advisor_response.content)
        i = 0
        for at in advisor_transactions:
            j = 0
            if at.get('booking_transaction_documents', None):
                for doc in at.get('booking_transaction_documents', None):
                    file_name = get_filename_from_document_path(doc['document'])
                    advisor_transactions[i]['booking_transaction_documents'][j]['document'] = file_name
                    j = j+1
                i = i + 1
    else:
        advisor_transactions = ''
    logger.info(
        logme("listed all the transaction done in UPLYF by advisor",request)
    )
    if req_type == "mobile":
        return advisor_transactions
    else:
        return render(request, 'dashboard/manage_transaction.html', locals())


def load_send_group_email_modal(request):
    '''
    Description: open send email modal pop up
    '''
    if request.method == "GET":
        logger.info(
            logme("opened send group modal",request)
        )
        return render(request, "dashboard/send_group_email_modal.html", locals())


def list_enquiried_clients(request):
    '''
    Description: It retuns the list of client who enquiried the advisor
    '''
    if request.method == "POST":
        req_type = request.POST.get('req_type',None)
        user = request.user
        user_profile = user.profile
        advisor_name = user_profile.first_name+" "+user_profile.last_name
        advisor_id = user_profile.advisor.id
        advisor_email = user_profile.email
        enquiry_management_list = None
        enquired_members_data = list_client_enquiry(advisor_name,advisor_id,advisor_email)
        if enquired_members_data:
            enquiry_management_list = enquired_members_data['content']
        logger.info(
            logme("opened enquired list of members",request)
        )
        if req_type == "mobile":
            return enquiry_management_list
        else:
            return render(request, "dashboard/enquired_list_member_modal.html", locals())


def list_profile_viewed(request):
    '''
    Description: It retuns the list of client who viewed
    '''
    PAGE_TITLE = 'List Profile Viewed'
    user = request.user
    user_profile = user.profile
    # Getting data from NFDB
    profile_viewed_list = ProfileShareMapping.objects.filter(
        advisor = user_profile.advisor,
        viewed_page=constants.MY_IDENTITY
    ).select_related('viewed_user_profile')
    ad_chk_viewed_list = AdvChkProfileConnectMap.objects.filter(
        email=user_profile.email,
        action_type='view'
    ).select_related('user_profile').annotate(
        first_name=F('user_profile__first_name'),
        member_email=F('user_profile__email')
    ).values(
        'first_name',
        'member_email',
        'modified_date',
        'registration_type'
    )
    logger.info(
        logme("redirected to list profile viewed page",request)
    )
    return render(request, 'dashboard/list_profile_viewed.html', locals())


def list_connect_profile(request):
    '''
    Description: It retuns the list of client who viewed
    '''
    PAGE_TITLE = 'List Connect Profile'
    user = request.user
    user_profile = user.profile
    u_profile = None
    profile_viewed_list = AdvChkProfileConnectMap.objects.filter(
        email=user_profile.email, 
        action_type='connect'
    ).select_related('user_profile').annotate(
        first_name = F('user_profile__first_name'),
        member_email = F('user_profile__email')
    ).values(
        'first_name',
        'member_email',
        'modified_date',
    )
    logger.info(
        logme("redirected to list profile viewed page",request)
    )
    return render(request, 'dashboard/list_connect_profile.html', locals())


def upload_transaction_documents(request):
    '''
    Description: It uploads the transaction documents
    '''
    if request.method == "POST":
        uploaded_doc = request.FILES.get('r_trans_doc', None)
        reingo_trans_id = request.POST.get('r_trans_id', None)
        tran_doc = base64.b64encode(uploaded_doc.read())
        trans_details = upload_reingo_transaction_document(tran_doc, reingo_trans_id, uploaded_doc.name)
        if trans_details:
            return HttpResponse(True)
        else:
            return HttpResponse(False)


def get_filename_from_document_path(doc_path):
    sub_str1 =  doc_path.rfind("/")
    sub_str2 = doc_path[sub_str1+1:]
    sub_str3 = sub_str2.rfind(".")
    extention = sub_str2[sub_str3:]
    sub_str4 = sub_str2.find("_")
    sub_str2 = sub_str2[sub_str4+1:]
    sub_str5 = sub_str2.rfind("_")
    sub_str_filename = sub_str2[:sub_str5]
    sub_str6 = sub_str_filename.rfind("_")
    sub_str_filename = sub_str2[:sub_str6]+extention
    return sub_str_filename


def financial_tools(request):
    '''
    Description: save advisory specialization
    '''
    if request.method == 'POST':
        user = request.user
        user_profile = UserProfile.objects.get(user=user)
        advisor_details = Advisor.objects.get(user_profile = user_profile)
        advisor_details.financial_instruments = request.POST['hidden_input']
        advisor_details.save()
    return redirect('/my_identity/')


def video_shoot_request(request):
    '''
    Description: Update flag video_shoot_request and triggers email
    '''
    if request.method == 'POST':
        req_type = request.POST.get('req_type', None)
        microlearning_tittle = request.POST.get('microlearning_tittle', None)
        descrition_of_the_topic = request.POST.get('descrition_of_the_topic', None)
        microlearning_location = request.POST.get('microlearning_location', None)
        preffered_date_of_shoot = request.POST.get('preffered_date_of_shoot', None)
        animation_required = request.POST.get('animation_required', None)
        profile_obj = request.user.profile
        advisor_video_request, created = AdvisorVideoRequest.objects.get_or_create(
                    user_profile=profile_obj,video_title=microlearning_tittle,status=constants.VIDEO_PUBLISH_APPROVED)
        advisor_video_request.video_description=descrition_of_the_topic
        advisor_video_request.location=microlearning_location
        advisor_video_request.shoot_date=preffered_date_of_shoot
        advisor_video_request.status=animation_required
        advisor_video_request.save()

        try:
            context_dict = {
                'username': first_name
            }
            send_mandrill_email(
                'REIA_24_01',
                [email, ],
                context=context_dict,
            )
            logger.info(
                logme("Email sent successfully ", request)
            )
        except:
            logger.info(
                logme("Failed to send email to Advisor", request)
            )
        try:
            context_dict = {
                'advisor_name':first_name,
                'advisor_email':email,
                'mobile_number':mobile,
                'city':city
            }
            send_mandrill_email(
                'REIA_24_03',
                [settings.REIA_ADMIN_EMAIL, ],
                context=context_dict,
            )
            logger.info(
                logme("Email sent successfully ", request)
            )
        except:
            logger.info(
                logme("Failed to send email to cameramen", request)
            )
        try:
            context_dict = {
                'advisor_name':first_name,
                'advisor_email':email,
                'mobile_number':mobile,
                'city':city
            }
            send_mandrill_email(
                'REIA_24_02',
                ['admin@upwrdz.com', ],
                context=context_dict,
            )
            logger.info(
                logme("Email sent successfully ", request)
            )
        except:
            logger.info(
                logme("Failed to send email to admin", request)
            )
        if req_type == "mobile":
            return JsonResponse({'response':'success'}, status=200)
        else:
            return HttpResponse('success')


def get_video_request_modal(request):
    '''
    Description: Loading Video request modal
    '''
    return render(request, 'dashboard/video_request_modal.html', locals())


def advisor_video_upload(request):
    '''
    Description: Saving Advisor published youtube video link and description
    '''
    if request.method == 'POST':
        video_title = request.POST.get('video_title', None)
        video_description = request.POST.get('video_description', None)
        video_link = request.POST.get('video_url', None)
        req_type = request.POST.get('req_type', None)
        user_profile = request.user.profile
        published_video = AdvisorPublishedVideo(
            user_profile=user_profile,
            video_title=video_title,
            video_description=video_description,
            video_link=video_link,
            status=constants.VIDEO_PUBLISH_APPROVED
        )
        published_video.save()
        nf = NotificationFunctions(request, user_profile)
        nf.save_notification(notification_type=VIDEO_UPLOAD_SUCCESS)
        del(nf)
        logger.info(
            logme("Published video information saved", request)
        )
        if req_type == "mobile":
            return JsonResponse({'response':'success'}, status=200)
        else:
            return HttpResponse('success')
    else:
        return HttpResponse('Access forbidden')


def check_ebs_mandatory_details(request):
    '''
    Description: Cheking mandatory fields for EBS
    '''
    if request.method == 'POST':
        user_profile = request.user.profile
        advisor = user_profile.advisor
        if user_profile.mobile and user_profile.address and user_profile.city\
            and user_profile.pincode:
                return HttpResponse('success')
        else:
            return HttpResponse('failed')
    else:
        return HttpResponse('Access forbidden')


def try_premium_modal(request):
    '''
    Description: opens a premium modal of subscription
    '''
    if request.method == 'GET':
        logger.info(
            logme("try premium open modal",request)
        )
        return render(request, "dashboard/subscription.html", locals())


def micro_learning_packages_model(request):
    '''
    Description: opens the micro learning packages model
    '''
    if request.method == 'GET':
        type = sub_constant.SUB_CAT_MICRO_LEARNING_PACK
        ml_pkgs, sub_cat_id = get_pkg_list_by_type(type)
        ftr_odr_list = sub_constant.FEATURE_ORDET_LIST_FOR_MICRO_LEARNING
        logger.info(
            logme("micro_learning_packages_model",request)
        )
        return render(request, "dashboard/micro_learning_packages.html", locals())


def check_advisor_subscribed_to_create_video(request):
    '''
    Description: Gets the advisor's video subscription details
    '''
    result_status = False
    if request.method == 'POST':
        user_profile = request.user.profile
        ml_video_pkg = MicroLearningVideoPkg.objects.filter(\
            advisor_subscription_pkg__user_profile=user_profile,\
            advisor_subscription_pkg__subscription_status=sub_constant.ACTIVATED\
        )
        if ml_video_pkg:
            result_status = True
    return JsonResponse({'res':result_status}, status=200)


@permission_classes((AllowAny,))
class FollowingActivities(viewsets.ViewSet):
    '''
    Description: Advisor's following activities like follow, unfollow and do not follow
    '''
    def __init__(self):
        super(FollowingActivities, self).__init__()

    def follow_advisors(self, request):
        '''
        Description: Advisor sends follow request another advisor
        '''
        user_profile = request.user.profile
        user_profile_id = user_profile.id
        follewee_email = request.POST.get('follower_email', None)
        if user_profile_id and follewee_email:
            followee_obj = UserProfile.objects.filter(email=follewee_email).first()
            if followee_obj:
                follow_advisor, created = ActivityFollowers.objects.get_or_create(
                    user_profile = user_profile, followers = followee_obj)
                if follow_advisor.followers.email == follewee_email\
                        and follow_advisor.following_status == constants.FOLLOWING:
                            return HttpResponse('Already following', status = 205)
                else:
                    follow_advisor.following_status = constants.IN_PROGRESS
                    activation_key = generate_key()
                    follow_advisor.activation_key = activation_key
                    follow_advisor.save()
                    accept_url = constants.ACCEPT_URL+"?ack="+follow_advisor.activation_key+"&accepted=True"+"&code="+followee_obj.referral_code
                    reject_url = constants.ACCEPT_URL+"?ack="+follow_advisor.activation_key+"&accepted=False"+"&code="+followee_obj.referral_code
                    try:
                        send_mandrill_email(
                            'ABOTMI_21',
                            [followee_obj.email],
                            context = {
                                'followee_name' : followee_obj.first_name,
                                'follower_name' : user_profile.first_name,
                                'accept_url' : accept_url,
                                'reject_url' : reject_url,
                            }
                        )
                    except:
                        logger.debug('Mail failed while sending request to user')
                    return JsonResponse({
                        'id':followee_obj.id,
                        'name' : followee_obj.first_name,
                        'email' : follewee_email,
                        }, status = 200)
            else:
                return HttpResponse('User does not exist', status = 204)
        else:
            return HttpResponse('Try again later', status = 409)

    def follower_advisor_mapping(self, request):
        '''
        Description: Followee Accepts to map with followers advisor
        '''
        accepted = request.GET.get('accepted', None)
        activation_key = request.GET.get('ack', None)
        followee_code = request.GET.get('code', None)
        template_name = 'dashboard/follow_accept_or_reject.html'
        context_dict = {'url': settings.DEFAULT_DOMAIN_URL}
        if accepted and activation_key:
            followee_obj = UserProfile.objects.filter(referral_code = followee_code).first()
            follow_advisor = ActivityFollowers.objects.filter(
                activation_key=activation_key).first()
            if followee_obj and follow_advisor:
                notification_obj = NotificationFunctions(request, followee_obj)
                if accepted =='True':
                    follow_advisor.followers = followee_obj
                    follow_advisor.following_status = constants.FOLLOWING
                    follow_advisor.activation_key = ""
                    follow_advisor.save()
                    del(notification_obj)
                    context_dict['accept'] = True
                    context_dict['follow_advisor'] = follow_advisor
                    return render(request, template_name, context=context_dict)
                elif accepted == 'False':
                    follow_advisor.followers=followee_obj
                    follow_advisor.following_status=constants.REJECTED
                    follow_advisor.activation_key = ""
                    follow_advisor.save()
                    del(notification_obj)
                    context_dict['reject'] = True
                    context_dict['follow_advisor'] = follow_advisor
                    return render(request, template_name, context=context_dict)
            else:
                context_dict['expire'] = True
                return render(request, template_name, context=context_dict)
        else:
            context_dict['invalid'] = True
            return render(request, template_name, context=context_dict)

    def unfollow_advisors(self, request):
        '''
        Description: Advsior unfollows an advisor
        '''
        follewee_email = request.POST.get('advisor_email', None)
        followee_obj = UserProfile.objects.filter(email=follewee_email).first()
        if followee_obj and follewee_email:
            follow_advisor = ActivityFollowers.objects.filter(
                user_profile = request.user.profile, followers = followee_obj).first()
            if follow_advisor:
                follow_advisor.following_status = constants.UNFOLLOW
                follow_advisor.save()
                return JsonResponse({'message': 'Advisor chose - unfollow'}, status = 200)
            else:
                return JsonResponse({'message': 'Advisor did not choose'}, status = 200)
        else:
            return JsonResponse({'message':'Advisor does not exist'}, status = 204)

    def donot_follow_advisors(self, request):
        '''
        Description: Advsior says do not follow to an advisor
        '''
        follewee_email = request.POST.get('advisor_email', None)
        followee_obj = UserProfile.objects.filter(email=follewee_email).first()
        if followee_obj and follewee_email:
            follow_advisor = ActivityFollowers.\
                objects.filter(user_profile = followee_obj, followers = request.user.profile ).first()
            if follow_advisor:
                follow_advisor.following_status = constants.DISCONNECTED
                follow_advisor.save()
                return JsonResponse({'message': 'Advisor chose - do not follow'}, status = 200)
            else:
                return JsonResponse({'message': 'Advisor did not choose'}, status = 200)
        else:
            return JsonResponse({'message':'Advisor does not exist'}, status = 204)

    def view_followers(self, request):
        '''
        Description: List of followers
        '''
        user = request.user
        user_profile = user.profile
        email = user_profile.email
        UNFOLLOW = 1
        if user_profile:
            follow_advisor = ActivityFollowers.objects.filter(
                user_profile=user_profile).exclude(Q(following_status=constants.UNFOLLOW)|Q(following_status=constants.DISCONNECTED))
            return render(request, "dashboard/unfollow_advisor.html", locals())
        else:
            return render(request, "dashboard/unfollow_advisor.html", locals())

    def view_followees(self, request):
        '''
        Description: List of followees - do not follow
        '''
        title = 'view_followees'
        user = request.user
        user_profile = user.profile
        email = user_profile.email
        if user_profile:
            follow_advisors = ActivityFollowers.objects.filter(
                followers=user_profile).exclude(Q(following_status=constants.UNFOLLOW))
            if follow_advisors:
                followees_list = UserProfile.objects.filter(id__in=follow_advisors).values('first_name', 'email')
            return render(request, "dashboard/unfollow_advisor.html", locals())
        else:
            return render(request, "dashboard/unfollow_advisor.html", locals())


def save_calendly_link(request):
    '''
    Description: Method saves the Calendly link of the Advisor 
    '''
    if request.method == 'POST':
        advisor = request.user.profile.advisor
        calendly_link = request.POST.get('link', None)
        if calendly_link:
            advisor.calendly_link = calendly_link
            advisor.save()
            return JsonResponse({'message':'Advisor calendly link saved', 'status': 200})
        else:    
            return JsonResponse({'message':'calendly link not saved', 'status': 204})
