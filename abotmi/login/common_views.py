import os
import json
import requests
import time
import datetime

from django.conf import settings

from django.contrib.auth.models import User
from datacenter.models import UserProfile

from common.views import logme, referral_points, get_notification_services_json
from common.constants import SIGNUP_WITH_EMAIL, PRIMARY, SIGNUP_POINTS, GOOGLE_MEDIA,\
    FACEBOOK_MEDIA, LINKEDIN_MEDIA, MEMBER_SIGNUP_WITH_EMAIL, MEMBER_FACEBOOK_MEDIA,\
    MEMBER_GOOGLE_MEDIA, MEMBER_LINKEDIN_MEDIA
from common.notification.constants import REFER_SIGNUP

from common.notification.views import NotificationFunctions

from signup.djmail import send_mandrill_email

import logging
logger = logging.getLogger(__name__)


class LoginCommonFunctions:
    '''
    Description: Creating Common funcitons for Re-use
    '''
    def __init__(self, params):
        self.request = params['request'] if params.has_key('request') else None
        self.ref_link = ''
        self.email = None
        self.first_name = None
        self.last_name = None
        self.birthday = None
        self.gender = None
        self.mobile = None
        self.user_selected_role = 'advisor'
        if self.request:
            self.ref_link = self.request.POST.get('ref_link', None)
            self.email = self.request.POST.get('email', None)
            self.first_name = self.request.POST.get('first_name', None)
            self.last_name = self.request.POST.get('last_name', None)
            self.birthday = self.request.POST.get('birthday', None)
            self.gender = self.request.POST.get('gender', None)
            self.mobile = self.request.POST.get('mobile', None)
            self.user_selected_role = self.request.POST.get(
                'user_selected_role', 'advisor')
            self.source_media = self.request.POST.get('sm_source', None)
            logger.info(
                logme('Common class object is created', params['request'])
            )

    def createuser(self, object=None):
        if object:
            user_password = object['password']
            up_email = object.get('email', None)
            up_first_name = object.get('first_name', None)
            up_last_name = object.get('last_name', None)
            up_mobile = object.get('mobile', None)
            ref_link = self.ref_link
            self.first_name = up_first_name if not self.first_name else self.first_name
            self.last_name = up_last_name if not self.last_name else self.last_name
            self.email = up_email if not self.email else self.email
            self.email = self.email.strip()
            self.mobile = up_mobile if not self.mobile else self.mobile
            if self.first_name and self.email:
                user, created = User.objects.get_or_create(
                    username=self.email, email=self.email)
                user_profile = user.profile
                # create/get record in user status table
                user_status = user_profile.status
                user.first_name = self.first_name
                user.last_name = self.last_name
                user.email = self.email
                user_profile.first_name = self.first_name
                user_profile.last_name = self.last_name
                if created:
                    user.set_password(user_password)
                    user.is_active = True
                    user.is_staff = True
                    logger.info(
                        "user signed up with emailid"
                    )
                    user_profile.communication_email_id = PRIMARY
                    if self.user_selected_role == 'investor':
                        user_profile.is_member = True
                        user_profile.source_media = MEMBER_SIGNUP_WITH_EMAIL
                    elif self.source_media == 'FASIA':
                        user_profile.source_media = 'FASIA'
                        user_profile.is_advisor = True
                    else:
                        user_profile.source_media = SIGNUP_WITH_EMAIL
                        user_profile.is_advisor = True

                        # Getting points by reffering the user
                        if ref_link:
                            referrer_obj = UserProfile.objects.filter(
                                referral_code=ref_link).first()
                            if referrer_obj:
                                user_profile.referred_by = referrer_obj.user
                                referral_points(referrer_obj, user_profile, SIGNUP_POINTS)
                                logger.info(
                                    "awarded referral points to the referred user"
                                )
                                notif_obj = NotificationFunctions(self.request)
                                notif_obj.save_notification(
                                    notification_type=REFER_SIGNUP,
                                    sender=user_profile,
                                    receive=referrer_obj
                                )
                                del(notif_obj)
                # cheking existing mobile number is verfied or not
                # if user_status.mobile_verified:
                #     user_status.mobile_verified = user_profile.mobile.__eq__(self.mobile)
                if self.mobile:
                    user_profile.mobile = self.mobile
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                user.save()
                user_profile.save()
                user_status.save()
                if created:
                    data = {
                        'status': 201,
                        'user': user,
                        'user_profile': user_profile,
                        'user_status': user_status
                    }
                else:
                    data = {
                        'status': 200,
                        'user': user,
                        'user_profile': user_profile,
                        'user_status': user_status
                    }
            else:
                data = {'status': 'form_not_valid'}
        else:
            data = {'status': 404}
        return data

    def get_or_create_social_media_advisor(self, object=None):
        if object:
            password = object['password']
            source_media = object['source_media']
            ref_link = self.ref_link
            if source_media == FACEBOOK_MEDIA:
                source_media = FACEBOOK_MEDIA if not self.user_selected_role == 'investor' else MEMBER_FACEBOOK_MEDIA
                field_name = 'facebook_media'
            elif source_media == GOOGLE_MEDIA:
                source_media = GOOGLE_MEDIA if not self.user_selected_role == 'investor' else MEMBER_GOOGLE_MEDIA
                field_name = 'google_media'
            elif source_media == LINKEDIN_MEDIA:
                source_media = LINKEDIN_MEDIA if not self.user_selected_role == 'investor' else MEMBER_LINKEDIN_MEDIA
                field_name = 'linkedin_media'
            else:
                source_media = None
                field_name = ''
            if self.email and self.first_name:
                user, created = User.objects.get_or_create(username=self.email, email=self.email)
                user_profile = user.profile
                user_status = user_profile.status  # create/get record in user status table
                if not user_profile.is_advisor and not user_profile.is_member:
                    user_profile.source_media = source_media
                    if field_name:
                        setattr(user_profile, field_name, self.email)
                if created:
                    user.first_name = self.first_name
                    user.last_name = self.last_name
                    user.set_password(password)
                    user.is_active = True
                    user.is_staff = True
                    user.save()
                    user_profile.first_name = self.first_name
                    user_profile.last_name = self.last_name
                    user_profile.email = self.email
                    user_profile.communication_email_id = PRIMARY
                    if self.user_selected_role == 'investor':
                        user_profile.is_member = True
                    else:
                        user_profile.is_advisor = True
                    if self.gender:
                        user_profile.gender = self.gender[0].upper()
                    if ref_link:
                        referrer_obj = UserProfile.objects.get(referral_code=ref_link)
                        user_profile.referred_by = referrer_obj.user
                        referral_points(referrer_obj, user_profile, SIGNUP_POINTS)
                        logger.info(
                            logme('awarded referal points to the referred advisor', self.request)
                        )
                        notif_obj = NotificationFunctions(self.request)
                        notif_obj.save_notification(
                            notification_type=REFER_SIGNUP,
                            sender=user_profile,
                            receive=referrer_obj
                        )
                        del(notif_obj)
                    try:
                        send_mandrill_email('ABOTMI_01', [email], context={'Name': first_name})
                    except:
                        logger.info(
                            logme('failed to send email to %s up user'%(str(source_media)), self.request)
                        )
                else:
                    if not user_profile.is_advisor and not user_profile.is_member:
                        user_profile.is_advisor = True
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                user.save()
                user_profile.save()
                data = {
                    'status': 200,
                    'is_created': created,
                    'user': user,
                    'user_profile': user_profile
                }
            else:
                data = {'status':204}
        else:
            data = {'status':204}
        return data
