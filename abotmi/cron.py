import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reia.settings")
import django
django.setup()
import datetime
from signup.djmail import send_mandrill_email, send_mandrill_email_with_attachement
from datacenter.models import Advisor,UserProfile,TrackReferrals, TransactionsDetails
from common.constants import CRISIL_APPLIED, CRISIL_ACCOUNT_NAME, CRISIL_ACCOUNT_NUMBER, CRISIL_BANK_NAME, CRISIL_BANK_BRANCH, CRISIL_BANK_IFSC_CODE, CRISIL_URL_ONE, CRISIL_URL_TWO
from common.utils import send_sms_alert
from num2words import num2words

'''
for sending reminder mail to reffered advisors
'''
advisorcount = Advisor.objects.count()
trackreferrals = TrackReferrals.objects.all()
for trackreferral in trackreferrals:
    user_profile = UserProfile.objects.get(id=trackreferral.referred_by_id)
    context_dict = {
        'name': trackreferral.name,
        'advisor_name': user_profile.first_name,
        'no_of_advisors': advisorcount,
        'url':'https://abotmi.com'
    }
    send_mandrill_email('ABOTMI_14', [trackreferral.email], context=context_dict)

'''
for sending reminder mail to those,
who have not made payment for crisil certification
'''
advisor_list = Advisor.objects.filter(crisil_application_status=CRISIL_APPLIED)
for advisor_data in advisor_list:
    email_to_send = advisor_data.user_profile.email
    registration_id = advisor_data.user_profile.registration_id
    if advisor_data.user_profile.mobile:
        mobile_number=advisor_data.user_profile.mobile
    transaction = TransactionsDetails.objects.filter(user_profile = advisor_data.user_profile)
    final_amount = ''
    if transaction:
        final_amount = transaction[0].discounted_amount
        final_amount_in_words = num2words(final_amount, lang='en_IN')
    name = advisor_data.user_profile.first_name + ' '+advisor_data.user_profile.last_name
    date = str(datetime.datetime.now().strftime("%Y-%m-%d"))
    our_account_name = CRISIL_ACCOUNT_NAME
    our_account_number = CRISIL_ACCOUNT_NUMBER
    our_bank_name = CRISIL_BANK_NAME
    our_branch_name = CRISIL_BANK_BRANCH
    our_branch_IFSC_code = CRISIL_BANK_IFSC_CODE
    url_one = CRISIL_URL_ONE
    context_dict = {
        'Username': name,
        'date': date,
        'our_account_name': our_account_name,
        'our_account_number': our_account_number,
        'our_bank_name': our_bank_name,
        'our_branch_name': our_branch_name,
        'our_branch_IFSC_code': our_branch_IFSC_code,
        'url': url_one,
        'final_amount':final_amount,
        'final_amount_in_words':final_amount_in_words
    }
    send_mandrill_email('REIA_17_01', [email_to_send], context=context_dict)
    message = 'Dear '+name+' ('+registration_id+'),Payment towards CRISIL verification is still pending. Pls pay immediately for processing your application'
    sms_response = send_sms_alert(mobile_number=mobile_number,message_template=message)

'''
for sending reminder mail to signup users
'''
signup_advisors = Advisor.objects.filter(is_register_advisor=False)
for advisor in signup_advisors:
    userprofile = UserProfile.objects.get(email=advisor.user_profile)
    context_dict = {
        'name': userprofile.first_name
    }
    send_mandrill_email('ABOTMI_03', [userprofile.email], context=context_dict)

'''
for sending reminder mail to company for registration
'''
email_verification_obj = EmailVerification.objects.filter(user_profile__is_company=True)
for obj in email_verification_obj:
    userprofile = UserProfile.objects.get(id=obj.user_profile)
    send_mandrill_email('REIA_19_02', [userprofile.email], context={'url':settings.DEFAULT_DOMAIN_URL+"/company/?ack="+obj.activation_key})

'''
for sending reminder mail to SPOC
'''
email_verification_obj = CompanyAdvisorMapping.objects.values('company_user_profile').annotate(dcount=
Count('company_user_profile'))
for obj in email_verification_obj:
    userprofile = UserProfile.objects.get(id=obj.company_user_profiles)
    affiliated_company = AffiliatedCompany.objects.get(user_profile=userprofile)
    send_mandrill_email('REIA_19_05', [userprofile.email], context={'affiliate_name':userprofile.first_name,'company_name':affiliated_company.company_name})
