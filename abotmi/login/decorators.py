import logging

from functools import wraps
from time import time

from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from datacenter.models import UserProfile, NoticeBoard, Advisor
from advisor_check.views import check_advisor_claimed, get_advisor_card
from common.views import logme

logger = logging.getLogger(__name__)


def active_and_advisor(view_func):
    def wrapper(request, *args, **kw):
        # "Absolute URL REQ:::::: "+path
        path = request.build_absolute_uri()
        # "Short URL REQ::::: "+full_path
        full_path = request.get_full_path()
        user = request.user.profile.is_advisor
        if not (user):
            return HttpResponse("<h1>You are not advisor <a href='%s'>Click here to return home</a></h1>" % settings.LOGIN_REDIRECT_URL)
        else:
            return view_func(request, *args, **kw)
    return wrapper


def active_and_registered_advisor(view_func):
    def wrapper(request, *args, **kw):
        path = request.build_absolute_uri()
        full_path = request.get_full_path()
        if  request.user.profile.is_advisor and request.user.profile.advisor.is_register_advisor:
            return view_func(request, *args, **kw)
        else:
            blog_url = "/blog/"
            return HttpResponse('<h1>You are not certified advisor \
                <a href="%s">Click here to return blog</a></h1>' % blog_url)
    return wrapper


def active_and_certified_advisor(view_func):
    def wrapper(request, *args, **kw):
        path = request.build_absolute_uri()
        full_path = request.get_full_path()
        if request.user.profile.is_advisor and request.user.profile.advisor.is_certified_advisor \
            or request.user.profile.advisor.is_honorable_advisor:
            return view_func(request, *args, **kw)
        else:
            blog_url = "/blog/icore/"
            return HttpResponse('<h1>You are not certified advisor \
                <a href="%s">Click here to return blog</a></h1>' % blog_url)
    return wrapper


def allow_nfadmin(view_func):
    def wrapper(request, *args, **kw):
        path = request.build_absolute_uri()
        full_path = request.get_full_path()
        user = request.user.profile.is_admin
        if not (user):
            return HttpResponse("<h1>You are not advisor <a href='%s'>\
                Click here to return home</a></h1>" % settings.LOGIN_REDIRECT_URL)
        else:
            return view_func(request, *args, **kw)
    return wrapper


def referral_user(referral_code_check):
    '''
    Checking whether valid referral link
    '''
    def wrapper(request, *args, **kw):
        if 'referral_code' in request.GET.keys():
            code = request.GET['referral_code']
            try:
                UserProfile.objects.get(referral_code=code)
            except ObjectDoesNotExist:
                return HttpResponse('not a valid referral link')
        return referral_code_check(request, *args, **kw)
    return wrapper


def check_role_and_redirect(view_func):
    def wrapper(request, *args, **kwargs):
        path = request.build_absolute_uri()
        full_path = request.get_full_path()
        user_selected_role = request.session.get(
            'user_selected_role', 'advisor')
        user_profile = request.user.profile
        if user_selected_role == 'advisor':
            claimed_status = check_advisor_claimed(request)
            if claimed_status:
                advisor = user_profile.advisor
                if advisor.is_register_advisor:
                    return HttpResponseRedirect('/my_identity/')
                else:
                    return HttpResponseRedirect('/signup/face_capture/')
            else:
                return HttpResponseRedirect('/advisor_check/get_advisor_card/')
        else:
            return HttpResponseRedirect('/member/')
    return wrapper


def allow_crisil_admin(view_func):
    '''
    Checking CRISIL admin or not
    '''
    def wrapper(request, *args, **kw):
        path = request.build_absolute_uri()
        full_path = request.get_full_path()
        user = request.user.profile.is_admin
        crisil_admin = request.user.profile.is_crisil_admin
        if crisil_admin or user:
            return view_func(request, *args, **kw)
        else:
            return HttpResponse("<h1>You are not advisor <a href='%s'>\
                Click here to return home</a></h1>" % settings.LOGIN_REDIRECT_URL)
    return wrapper


def timer(view_func):
    def wrapper(request, *args, **kwargs):
        start = time()
        result = view_func(request, *args, **kwargs)
        elapsed = time() - start
        logger.info(
            logme("%s took %d time to finish" % (view_func.__name__, elapsed), request)
        )
        return result
    return wrapper


def check_member_or_advisor(additional_val=None):
    '''
    Checking member or not
    '''
    def check_member_or_advisor(view_func):
        def wrapper(request, slug=None, *args, **kwargs):
            user_selected_role = request.session.get(
                'user_selected_role', 'advisor')
            if user_selected_role == 'investor' and not slug:
                return HttpResponse('<h2>You have dont access to see this page</h2>')
            if not request.user.profile.advisor.is_register_advisor and not slug:
                return HttpResponseRedirect('/signup/face_capture/')
            else:
                return view_func(request, slug, *args, **kwargs)
        return wraps(view_func)(wrapper)
    return check_member_or_advisor


def allow_advisor(view_func):
    '''
    Allows only advisor
    '''
    def wrapper(request, *args, **kwargs):
        user_selected_role = request.session.get(
            'user_selected_role', 'advisor')
        if user_selected_role == 'advisor' and request.user.profile.is_advisor:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse(
                "You Login as %s in ABOTMI. You don't has access to %s functionality. \
                Please click <a href='%s'>here</a> to go back." % (
                    user_selected_role,
                    'Advisor',
                    settings.DEFAULT_DOMAIN_URL
                )
            )
    return wrapper


def allow_investor(view_func):
    '''
    Allows only investor
    '''
    def wrapper(request, *args, **kwargs):
        user_selected_role = request.session.get(
            'user_selected_role', 'Advisor')
        if user_selected_role == 'investor' and request.user.profile.is_member:
            return view_func(request, slug, *args, **kwargs)
        else:
            return HttpResponse(
                "You Login as %s in ABOTMI. You don't has access to %s functionality. \
                Please click <a href='%s'>here</a> to go back." % (
                    user_selected_role,
                    'Investor',
                    settings.DEFAULT_DOMAIN_URL
                )
            )
        return wrapper


def allow_blockchain_admin(view_func):
    """
        this function to restrict other user to open blockchain dashboard
        only admin can see that.
    """
    def wrapper(request, *args, **kw):
        path = request.build_absolute_uri()
        full_path = request.get_full_path()
        user = request.user.is_superuser

        if user:
            return view_func(request, *args, **kw)
        else:
            return HttpResponse("<h1>You are not Admin <a href='%s'>\
                Click here to return home</a></h1>" % settings.LOGIN_REDIRECT_URL)
    return wrapper


def allow_claimed_advsior(view_func):
    def wrapper(request, *args, **kwargs):
        user_selected_role = request.session.get(
            'user_selected_role', 'advisor')
        if user_selected_role == 'advisor':
            claimed_status = check_advisor_claimed(request)
            if claimed_status:
                return view_func(request, *args, **kwargs)
            return HttpResponseRedirect('/advisor_check/get_advisor_card/')
        else:
            return HttpResponse(
                "You Login as %s in ABOTMI. You don't has access to %s functionality. \
                Please click <a href='%s'>here</a> to go back." % (
                    user_selected_role,
                    'advisor',
                    settings.DEFAULT_DOMAIN_URL
                )
            )
    return wrapper
