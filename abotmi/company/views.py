import json
import logging
import os
import pandas as pd
from pathlib2 import Path

# Django modules
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.utils.crypto import get_random_string

# Database models
from datacenter.models import (UserProfile, AffiliatedCompany, UploadDocuments, 
    EmailVerification, Advisor, CompanyAdvisorMapping)

# Local Imports
from signup.djmail import send_mandrill_email
from common import constants
from common.views import logme, create_user_from_uploaded_file
from company.tasks import bulk_advisor_data_creation
from company.serializers import BulkAdvisorDataSerializer

# Constatns
from common.api_constants import NEXT_URL_LINK

logger = logging.getLogger(__name__)

def index(request):
    '''
    Descrption:On clcik of company activation link we are navigating to Registration form.
    '''
    context_dict = { 'PRODUCT_NAME' : settings.PRODUCT_NAME }
    context = RequestContext(request)
    user = request.session.get('user')
    if request.method == 'GET':
        try:
            activation_key = request.GET['ack']
            verification = EmailVerification.objects.get(activation_key=request.GET['ack'])
            logger.info(
                logme("company activation link verified",request)
            )
        except:
            logger.info(
                logme("company activation link may be wrong or expired",request)
            )
            return HttpResponse("Activation link may be wrong or expired")
        user_auth_obj= User.objects.get(username=verification.user_profile.user.username)
        user_profile = ''
        user_profile = UserProfile.objects.filter(user = user_auth_obj)
        if user_profile:
            user_profile = user_profile[0]
        company = ''
        company = AffiliatedCompany.objects.filter(user_profile = user_profile)
        if company:
            company = company[0]
        request.session['user'] = user_auth_obj.username
        logger.info(
            logme("company user=%s redirected to company registration form after \
                activation"%(str(company)),request)
        )
        return render(request, 'company/add_affiliate.html', locals())

def add_affiliate(request):
    '''
    Descrption: Navigating to Company Registraion Form.
    '''
    PAGE_TITLE = 'Add Affiliate'
    logger.info(
        logme("company user redirected to company registration page",request)
    )
    return render(request, 'company/add_affiliate.html', locals())

def my_company_track(request):
    '''
    Descrption:Navigating to Company Profile(Track) Page.
    '''
    PAGE_TITLE = 'My Company Track'
    company_logo_url = ''
    awards_or_rewards = ''
    company_ob = AffiliatedCompany.objects.get(user_profile = request.user.profile)
    company_logo = UploadDocuments.objects.filter(
        documents_type = 'company_logo',
        user_profile = request.user.profile
    )
    if company_logo:
        company_logo_url = company_logo[0].documents.url
    if company_ob.awards_or_rewards:
        awards_or_rewards = json.loads(company_ob.awards_or_rewards)
    logger.info(
        logme("navigated to company my track page",request)
    )
    return render(request, 'company/my_company_track.html', locals())

def employees_details(request):
    '''
    Descrption:Sending Advisor List from Respected Company.
    '''
    PAGE_TITLE = 'Advisor Details'
    user = request.user
    user_profile = user.profile
    company_obj = AffiliatedCompany.objects.get(user_profile = user_profile)
    domain = company_obj.domain_name
    if domain:
        domain = '.'+domain
        company_users = UserProfile.objects.filter(advisor__questions__contains = domain)
        for profile in company_users:
            affiliate_company_child,status = CompanyAdvisorMapping.objects.get_or_create(
                advisor_user_profile = profile,
                company_user_profile = user_profile
            )
            if status:
                affiliate_company_child.status = constants.NOT_APPROVED
                affiliate_company_child.save()
    company_advisor_profile = CompanyAdvisorMapping.objects.filter(
        company_user_profile = user_profile
    )
    approved_advisors_count = company_advisor_profile.filter(
        status = constants.APPROVED
    ).count()
    not_approved_advisors_count = company_advisor_profile.filter(
        status = constants.NOT_APPROVED
    ).count()
    disown_advisor_count = company_advisor_profile.filter(
        status = constants.DIS_OWN
    ).count()
    logger.info(
        logme("listed company advisors from respective companies", request)
    )
    return render(request, 'company/employees_details.html', locals())

def save_add_affiliate_form(request):
    '''
    Descrption:Saving Regsitraion form and Generating credentials to particular Company.
    '''
    if request.method == 'POST':
        user = request.session.get('user')
        user_obj = User.objects.get(username = user)
        old_email_id = user_obj.username
        point_of_contact_email = request.POST.get('point_of_contact_email_id', None)
        company_name = request.POST.get('company_name', None)
        if point_of_contact_email:
            user_obj.username = point_of_contact_email
            user_obj.email = point_of_contact_email
            user_password = get_random_string(length=8)
            user_obj.set_password(user_password)
            user_obj.first_name = request.POST.get('point_of_contact_name', None)
            user_obj.save()
            user_profile = UserProfile.objects.filter(user = user_obj)
            if user_profile:
                user_profile = user_profile.first()
                user_profile.address = request.POST.get('re_office_address', None)
                user_profile.first_name = request.POST.get('point_of_contact_name', None)
                user_profile.email = point_of_contact_email
                user_profile.mobile = request.POST.get(
                    'point_of_contact_phone_number', None)
                user_profile.facebook_media = request.POST.get('facebook_media', None)
                user_profile.google_media = request.POST.get('google_media', None)
                user_profile.linkedin_media = request.POST.get('linkedin_media', None)
                user_profile.twitter_media = request.POST.get('twitter_media', None)
                user_profile.company_name = company_name
                user_profile.is_company = True
                user_profile.save()
                company_obj,created = AffiliatedCompany.objects.get_or_create(
                    user_profile = user_profile)
                company_obj.company_name = company_name
                address_json = {
                    'corporate_office': request.POST.get('co_office_address', ''),
                    'registration_office': request.POST.get('re_office_address', '')
                }
                company_obj.address = json.dumps(address_json)
                company_obj.tagline = request.POST.get('company_tagline', None)
                company_obj.website_url = request.POST.get('company_url', None)
                company_obj.objective = request.POST.get('company_objective', None)
                company_obj.description = request.POST.get('company_description', None)
                company_obj.awards_or_rewards = request.POST.get(
                    'all_awards_and_rewards', None)
                company_obj.corprate_identity_no = request.POST.get('cin_no', None)
                company_obj.number_client = request.POST.get('no_of_clients', None)
                company_obj.number_of_employee = request.POST.get('no_of_employees', None)
                if request.POST['terms_and_conditions']:
                    company_obj.terms_and_conditions = True
                upload_documents, status = UploadDocuments.objects.get_or_create(
                    documents_type = 'company_logo',
                    user_profile = user_profile
                )
                upload_documents.documents = request.FILES['company_logo']
                company_obj.logo = upload_documents.documents
                upload_documents.save()
                company_obj.save()
                upload_document_e_brochure, is_created = UploadDocuments.objects.get_or_create(
                    documents_type = 'e_brochure',
                    user_profile = user_profile
                )
                upload_document_e_brochure.documents = request.FILES['company_e_brochure']
                upload_document_e_brochure.save()
                domain = company_obj.domain_name
                if domain:
                    domain = '.'+domain
                    company_users = UserProfile.objects.filter(
                        advisor__questions__contains = domain)
                    for profile in company_users:
                        affiliate_company_child,status = CompanyAdvisorMapping.objects.get_or_create(
                            advisor_user_profile = profile,
                            company_user_profile = user_profile
                            )
                        if status:
                            affiliate_company_child.status = constants.NOT_APPROVED
                            affiliate_company_child.save()
                activation_key = request.POST['activation_key']
                verification = EmailVerification.objects.get(activation_key=activation_key)
                verification.delete()
                context_dict = {
                    'affiliate_name': user_profile.first_name,
                    'username': user_profile.email,
                    'url':NEXT_URL_LINK,
                    'password': user_password
                }
                send_mandrill_email('REIA_19_03', [user_profile.email], context=context_dict)
                # need to send emails using cron(this is for next release)
                # send_mandrill_email('REIA_19_04', [user_profile.email], context={'affiliate_name':user_profile.first_name,'company_name':company_name})
                logger.info(
                    logme("registration form data saved & generated credentials for\
                     company, mail sent ", request)
                )
                return HttpResponseRedirect('/')
            else:
                logger.error(
                logme("unable to register company, company userprofile not found", request)
                )
                return HttpResponse('Unable to create Your company. Please try again \
                    after some time')
        else:
            logger.error(
                logme("unable to register company, company email not found", request)
            )
            return HttpResponse('Error')
    else:
        return HttpResponse('Access forbidden')


def fetch_advisor_details(request):
    '''
    Descrption:Sending advisor information.
    '''
    if request.method == 'POST':
        index = 0
        user_profile = UserProfile.objects.filter(id = request.POST['id'])
        if user_profile:
            user_profile = user_profile.first()
            advisor = Advisor.objects.filter(user_profile = user_profile)
            if advisor:
                advisor = advisor.first()
                advisor_company_email = ''
                result = constants.DETAILS_NOT_FOUND
                if advisor.questions:
                    question  = json.loads(advisor.questions)
                    for i in question[2]['Remark'][0]['Remark']:
                        index +=1
                        if request.POST['domain'] in i['Answer']:
                            advisor_company_email = i['Answer']
                            result = constants.DETAILS_FOUND
                            registration_no=question[2]['Remark'][0]['Remark'][index]['Answer']
                    response = {
                        'status':result,
                        'advisor_company_email' : advisor_company_email,
                        'advisor_company_registration':registration_no,
                        'profile_pic' : user_profile.picture.url if user_profile.picture else None
                    }
            else:
                response = { 'status':constants.DETAILS_NOT_FOUND }
                logger.info(
                    logme("advisors not found for company",request)
                )
        else:
            logger.info(
                logme("advisor not found for company",request)
            )
            response = { 'status':constants.DETAILS_NOT_FOUND }
        logger.info(
            logme("fetching advisor details for company",request)
        )
        return JsonResponse(response)
    else:
        logger.info(
            logme("GET request - access forbidden to fetch advisors", request)
        )
        return HttpResponse('Access forbidden')


def update_company_details(request):
    '''
    Descrption:Updating Company Profile(Track) information.
    '''
    if request.method == 'POST':
        user = request.user
        user_profile = user.profile
        company_obj = AffiliatedCompany.objects.filter(user_profile = user_profile).first()
        if company_obj:
            company_obj.company_name = request.POST['company_name']
            company_obj.tagline = request.POST['company_tagline']
            company_obj.website_url = request.POST['company_url']
            company_obj.objective = request.POST['company_objective']
            company_obj.description = request.POST['company_description']
            company_obj.awards_or_rewards = request.POST['all_awards_and_rewards']
            company_obj.save()
            user_profile.street_name = request.POST['company_address']
            user_profile.address = request.POST['address_line_2']
            user_profile.locality = request.POST['location']
            user_profile.city = request.POST['city']
            user_profile.state = request.POST['state']
            user_profile.first_name = request.POST['point_of_contact_name']
            user_profile.mobile = request.POST['point_of_contact_phone_number']
            user_profile.facebook_media = request.POST['facebook_media']
            user_profile.google_media = request.POST['google_media']
            user_profile.linkedin_media = request.POST['linkedin_media']
            user_profile.twitter_media = request.POST['twitter_media']
            user_profile.company_name = request.POST['company_name']
            user_profile.save()
            user.first_name = request.POST['point_of_contact_name']
            user.save()
            logger.info(
                logme("updated company profile information",request)
            )
            return HttpResponse('success')
        else:
            logger.info(
                logme("updating company profile information failed",request)
            )
            return HttpResponse('failed')
    else:
        logger.info(
            logme("GET request - access forbidden to update company information",request)
        )
        return HttpResponse('Access forbidden')


def check_email_exist_or_not(request):
    '''
    Checking Email is exists or not
    '''
    if request.method == 'POST':
        if request.POST['value'] == 'company_reg':
            user = request.session.get('user')
            user = User.objects.get(username = user)
            username = request.POST['username']
            if not username == user.username:
                user_obj = User.objects.filter(username = username)
                if user_obj:
                    logger.info(
                        logme("validation - email exist for creating company", request)
                    )
                    return HttpResponse('exist')
                else:
                    logger.info(
                        logme("validation - email does not exist for creating company", request)
                    )
                    return HttpResponse('new_user')
            else:
                logger.info(
                    logme("validation - email does not exist for creating company", request)
                )
                return HttpResponse('user_email')
    else:
        logger.info(
            logme("GET request - access forbidden for checking email validation for \
                creating company", request)
        )
        return HttpResponse('Access forbidden')


def update_affiliate_company_status(request):
    '''
    Description:Company Can Approve the Advisors who all are under comming him.
        (company will check advisors company email id is correct or not)
    '''
    if request.method == 'POST':
        user_profile_id = request.POST['id']
        user_profile = UserProfile.objects.filter(id = user_profile_id)
        affiliated_company_status = CompanyAdvisorMapping.objects.filter(
            company_user_profile = request.user.profile,
            advisor_user_profile_id = user_profile_id
        )
        company = AffiliatedCompany.objects.filter(user_profile= request.user.profile)
        if affiliated_company_status:
            if (request.POST['status'] == constants.DIS_OWN 
                or request.POST['status'] == constants.NOT_APPROVED):
                affiliated_company_status[0].status =constants.APPROVED
                logger.info(
                    logme("advisor approved/owned by company", request)
                )
                if request.POST['status'] == constants.DIS_OWN:
                    affiliated_company_status[0].remarks = request.POST['feedback']
                affiliated_company_status[0].save()
                try:
                    send_mandrill_email(
                        'REIA_19_06', 
                        [user_profile[0].email], 
                        context={'advisor_name':user_profile[0].first_name}
                    )
                    logger.info(
                        logme("sent mail after advisor approval/owning by company",request)
                    )
                except:
                    logger.error(
                        logme("failed to send mail after advisor approval by company", 
                            request)
                    )
                    return HttpResponse('mailfailed')
            if request.POST['status'] == constants.APPROVED:
                logger.info(
                    logme("advisor disowned by company", request)
                )
                affiliated_company_status[0].status = constants.DIS_OWN
                affiliated_company_status[0].remarks = request.POST['feedback']
                affiliated_company_status[0].save()
                try:
                    send_mandrill_email(
                        'REIA_19_07', 
                        [user_profile[0].email], 
                        context={
                            'advisor_name':user_profile[0].first_name,
                            'company_name':company[0].company_name
                        }
                    )
                    logger.info(
                        logme("sent mail after advisor disowned by company",request)
                    )
                except:
                    logger.error(
                        logme("failed to send mail after advisor disowned by company",request)
                    )
                    return HttpResponse('mailfailed')
        return HttpResponse('success')


def why_we_are_asking(request):
    '''
    Navigating to why_we_are_asking html 
    '''
    logger.info(
        logme("redirected to company why we are asking page", request)
    )
    return render(request, 'company/why_we_are_asking.html',locals())


def confidence_assurance(request):
    '''
    Navigating to confidence_assurance html 
    '''
    logger.info(
        logme("redirected to company confidence assurance page", request)
    )
    return render(request, 'company/confidence_assurance.html',locals())


def change_password(request):
    '''
    Navigating to changepassword html
    '''
    PAGE_TITLE = 'Change Password'
    context = RequestContext(request)
    logger.info(
        logme("redirected to change Password page",request)
    )
    return render_to_response("company/changepassword.html",context)


def get_in_touch(request):
    '''
    Navigating company get_in_touch html
    '''
    PAGE_TITLE = 'Get in touch'
    context = RequestContext(request)
    hide_signup_popup=1
    logger.info(
        logme("redirected to company get in touch page",request)
    )
    return render_to_response("company/get_in_touch.html",context)


def get_not_approved_advsors_list(request):
    '''
    Fetching not_approved advisors list under company.
    '''
    if request.method == 'POST':
        not_approved_list = CompanyAdvisorMapping.objects.filter(\
            company_user_profile = request.user.profile,
            status = constants.NOT_APPROVED
            )
        logger.info(
            logme("fetching not approved advisors list under company",request)
        )
        return render(request, 'company/not_approved_advisors.html', locals())
    else:
        logger.info(
            logme("GET request - access forbidden for fetching not approved advisors list\
             under company",request)
        )
        return HttpResponse('Access forbidden')


def get_approved_advisor_list(request):
    '''
    Fetching approved advisors list under company
    '''
    if request.method == 'POST':
        approved_list = CompanyAdvisorMapping.objects.filter(
            company_user_profile = request.user.profile,
            status = constants.APPROVED
            )
        logger.info(
            logme("fetching approved advsiors list under company", request)
        )
        return render(request, 'company/approved_advisors.html', locals())
    else:
        logger.info(
            logme("GET request - access forbidden for fetching approved advsiors list \
            under company", request)
        )
        return HttpResponse('Access forbidden')


def get_disown_advisors_list(request):
    '''
    Fetching disown advisors list under company
    '''
    if request.method == 'POST':
        disown_list = CompanyAdvisorMapping.objects.filter(
            company_user_profile = request.user.profile,
            status = constants.DIS_OWN
            )
        logger.info(
            logme("fetching disowned advisors list under company", request)
        )
        return render(request, 'company/disown_advisor.html', locals())
    else:
        logger.info(
            logme("GET request - access forbidden for fetching disowned advisors list \
            under company",request)
        )
        return HttpResponse('Access forbidden')


def upload_advisors_data(request):
    '''
    Upload Advisors data in excel format
    Used by the company user
    '''
    user_profile=request.user.profile
    file_to_upload = request.FILES['documents_advisor_list']
    documents_new_upload = UploadDocuments.objects.create(
            user_profile=user_profile
        )
    documents_new_upload.documents = request.FILES['documents_advisor_list']
    documents_new_upload.documents_type = 'advisor_data_excel'
    documents_new_upload.save()
    document_url = str(documents_new_upload.documents)
    if document_url:
        if user_profile:
            filename = 'temp_bulk_advisor_data_{}.xlsx'.format(randint(0,100000))
            if not Path(filename).is_file():
                file_open=default_storage.open(document_url,'r')
                with open(filename, "wb") as fh:
                    fh.write(file_open.read())
                    fh.close()
                advisor_data = pd.read_excel(str(filename))
                serializer = BulkAdvisorDataSerializer(advisor_data)
                os.remove(filename)
                bulk_advisor_data_creation.apply_async((serializer.data, user_profile.id,))
        else:
            message="user_profile not found"
        message = "success"
    else:
        message = "Please try again later!!"
    return HttpResponseRedirect("/company/my_company_track/")
