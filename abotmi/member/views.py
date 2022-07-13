# python lib
import logging
import mimetypes
import base64
from mimetypes import MimeTypes

# Django modules
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.generic import View
from django.core.files.storage import default_storage

# Database models
from advisor_check.models import AdvisorData
from datacenter.models import (
    UserProfile, Member, Advisor, GetAdvice, GiveAdvice, UploadDocuments, UserStatus,
    Country
)

# Local imports
from common import constants
from common.notification.constants import ADVICE_REQ
from common.notification.views import NotificationFunctions
from common.utils import generate_key
from common.views import logme, UploadDocumentsFunctions, generate_pdf
from login.decorators import active_and_advisor
from signup.djmail import (
    send_mandrill_email, send_mandrill_email_with_attachement,
    send_mandrill_email_with_mul_attachement
)

# Constatns
from common.api_constants import (
    GOOGLE_SINGLE_URL, FACEBOOK_SINGLE_URL, LINKEDIN_SINGLE_URL
)

# Rest framework imports
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

logger = logging.getLogger(__name__)


class MemberIndexClass(View):

    def get(self, request, *args, **kwargs):
        '''
        Description: Function for navigating to member base html
        '''
        total_advisor = AdvisorData.objects.all().values('name').count()
        advisor_type_ca = AdvisorData.objects.filter(
            category__contains='CA').values('name').count()
        advisor_type_mfa = AdvisorData.objects.filter(
            category__contains='mutual_fund').values('name').count()
        advisor_type_ia = AdvisorData.objects.filter(
            category__contains='insurance').values('name').count()
        advisor_type_other = AdvisorData.objects.filter(
            category='other').values('name').count()
        ad_chk_name = request.session.get('ad_chk_name', None)
        ad_chk_email = request.session.get('ad_chk_email', None)
        ad_chk_mobile = request.session.get('ad_chk_mob', None)
        ad_chk_loc = request.session.get('ad_chk_loc', None)
        ad_chk_country = request.session.get('ad_chk_country', None)
        ad_chk_reg = request.session.get('ad_chk_reg', None)
        country = Country.objects.all().values('name', 'code')
        LOGIN_URL = settings.LOGIN_URL
        return render(request, 'advisor_check/home.html', locals())


class GetFormAdviceClass(View):

    def get(self, request, *args, **kwargs):
        '''
        Description: Function for navigating to Get Advice html
        '''
        advisor_id = request.GET.get('adv_id', None)
        advisor_name = request.GET.get('adv_name', None)
        advisor_email = request.GET.get('advisor_email', None)
        inv_chk_login = request.session.get('inv_chk_login', None)
        social_auth_ses = request.session.get('social_auth_ses', None)
        logger.info(
            logme("redirected to get advice page", request)
        )
        return render(request, "member/get_advice.html", locals())

    def post(self, request, *args, **kwargs):
        '''
        Description: Getting the Details and uploaded documents save
        '''
        user_profile = request.user.profile
        title = request.POST.get('title', None)
        advisor_id = request.POST.get('advisor_id', None)
        advisor_name = request.POST.get('advisor_name', None)
        advisor_email = request.POST.get('advisor_email', None)
        message = request.POST.get('message', None)
        document_ids = request.POST.get('document_ids', None)
        inv_chk_login = request.session.get('inv_chk_login', None)
        social_auth_ses = request.session.get('social_auth_ses', None)
        get_advice, created = GetAdvice.objects.get_or_create(
            question_title=title,
            user_profile=user_profile
        )
        if created:
            get_advice.description = message
            get_advice.document_ids = document_ids
            if advisor_email:
                get_advice.advisor_email = advisor_email
                advisor_profile = UserProfile.objects.filter(email=advisor_email).first()
                if advisor_profile:
                    # Saving Notification
                    nf = NotificationFunctions(request, receive=advisor_profile)
                    nf.save_get_advice(
                        notification_type=ADVICE_REQ,
                        sender=user_profile,
                        advice_id=get_advice.id)
                    del(nf)
            get_advice.save()
            try:
                attachement_arr = []
                if document_ids:
                    document_ids = document_ids.split(',')
                    docs = UploadDocuments.objects.filter(id__in=document_ids)
                    for doc in docs:
                        if doc and doc.documents:
                            p = doc.documents
                            content_type = mimetypes.guess_type(p.url)
                            try:
                                slash_indx = p.name.rindex('/')
                                name = p.name[slash_indx+1:]
                            except:
                                name = p.name
                            fo = default_storage.open(str(p), "rb")
                            filecontent = fo.read()
                            pdf = base64.b64encode(filecontent)
                            attachement = {
                                'type': content_type,
                                'content': pdf,
                                'name': name
                            }
                            attachement_arr.append(attachement)
                adv_context_dict = {
                    'advisor_name': advisor_name,
                    'member_name': user_profile.first_name,
                    'member_email': user_profile.email,
                    'query_title': title,
                    'query_description': message,
                }
                send_mandrill_email_with_mul_attachement(
                    'ABOTMI_29',
                    [advisor_email],
                    context=adv_context_dict,
                    attachements=attachement_arr
                )
                inst_context_dict = {
                    'advisor_name': advisor_name,
                    'member_name': user_profile.first_name,
                }
                send_mandrill_email(
                    'ABOTMI_28',
                    [user_profile.email],
                    context=inst_context_dict
                )
                logger.info(
                    logme('sent advice to email', self.request)
                )
            except Exception as e:
                message = "Unable to send"
                logger.info(
                    logme('unable to send advice to email exception:%s' % (
                        e), self.request)
                )
        if social_auth_ses and inv_chk_login:
            logout(request)
        logger.info(
            logme('Saving the Get advice form details', request)
            )
        return HttpResponse("success")


def get_advice(request):
    '''
    Description: Navigating to get_advice html
    '''
    logger.info(
        logme("redirected to get advice page", request)
    )
    return render(request, "member/get_advice.html", locals())


@active_and_advisor
def get_questions_list(request):
    '''
    Description : List the questions
    '''
    title = 'Give Advice'
    user_profile = request.user.profile
    get_advice_obj = GetAdvice.objects.filter(
        advisor_email=user_profile.email).order_by('-created_date')
    context_data = {
        'title': title,
        'get_advice_obj': get_advice_obj
    }
    return render(request, "member/give_advice.html", context=context_data)


@active_and_advisor
def read_more_answer(request):
    '''
    Description: read more on the particular question
    '''
    if request.method == 'GET':
        question_id = request.GET.get('question_id', None)
        get_advice_obj = GetAdvice.objects.filter(id=question_id).first()
        give_advice_obj = GiveAdvice.objects.filter(question=get_advice_obj)
        answer_obj = None
        if give_advice_obj:
            for obj in give_advice_obj:
                if obj.user_profile.id == get_advice_obj.user_profile.id:
                    answer_obj = True
        return render(request, "member/read_more_answers.html", locals())


@active_and_advisor
def answers_archive(request):
    '''
    Description: Searching for the answers and returning
    '''
    if request.method == 'GET':
        page_number = request.GET.get('search', None)
        archive = None
        if request.is_ajax():
            archive = GetAdvice.objects.filter(Q(question_title__icontains=page_number))
        template = 'member/drop_down_question_list.html'
        data = {'archives': archive}
        return render_to_response(
            template, data, context_instance=RequestContext(request))


def get_member_response(request):
    '''
    Description : Saves members acceptance for the answers
    '''
    title = 'Member_responce'
    if request.method == "GET":
        accepted = request.GET.get('accepted', None)
        activation_key = request.GET.get('ack', None)
        member_code = request.GET.get('code', None)
        question_id = request.GET.get('q_id', None)
        user_profile = UserProfile.objects.filter(referral_code=member_code).first()
        get_advice_obj = GetAdvice.objects.filter(
            id=question_id, user_profile=user_profile).first()
        give_advice_obj = GiveAdvice.objects.filter(
            question=get_advice_obj, activation_key=activation_key).first()
        try:
            if request.user.profile.is_advisor:
                return HttpResponse("<h1>You are not member <a href='%s'>Click here to\
                    return home</a></h1>" % settings.LOGIN_REDIRECT_URL)
        except:
            pass
        if give_advice_obj:
            if accepted == "True":
                give_advice_obj.status = constants.ACCEPTED
                answer_true = True
                batch_code_obj = give_advice_obj.user_profile
                advisor_status = UserStatus.objects.filter(
                    user_profile=user_profile).first()
                PROFILE_URL = None
                if batch_code_obj.batch_code:
                    # url = constants.SHOW_PROFILE_URL+"?slug="+batch_code_obj.batch_code
                    url = settings.DEFAULT_DOMAIN_URL+'/profile/'+batch_code_obj.batch_code
                give_advice_obj.save()
                return render(request, 'member/member_advice_rating.html', locals())
            else:
                give_advice_obj.status = constants.REJECTED
                answer_true = False
                give_advice_obj.save()
                return render(request, 'member/member_advice_rating.html', locals())
        else:
            return HttpResponse('This link has expired.', status=200)


@permission_classes((AllowAny,))
def get_profile_details(request, slug=None):
    '''
    Description: Show the profile detials
    '''
    if request.method == "GET":
        title = 'Profile_details'
        recaptcha_key = constants.RECAPTCHA_KEY
        slug = request.GET.get('slug', None)
        if slug:
            user_profile = UserProfile.objects.filter(
                batch_code=slug).first()
            if advisor_obj:
                advisor_user_profile = user_profile
                advisor_user_status, is_created = UserStatus.objects.get_or_create(
                    user_profile=advisor_user_profile)
                if is_created:
                    advisor_user_status.my_identity_status = True
                    advisor_user_status.my_repute_status = False
                    advisor_user_status.save()
                url = settings.DEFAULT_DOMAIN_URL + '/my_identity/'
                logger.info(
                    logme("redirected to the upwrdz shared profile", request)
                )
                return render(request, 'signup/guest_details.html', locals())
            else:
                return HttpResponse(
                    '<h1>Unable to view Profile. Check the URL once.</h1>')
        else:
            logger.info(
                logme("failed to redirected to the upwrdz shared profile", request)
            )
            return HttpResponse('<h1>Unable to view Profile. Please try again after \
                sometime</h1>')


@permission_classes((AllowAny,))
def get_member_rating(request):
    '''
    Description : Saves rating for advisor's answer
    '''
    if request.method == "POST":
        activation_key = request.POST.get('ack', None)
        member_code = request.POST.get('member_code', None)
        members_remarks = request.POST.get('member_remarks', None)
        question_id = request.POST.get('question_id', None)
        member_rating_level = request.POST.get('member_rating_level', None)
        if activation_key:
            user_profile = UserProfile.objects.filter(referral_code=member_code).first()
            get_advice_obj = GetAdvice.objects.filter(
                id=question_id,
                user_profile=user_profile
            ).first()
            give_advice_obj = GiveAdvice.objects.filter(
                    question=get_advice_obj, activation_key=activation_key).first()
            if give_advice_obj:
                if member_rating_level and not members_remarks:
                    give_advice_obj.rating = member_rating_level
                elif members_remarks and not member_rating_level:
                    give_advice_obj.remarks = members_remarks
                give_advice_obj.activation_key = ''
                give_advice_obj.save()
                return JsonResponse({'message': 'submitted'}, status=200)
            else:
                return HttpResponse('Already submitted.', status=204)
        else:
            return HttpResponse('This link has expired.', status=204)


@permission_classes((AllowAny,))
def connect_advisor(request):
    '''
    Description: Connects investor to the advisor
    '''
    if request.method == "POST":
        member_code = request.POST.get('member_code', None)
        question_id = request.POST.get('q_id', None)
        user_profile = UserProfile.objects.filter(referral_code=member_code).first()
        get_advice_obj = GetAdvice.objects.filter(
            id=question_id,
            user_profile=user_profile
        ).first()
        give_advice_obj = GiveAdvice.objects.filter(question=get_advice_obj).first()
        description = None
        email = give_advice_obj.user_profile.email
        try:
            send_mandrill_email(
                'ABOTMI_25',
                [email],
                context={
                    'name': user_profile.first_name,
                    'description': description,
                }
            )
        except:
            logger.debug('Mail failed while sending request to user')
        return JsonResponse({'message': 'connect'}, status=200)


@permission_classes((IsAuthenticated,))
class GiveAdviceClass(viewsets.ViewSet):
    '''
    Description: Advisor's forum for giving advices for the questions
    '''
    def __init__(self):
        super(GiveAdviceClass, self).__init__()

    def get_questions_lists(self, request):
        '''
        Description: List the questions
        '''
        get_advice_obj = GetAdvice.objects.all()[:5]
        return render(request, "member/give_advice.html", local())

    def view_all_answers(self, request):
        '''
        Description: View all answers to the specific questions
        '''
        question_ids = request.POST.get('view_question_id', None)
        question_id = request.POST.get('question_id', None)
        get_advice_obj = GetAdvice.objects.filter(id=question_id).first()
        give_advice_obj = GiveAdvice.objects.filter(question=get_advice_obj)
        return render(request, "member/view_all_answers.html", locals())

    def submit_advice(self, request):
        '''
        Description: Submit the advice for the particular question
        '''
        if request.method == 'POST':
            user_profile = request.user.profile
            advice = request.POST.get('advice', None)
            question_id = request.POST.get('question_id', None)
            give_advice_doc = request.POST.get('give_advice_doc', None)
            pdf_attachement = None
            pdf_attachements = None
            get_advice_obj = GetAdvice.objects.filter(id=question_id).first()
            give_advice_obj = GiveAdvice.objects.create(
                user_profile=request.user.profile, question=get_advice_obj)
            if give_advice_obj:
                give_advice_obj.answer = advice
                activation_key = generate_key()
                give_advice_obj.activation_key = activation_key
                give_advice_obj.document_ids = give_advice_doc
                give_advice_obj.save()
                accept_rate_url = constants.ADVICE_STATUS_URL+"?ack="\
                    + give_advice_obj.activation_key+"&accepted=True"+"&code="\
                    + get_advice_obj.user_profile.referral_code+"&q_id="+question_id
                remarks_url = constants.ADVICE_STATUS_URL+"?ack="\
                    + give_advice_obj.activation_key+"&accepted=False"+"&code="\
                    + get_advice_obj.user_profile.referral_code+"&q_id="+question_id
                try:
                    send_mandrill_email_with_attachement(
                        'ABOTMI_22',
                        [get_advice_obj.user_profile.email],
                        pdf_attachement,
                        context={
                            'member_name': get_advice_obj.user_profile.first_name,
                            'advisor_name': user_profile.first_name,
                            'description': advice,
                            'accept_rate_url': accept_rate_url,
                            'remarks_url': remarks_url,
                        }
                    )
                except:
                    logger.debug('Mail failed while sending request to user')
            return HttpResponse('You have submitted the advice', status=200)

    def download_docs(self, request):
        '''
        Description: Download the docs related to the question uploaded by the questioner
        '''
        if request.method == 'POST':
            question_id = request.POST.get('question_id', None)
            advisor_doc = None
            if question_id:
                document_list = None
                get_advice_obj = GetAdvice.objects.filter(id=question_id).first()
                if get_advice_obj.document_ids:
                    doc_id = get_advice_obj.document_ids.split(',')
                    document = UploadDocumentsFunctions(
                        request,
                        get_advice_obj.user_profile
                    )
                    document_list = document.get_document(doc_id=doc_id, many=True)
                if get_advice_obj:
                    docs = UploadDocuments.objects.filter(
                        user_profile=get_advice_obj.user_profile,
                        documents_type="GET_ADVICE"
                    )
                    advisor_doc = True
                return render(request, "member/view_documents.html", locals())

    def download_advisors_docs(self, request):
        '''
        Description: Download the docs related to the question uploaded by the advisors
        '''
        if request.method == 'POST':
            answer_id = request.POST.get('answer_id', None)
            if answer_id:
                document_list = None
                give_advice_obj = GiveAdvice.objects.filter(id=answer_id).first()
                if give_advice_obj.document_ids:
                    doc_id = give_advice_obj.document_ids.split(',')
                    document = UploadDocumentsFunctions(
                        request,
                        give_advice_obj.user_profile
                    )
                    document_list = document.get_document(doc_id=doc_id, many=True)
                    del(document)
                return render(request, "member/view_documents.html", locals())
