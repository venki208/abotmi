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
# %(Viewer name/email) --> expected value
VIEWED_PROFILE = '%s has viewed your profile'
