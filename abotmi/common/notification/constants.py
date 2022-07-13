'''
Referral Constants
'''
REFERRAL_NOTIFICATION = 'referral_notifaction'
# %(signup advisor name/email) --> expected value
LEVEL_1_SIGNUP_NOTIFCATION = 'Your referred %s is signed up into UPWRDZ'
# %(signup advisor name/email, referred advisor name/email) --> expected value
LEVEL_2_SIGNUP_NOTIFCATION = '%s is Signed up into UPWRDZ. referred by %s'
# %(registered advisor name/email)
LEVEL_1_REGISTER_NOTIFCATION = 'Your referred %s has become a registered advisor'
# %(registered advisor name/email, referred advisor name/email) --> expected value
LEVEL_2_REGISTER_NOTIFCATION = '%s has become a registered advisor. referred by %s'

'''
Add Client Constatns
'''
CLIENT_NOTIFICATION = 'client_notification'
# %(signup advisor name/email) --> expected value
LEVEL_1_CLIENT_SIGNUP_NOTIFCATION = 'Your Client %s is signed up into UPLYF'
# %(signup advisor name/email, referred advisor name/email) --> expected value
LEVEL_2_CLIENT_SIGNUP_NOTIFCATION = '%s is Signed up into UPLYF. Added by %s'
# %(registered advisor name/email)
LEVEL_1_CLIENT_REGISTER_NOTIFCATION = 'Your Client %s has got Registered with UPLYF'
# %(registered advisor name/email, referred advisor name/email) --> expected value
LEVEL_2_CLIENT_REGISTER_NOTIFCATION = '%s has become a registered client. referred by %s'


'''
Follow Constatns
'''
ADVISOR_FOLLOWING = "you started following %s"
ADVISOR_REJECTED = "%s rejected your request"

'''
Viewed Profile Constatns
'''
VIEWED_PROFILE_NOTIFICATION = 'viewed_profile_notification'


# Signup
SIGNUP_TEMPLATE = 'signup'

# Verification constants
EMAIL_VERF_TEMPLATE = 'email_verification'
MOBILE_VERF_TEMPLATE = 'mobile_verification'

# Registration
REGISTRATION_TEMPLATE = 'registration'
REG_REQ = 'reg_req'

# Advisor check
ADVISOR_CHK_CLAIM = 'ad_chk_claim'
ADV_CHK_CONNECT = 'adv_chk_connect'

# Static Constants
LEARN_ABOUT_MY_IDENTITY = 'learn_about_my_identity'
LEARN_ABOUT_MY_HUB = 'learn_about_my_hub'
LEARN_ABOUT_COURSE = 'learn_about_course'

# Refer Constants
REFER_SIGNUP = 'refer_signup'
REFER_REGISTRATION = 'refer_registration'

# Viewed Profile constants
VIEWED_PROFILE = 'viewed_profile'

# Rating Constatns
RATE_REQ = 'rate_request'
RATE_RES = 'rate_response'

# Ranking Constatns
RANK_REQ = 'rank_request'
RANK_RES = 'rank_response'

VIDEO_UPLOAD_SUCCESS = 'video_upload_success'
ADVICE_REQ = 'advice_request'
FOLLOQ_REQ = 'follow_request'


# Attaching function name to notification types
GET_FUNC_NAME = {
    SIGNUP_TEMPLATE: 'get_receiver_data',
    EMAIL_VERF_TEMPLATE: 'get_receiver_data',
    MOBILE_VERF_TEMPLATE: 'get_receiver_data',
    REGISTRATION_TEMPLATE: 'get_receiver_data',
    REG_REQ: 'get_receiver_data',
    LEARN_ABOUT_MY_IDENTITY: 'get_receiver_data',
    LEARN_ABOUT_MY_HUB: 'get_receiver_data',
    LEARN_ABOUT_COURSE: 'get_receiver_data',
    REFER_SIGNUP: 'get_sender_data',
    REFER_REGISTRATION: 'get_sender_data',
    VIEWED_PROFILE: 'get_sender_data',
    ADV_CHK_CONNECT: 'get_sender_data',
    RATE_REQ: 'get_sender_data',
    RATE_RES: 'get_sender_data',
    RANK_REQ: 'get_sender_data',
    RANK_RES: 'get_sender_data',
    VIDEO_UPLOAD_SUCCESS: 'get_receiver_data',
    ADVICE_REQ: 'get_advice_data',
    FOLLOQ_REQ: 'get_sender_data',
}
