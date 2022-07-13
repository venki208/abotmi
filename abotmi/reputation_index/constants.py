from django.conf import settings
# Reputation Index Constants
SEBI = "sebi_registration"
AMFI = "amfi_registration"
IRDA = "irda_registration"
RERA = "rera_registration"
DSA = "dsa_registration"
OTHER_REG="other_registration"

#Financial instruments
EQUITY = 'Equity'
MUTUAL_FUND = 'Mutual Fund'
INSURANCE = 'Insurance'
WEALTH_ADVISORY = 'Wealth Advisory'
PORTFOLIO_MANAGEMENT = 'PortFolio Management'

#Peer rating
PEER_RATE_FIFTY = 'peer_rate_fifty'
PEER_RATE_TEN = 'peer_rate_ten'
PEER_RATE_ONE = 'peer_rate_one'

#EIPV
EIPV_VERIFIED ='eipv_verified'
BUSINESS_CODE_CONDUCT="business_code_conduct"

# AGE
AGE_BETW_20AND30 = 'age_betw_20and30'
AGE_BETW_30AND40 = 'age_betw_30and40'
AGE_BETW_40AND50 = 'age_betw_40and50'
AGE_ABOVE50 = 'age_above50'

# OFFICE ADDRESS
ADVISOR_OFFICE_ADDRESS = 'advisor_office_address'

# communication urls
ADVISOR_FACEBOOK_ID = 'advisor_facebook_id'
ADVISOR_GOOGLE_ID = 'advisor_google_id'
ADVISOR_LINKEDIN_ID = 'advisor_linkedin_id'
ADVISOR_TWITTER_ID = 'advisor_twitter_id'

# WEBINAR
ADVISOR_MEETUP_HOSTED_BELOW_5 = 'advisor_meetup_hosted_below_5'
ADVISOR_MEETUP_HOSTED_BETW_5AND10 = 'advisor_meetup_hosted_betw_5and10'
ADVISOR_MEETUP_HOSTED_BETW_10AND25 = 'advisor_meetup_hosted_betw_10and25'

# MERTUP
ADVISOR_WEBINAR_HOSTED_BETW_1AND5 = 'advisor_webianr_hosted_betw_1and5'
ADVISOR_WEBINAR_HOSTED_BETW_5AND15 = 'advisor_webianr_hosted_betw_5and15'
ADVISOR_WEBINAR_HOSTED_ABOVE_15 = 'advisor_webianr_hosted_above_15'

# total clients served
TOTAL_CLIENTS_SERVED_BELOW_50 = 'total_clients_served_below_50'
TOTAL_CLIENTS_SERVED_BETW_50AND100 = 'total_clients_served_betw_50and100'
TOTAL_CLIENTS_SERVED_BELOW_100AND500 = 'total_clients_served_betw_100and500'
TOTAL_CLIENTS_SERVED_ABOVE_500 = 'total_clients_served_above_500'

# total advisor connected
TOTAL_ADVISORS_CONNECTED_BELOW_10 = 'total_advisors_connected_below_10'
TOTAL_ADVISORS_CONNECTED_BETW_10AND50 = 'total_advisors_connected_betw_10and50'
TOTAL_ADVISORS_CONNECTED_ABOVE_50 = 'total_advisors_connected_above50'

# LOOPING
ADVISORS_REFERRED = 'advisor_referred'
REFERRED_REGISTERED_ADVISOR = 'referred_registered_advisor'

# RATING AND RANKING
ADVISOR_REQUEST_FOR_RATING = 'advisor_request_for_rating'
ADVISOR_RATED = 'advisor_got_rated'
ADVISOR_REQUEST_FOR_RANKING = 'advisor_request_for_ranking'
ADVISOR_RANKED = 'advisor_got_ranked'

# LANGUAGES KNOWN
LANGUAGES_COUNT_ONE = 'languages_known_count_1'
LANGUAGES_COUNT_TWO = 'languages_known_count_2'
LANGUAGES_COUNT_THREE = 'languages_known_count_3'
LANGUAGES_COUNT_FOUR = 'languages_known_count_4'
LANGUAGES_COUNT_ABOVE_5 = 'languages_known_count_5'

# LANGUAGES KNOWN TO READ AND WRITE
LANGUAGES_READ_WRITE_COUNT_1 = 'languages_read_write_count_1'
LANGUAGES_READ_WRITE_COUNT_2 = 'languages_read_write_count_2'
LANGUAGES_READ_WRITE_COUNT_3 = 'languages_read_write_count_3'
LANGUAGES_READ_WRITE_COUNT_4 = 'languages_read_write_count_4'
LANGUAGES_READ_WRITE_ABOVE_5 = 'languages_read_write_count_above_5'

# TEXTIANT API END POINTS
RANK_API_KEY = getattr(settings, "RANK_API_KEY", "y82QiA9dfH2DsnLr7q8sX5xzQikeMDdT97I4auv2")
RANK_API_URL = getattr(settings, "RANK_API_URL", "https://rankapi.int.textient.com/v1")
RANK_SCORING_FB = "/fb"
RANK_SCORING_LINKEDIN = "/linkedin"
RANK_ADVISOR_SCORING = "/reppute"
RANK_NATIVE_LOCATION_ADVISOR_SCORING = "/loc/native"
RANK_TRANSIT_LOCATION_ADVISOR_SCORING = "/loc/transient"
RANK_ADVISORS_RANKING_API = "/rank"
RANK_API_KEY_HEADER = { 'x-api-key': RANK_API_KEY }

HYPERLOCAL_NATIVE = "native"
HYPERLOCAL_TRANSIT = "transient"

#Google API Constatnts for finding pincode
API_GOOGLE_GEONAMES = "http://api.geonames.org/findNearbyPostalCodes"
KEY_GOOGLE_GEONAMES = "kantanand"

#user type constants
USER_TYPE_ADVISOR = 'advisor'
USER_TYPE_MEMBER = 'member'
