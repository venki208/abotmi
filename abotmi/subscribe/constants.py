from django.conf import settings

# To stop/start package
ACTIVATED = "ACTIVATED"
DEACTIVATED = "DEACTIVATED"

#package type constans as per db choices
PKG_STANDARD = 'STANDARD'
PKG_DELUXE = 'DELUXE'
PKG_PREMIUM = 'PREMIUM'
PKG_EXECUTIVE = 'EXECUTIVE'
PKG_PLATINUM = 'PLATINUM'

#SubscriptionCategory as stored in databse SubscriptionCategoryMaster table
SUB_CAT_MICRO_LEARNING_PACK = "MICRO_LEARNING_PACK"
SUB_CAT_IDENTITY_PACK = "IDENTITY_PACK"

#Order of packge type list
PKG_ORDER_LIST = [PKG_STANDARD,PKG_DELUXE,PKG_PREMIUM,PKG_EXECUTIVE,PKG_PLATINUM]


#Payment status
PAYMENT_PENDING = "Transaction pending"
PAYMENT_COMPLETED = "Transaction Successful"

#Micro learning feature name
ML_NO_OF_VIDEOS = "no_of_videos"

#Service Type
SERVICE_TYPE = "subscription"


PKG_ORDER_LIST = [PKG_STANDARD,PKG_DELUXE,PKG_PREMIUM,PKG_EXECUTIVE,PKG_PLATINUM]

FEATURE_ORDET_LIST = [
    {'list_of_viewers' : 'List of Viewers'},
    {'number_of_viewer_details' : 'No. of Viewer Details'},
    {'name' : 'Name'},
    {'email' : 'Email'},
    {'contact_number' : 'Contact Number'},
    {'when_they_visit' : 'When They Visit'},
    {'social_media_link' : 'Social Media Link'},
    {'location' : 'Location'},
    {'viewer_registrations_status' : 'Visitor Reg Status'},
    {'pupose_of_visit' : 'Purpose of Visit'},
    {'real_time_notification' : 'Real Time Notification'},
    {'social_graph' : 'Social Graph'},
    {'behavioural_graph' : 'Behavioural Graph'}
]

FEATURE_ORDET_LIST_FOR_MICRO_LEARNING = [
    {'amount_to_pay' : 'Amount to pay'},
    {'no_of_videos' : 'No. of videos'},
    {'duration_of_video' : 'Duration of the video'},
    {'content_duration' : 'Content duration'}
]

ACTIVATED_KEYORDER = ["Package", "Name","Email", "Mobile", "Last Visited", "Social Media Link", "Location", "Viewer Registrations Status", "Purpose Of Visit", "Real Time Notification", "Social Graph", "Behavioural Graph"]

UPGRADE_TO_REVEAL = 'UPGRADE TO REVEAL'
DATA_NOT_AVAILABLE = 'NOT AVAILABLE'