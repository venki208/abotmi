import json
import logging
import sys

from django.conf import settings

from datacenter.models import (
    Notification, NotificationTemplate, UserProfile, TemplateData
)
from .constants import LEVEL_1_SIGNUP_NOTIFCATION,\
    LEVEL_2_SIGNUP_NOTIFCATION, REFERRAL_NOTIFICATION, LEVEL_1_REGISTER_NOTIFCATION,\
    LEVEL_2_REGISTER_NOTIFCATION, CLIENT_NOTIFICATION, LEVEL_1_CLIENT_SIGNUP_NOTIFCATION,\
    LEVEL_2_CLIENT_SIGNUP_NOTIFCATION, LEVEL_1_CLIENT_REGISTER_NOTIFCATION,\
    LEVEL_2_CLIENT_REGISTER_NOTIFCATION
from .constants import GET_FUNC_NAME

from common.views import logme

logger = logging.getLogger(__name__)

notification_level1 = [
    'viewed_profile', 'refer_signup', 'refer_registration', 'adv_chk_connect',
    'rate_response', 'rank_response', 'rate_request', 'rank_request', 'advice_request',
    'follow_request',
]


class NotificationStatus():
    '''
    Getting the status of notification True/False

    params:
    ------
    request --> request object
    receive --> receive object(should be UserProfile table object)
    '''

    def __init__(self, request=None, receive=None, *args, **kwargs):
        self.request = request
        self.receive = receive

    def check_template_exists(self, notification_type):
        '''
        Checks template is exist or not

        params:
        ------
        notification_type --> type of Notification Template <String>

        Result: return Notification Template table object
        ------
        '''
        request = self.request
        notif_temp = NotificationTemplate.objects.filter(
            template_type=notification_type).first()
        if not notif_temp:
            logger.error(
                logme(
                    'Missing Notification template type to save the notification',
                    request
                )
            )
        return notif_temp

    def get_catogery_status(self, user_status=None, catogery=None):
        '''
        Checks User gave access to save the notification in database

        params:
        -------
        user_status --> UserStatus Table object <obj>
        catogery --> Notification catogery type <string>

        Result: True/False
        ------
        '''
        request = self.request
        user_status = self.receive.status if not user_status else user_status
        if user_status and catogery:
            if user_status.notification_service:
                notif_json = json.loads(user_status.notification_service)
                return notif_json.get(catogery, True)
            else:
                logger.info(
                    logme('User switch off to save {} notifications'.format(
                        catogery
                    ), request)
                )
                return True
        else:
            return False

    def is_nf_save(self, notification_type, user_status):
        '''
        Checks Notification Template is exist or not and checks user is allowed to save
        the notification

        params:
        -------
        notification_type --> type of Notification Template <String>
        user_status --> UserStatus Table object <obj>

        Result: True/False
        ------
        '''
        catg_status = False
        templ_obj = self.check_template_exists(notification_type)
        if templ_obj:
            catg_status = self.get_catogery_status(
                user_status, templ_obj.catogery)
        return (True, str(templ_obj.id)) if (templ_obj and catg_status) else (False, '')


class SaveAdviceNotification():
    '''
    Saving Advice Notifications

    params:
    -------
    request --> request object
    receive --> receive object(should be UserProfile table object)
    '''

    def __init__(self, request=None, receive=None):
        self.request = request
        self.receive = receive

    def save_get_advice(
            self, advice_id, data=[], notification_type=None, receive=None,
            sender=None, receive_from='user_profile', sender_from='user_profile'):
        '''
        Saving Advice notification in db

        params:
        ------
        * --> mandatory
        advice_id * --> id of the asked advice (Should pass GetAdvice object id)
        notification_type * --> Type of notification <string>
        receive --> received user object (UserProfile Object(
            no need to pass if object pass while creating cls obj))
        sender --> from object
        receive_from --> Default will take `user_profile` (
            i.e; receive person obj from UserProfile Table)
        sender_from --> Default will take `user_profile` (
            i.e; receive person obj from UserProfile Table)
        '''
        request = self.request
        receive = receive if receive else self.receive
        if notification_type and receive and sender and advice_id:
            is_allow_to_save, templ_id = self.is_nf_save(
                notification_type, receive.status)
            if is_allow_to_save:
                temp_data = TemplateData(
                    data_type='get_advice_id', value=str(advice_id))
                try:
                    params = {}
                    params['receive_id'] = str(receive.id)
                    params['template_id'] = templ_id
                    params['receive_id_from'] = receive_from
                    params['sender_id'] = str(sender.id)
                    params['sender_id_from'] = sender_from
                    nf = Notification.objects.create(**params)
                    nf.template_data.append(temp_data)
                    nf.save()
                    return True
                except Exception as e:
                    print e
                    line_no = str(sys.exc_info()[-1].tb_lineno)
                    logger.error(
                        logme(
                            'Unable to save get advice notification. \
                                error->%s, line_no->%s' % (str(e), line_no),
                            request
                        )
                    )
                    return False
            return False
        else:
            logger.error(
                logme(
                    'Unable to save get advice notification. missing parameter', request)
            )
            return False


class NotificationFunctions(NotificationStatus, SaveAdviceNotification):
    '''
        Description: Saving, Deleteing, Updating, Getting Notifications
        parameters to pass for creating object
        request --> request
        user_profile --> UserProfile table object
    '''

    def __init__(self, request=None, receive=None):
        NotificationStatus.__init__(self, request=None, receive=None)
        SaveAdviceNotification.__init__(self, request=None, receive=None)
        self.request = request
        self.receive = receive

    def save_notification(
            self, data=[], notification_type=None, receive=None,
            sender=None, receive_from='user_profile', sender_from='user_profile'):
        '''
        Saving the Advisor Notifications
        '''
        request = self.request
        if notification_type:
            try:
                receive = receive if receive else self.receive
                is_allow_to_save, templ_id = self.is_nf_save(
                    notification_type, receive.status)
                if is_allow_to_save:
                    clm_args = {}
                    clm_args['receive_id'] = str(receive.id)
                    clm_args['template_id'] = templ_id
                    clm_args['receive_id_from'] = receive_from
                    if sender:
                        clm_args['sender_id'] = str(sender.id)
                        clm_args['sender_id_from'] = sender_from
                    notification, status = Notification.objects.get_or_create(
                        **clm_args)
                    if data:
                        notification.values = data
                    notification.save()
                    logger.info(
                        logme(
                            'Created notification for %s' % (notification_type),
                            request
                        )
                    )
                    return True
                else:
                    return False
            except Exception as e:
                print e
                logger.error(
                    logme(
                        'Unable to create notification for %s, error-> %s, \
                            line_no: %s' % (
                            notification_type, str(e), str(sys.exc_info()[-1].tb_lineno)),
                        request
                    )
                )
        else:
            logger.error(
                logme('Missing notification_type param to save', request)
            )
            return False

    @staticmethod
    def get_message_values(nf_obj, notification_type, user_profile=None):
        mes_attr = []
        fun_params = {
            'nf_obj': nf_obj,
            'notification_type': notification_type,
            'user_profile': user_profile
        }
        cls_fun = getattr(NFTemplateData, GET_FUNC_NAME[notification_type])
        user_data = cls_fun(**fun_params)
        return user_data

    @staticmethod
    def update_read_status(ids=None):
        '''
        Updating read status to True
        '''
        if ids:
            ids = ids if type(ids) == list else list(ids)
            nf = Notification.objects.filter(id__in=ids)
            if nf:
                nf.update(read_status=True)
        return True


class ActionUrl():
    '''
    Gets the action URL
    '''

    @staticmethod
    def get_advice_url(advice_id):
        '''
        Generating Get Advice action URL
        '''
        return '/member/read_more_answer/?question_id={}'.format(advice_id)


class NFTemplateData():
    '''
    
    '''

    @staticmethod
    def get_receiver_data(*args, **kwargs):
        up_list = []
        profile_url = []
        user_data = {}
        nf_obj = kwargs['nf_obj']
        user_profile = kwargs.get('user_profile', None)
        up_list.append(user_profile.full_name)
        user_data['msg_data'] = up_list
        user_data['profile_url'] = None
        user_data['profile_pic'] = None
        user_data['action'] = False
        return user_data

    @staticmethod
    def get_sender_data(*args, **kwargs):
        nf_obj = kwargs['nf_obj']
        sender_id = nf_obj.sender_id
        user_profile = kwargs.get('user_profile', None)
        profile_url, action_url, profile_pic = '', '', ''
        user_data = {}
        up_list = []
        u_p = UserProfile.objects.filter(
            id=sender_id)
        u_p_obj = u_p.first()
        if u_p:
            up_list.insert(0, u_p_obj.full_name)
            if u_p_obj.is_member and not u_p_obj.is_advisor:
                profile_url = '/investor_profile/'
            else:
                profile_url = '/profile/'
            profile_url = settings.DEFAULT_DOMAIN_URL + profile_url + \
                u_p_obj.batch_code
            profile_pic = u_p_obj.picture.url if u_p_obj.picture else ''
        user_data['msg_data'] = up_list
        user_data['profile_url'] = profile_url
        user_data['profile_pic'] = profile_pic if sender_id else None
        user_data['action'] = False
        return user_data

    @staticmethod
    def get_advice_data(*args, **kwargs):
        user_data = NFTemplateData.get_sender_data(*args, **kwargs)
        nf_obj = kwargs['nf_obj']
        if nf_obj.template_data:
            advice_id = nf_obj.template_data[0].value
            user_data['action_url'] = ActionUrl.get_advice_url(advice_id)
            user_data['action'] = True
        return user_data
