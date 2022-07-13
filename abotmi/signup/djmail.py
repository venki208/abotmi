from django.conf import settings
from django_mandrill.mail import MandrillTemplateMail
from common.constants import FACEBOOK_PAGE_URL, GOOGLE_PLUS_PAGE_URL, LINKEDIN_PAGE_URL, \
    TWITTER_PAGE_URL


# ========================================================================
# Common function for Mandrill Mail
# ========================================================================
def send_mandrill_email(template_name, email_to, context, curr_site=None):
    if context is None:
        context = {}
    message = {
        'to': [],
        'global_merge_vars': []
    }
    for em in email_to:
        message['to'].append({'email': em})
    for k, v in context.items():
        message['global_merge_vars'].append({'name': k, 'content': v})
    message['global_merge_vars'].append(
        {'name': 'upwrdz_redirect_url', 'content': settings.DEFAULT_DOMAIN_URL})
    # appending social media urls
    message['global_merge_vars'].append(
        {'name': 'upwrdz_facebook_url', 'content': FACEBOOK_PAGE_URL})
    message['global_merge_vars'].append(
        {'name': 'upwrdz_googleplus_url', 'content': GOOGLE_PLUS_PAGE_URL})
    message['global_merge_vars'].append(
        {'name': 'upwrdz_linkedin_url', 'content': LINKEDIN_PAGE_URL})
    message['global_merge_vars'].append(
        {'name': 'upwrdz_twitter_url', 'content': TWITTER_PAGE_URL})
    MandrillTemplateMail(template_name, [], message).send()


# ========================================================================
# Common function for Mandrill Mail with attachement
# ========================================================================
def send_mandrill_email_with_attachement(template_name, email_to, attachement, context):
    if context is None:
        context = {}
    message = {
        'to': [],
        'global_merge_vars': [],
        'attachments': []
    }
    for em in email_to:
        message['to'].append({'email': em})
    for k, v in context.items():
        message['global_merge_vars'].append({'name': k, 'content': v})
    message['global_merge_vars'].append(
        {'name': 'upwrdz_redirect_url', 'content': settings.DEFAULT_DOMAIN_URL})
    message['attachments'].append(attachement)
    # appending social media urls
    message['global_merge_vars'].append(
        {'name': 'upwrdz_facebook_url', 'content': FACEBOOK_PAGE_URL})
    message['global_merge_vars'].append(
        {'name': 'upwrdz_googleplus_url', 'content': GOOGLE_PLUS_PAGE_URL})
    message['global_merge_vars'].append(
        {'name': 'upwrdz_linkedin_url', 'content': LINKEDIN_PAGE_URL})
    message['global_merge_vars'].append(
        {'name': 'upwrdz_twitter_url', 'content': TWITTER_PAGE_URL})
    MandrillTemplateMail(template_name, [], message).send()

# ========================================================================
# Common function for Mandrill Mail with MULTIPLE attachement
# ========================================================================
def send_mandrill_email_with_mul_attachement(template_name, email_to, attachements, context):
    if context is None:
        context = {}
    message = {
        'to': [],
        'global_merge_vars': [],
        'attachments': []
    }
    for em in email_to:
        message['to'].append({'email': em})
    for k, v in context.items():
        message['global_merge_vars'].append({'name': k, 'content': v})
    message['global_merge_vars'].append(
        {'name': 'upwrdz_redirect_url', 'content': settings.DEFAULT_DOMAIN_URL})
    message['attachments'] = attachements
    # appending social media urls
    message['global_merge_vars'].append(
        {'name': 'upwrdz_facebook_url', 'content': FACEBOOK_PAGE_URL})
    message['global_merge_vars'].append(
        {'name': 'upwrdz_googleplus_url', 'content': GOOGLE_PLUS_PAGE_URL})
    message['global_merge_vars'].append(
        {'name': 'upwrdz_linkedin_url', 'content': LINKEDIN_PAGE_URL})
    message['global_merge_vars'].append(
        {'name': 'upwrdz_twitter_url', 'content': TWITTER_PAGE_URL})
    MandrillTemplateMail(template_name, [], message).send()

# =======================================================================
# Sending mail to admin of REAF(contact@reafglobal.com) with reply-to
# =======================================================================
def send_mandrill_email_admin(template_name, email_to, user_email, context, curr_site=None):
    if context is None:
        context = {}
    message = {
        'to': [],
        'headers': {},
        'global_merge_vars': []
    }
    for em in email_to:
        message['to'].append({'email': em})
        message['headers'] = {'Reply-To': user_email}
    for k, v in context.items():
        message['global_merge_vars'].append({'name': k, 'content': v})
    message['global_merge_vars'].append(
        {'name': 'upwrdz_redirect_url', 'content': settings.DEFAULT_DOMAIN_URL})
    # appending social media urls
    message['global_merge_vars'].append(
        {'name': 'upwrdz_facebook_url', 'content': FACEBOOK_PAGE_URL})
    message['global_merge_vars'].append(
        {'name': 'upwrdz_googleplus_url', 'content': GOOGLE_PLUS_PAGE_URL})
    message['global_merge_vars'].append(
        {'name': 'upwrdz_linkedin_url', 'content': LINKEDIN_PAGE_URL})
    message['global_merge_vars'].append(
        {'name': 'upwrdz_twitter_url', 'content': TWITTER_PAGE_URL})
    MandrillTemplateMail(template_name, [], message).send()


# =======================================================================
# Sending mail from dynamic address
# =======================================================================
def send_mandrill_email_dynamic_from(template_name, email_from, email_to, context, curr_site=None):
    if context is None:
        context = {}
    message = {
        'from_email': email_from,
        'to': [],
        'global_merge_vars': []
    }
    for em in email_to:
        message['to'].append({'email': em})
    for k, v in context.items():
        message['global_merge_vars'].append({'name': k, 'content': v})
    message['global_merge_vars'].append(
        {'name': 'upwrdz_redirect_url', 'content': settings.DEFAULT_DOMAIN_URL})
    # appending social media urls
    message['global_merge_vars'].append(
        {'name': 'upwrdz_facebook_url', 'content': FACEBOOK_PAGE_URL})
    message['global_merge_vars'].append(
        {'name': 'upwrdz_googleplus_url', 'content': GOOGLE_PLUS_PAGE_URL})
    message['global_merge_vars'].append(
        {'name': 'upwrdz_linkedin_url', 'content': LINKEDIN_PAGE_URL})
    message['global_merge_vars'].append(
        {'name': 'upwrdz_twitter_url', 'content': TWITTER_PAGE_URL})
    MandrillTemplateMail(template_name, [], message).send()


# =======================================================================
# sending mail with dynamic subject
# =======================================================================
def send_mandrill_email_admin_subject(template_name, email_to, user_email, subject, context, curr_site=None):
    if context is None:
        context = {}
    message = {
        'subject': subject,
        'to': [],
        'headers': {},
        'global_merge_vars': []
    }
    for em in email_to:
        message['to'].append({'email': em})
        message['headers'] = {'Reply-To': user_email}
    for k, v in context.items():
        message['global_merge_vars'].append({'name': k, 'content': v})
    message['global_merge_vars'].append(
        {'name': 'upwrdz_redirect_url', 'content': settings.DEFAULT_DOMAIN_URL})
    # appending social media urls
    message['global_merge_vars'].append(
        {'name': 'upwrdz_facebook_url', 'content': FACEBOOK_PAGE_URL})
    message['global_merge_vars'].append(
        {'name': 'upwrdz_googleplus_url', 'content': GOOGLE_PLUS_PAGE_URL})
    message['global_merge_vars'].append(
        {'name': 'upwrdz_linkedin_url', 'content': LINKEDIN_PAGE_URL})
    message['global_merge_vars'].append(
        {'name': 'upwrdz_twitter_url', 'content': TWITTER_PAGE_URL})
    MandrillTemplateMail(template_name, [], message).send()
