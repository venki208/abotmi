# python lib
import cStringIO as StringIO
import datetime
import json
import logging
import requests
from datetime import date

# Constants
from common.constants import (MEMBER_ROLE, ADVISOR_ROLE, CRISIL_GOT_CERTIFICATE, 
    SSL_VERIFY, POST_DOCTORATE, DOCTORATE, POST_GRADUATION,GRADUATION,
    PROFESSIONAL_QUALIFICATION, OTHER_QUALIFICATION, PREMIUM_INSTUTIONS_LIST, 
    HIGHEST_EDU_DICT,EDU_CAT_SPL_IN_MBA_OR_DIP_LIST, ADD_QUALIFICATION_IN_MBA_OR_DIP_LIST,
    PROF_IN_ADD_SUB)
from reputation_index import constants as reputation_constants

# Database Models
from datacenter.models import ReferralPointsType, ReferralPoints, Advisor,\
    TransactionsDetails, UploadDocuments, UserProfile, RewardPoints, ReputationIndex,\
    AdvisorRating, MeetUpEvent, TrackWebinar, ReputationIndexMetaData, AdvisorReputationIndex

# Local imports
from reputation_index.serializers import ReputationIndexMetaDataSerializer

logger = logging.getLogger(__name__)


def social_signup(user_profile):
    '''
    Description: Checking the sign up categary of user
    '''
    signup_by = None
    if user_profile.source_media:
        signup_by = user_profile.source_media
    reward_point= RewardPoints.objects.filter(name=signup_by).first()
    ReputationIndex.objects.get_or_create(
        reward_type=reward_point,
        user_profile=user_profile
    )
    return True


def advisor_certification(user_profile):
    '''
    Description: Advisor's certification_title
    '''
    advisor = Advisor.objects.get(user_profile = user_profile)
    reward_point_sebi = RewardPoints.objects.filter(
        name=reputation_constants.SEBI).first()
    reward_point_amfi = RewardPoints.objects.filter(
        name=reputation_constants.AMFI).first()
    reward_point_irda = RewardPoints.objects.filter(
        name=reputation_constants.IRDA).first()
    reward_point_rera = RewardPoints.objects.filter(
        name=reputation_constants.RERA).first()
    reward_point_dsa = RewardPoints.objects.filter(
        name=reputation_constants.DSA).first()
    reward_point_other = RewardPoints.objects.filter(
        name=reputation_constants.OTHER_REG).first()
    if advisor.is_certified_advisor:
        if advisor.sebi_number:
            sebi_piont = reward_point_sebi.points
            ReputationIndex.objects.get_or_create(
                reward_type=reward_point_sebi,
                user_profile=user_profile
            )
        if advisor.amfi_number:
            amfi_point = reward_point_amfi.points
            ReputationIndex.objects.get_or_create(
                reward_type=reward_point_amfi,
                user_profile=user_profile
            )
        if advisor.irda_number:
            amfi_point = reward_point_irda.points
            ReputationIndex.objects.get_or_create(
                reward_type=reward_point_irda,
                user_profile=user_profile
            )
        if advisor.is_rera:
            ReputationIndex.objects.get_or_create(
                reward_type=reward_point_rera,
                user_profile=user_profile
            )
        if advisor.dsa_details:
            ReputationIndex.objects.get_or_create(
                reward_type=reward_point_dsa,
                user_profile=user_profile
            )
        if advisor.other_registered_number:
            if advisor.other_registered_organisation:
                ReputationIndex.objects.get_or_create(
                    reward_type=reward_point_other,
                    user_profile=user_profile
                )
    return True


def advisor_certification(user_profile):
    '''
    Description: Advisor's financial instruments sold and it's experience
    '''
    advisor = Advisor.objects.get(user_profile = user_profile)
    reward_point_equity = RewardPoints.objects.filter(
        name=reputation_constants.EQUITY).first()
    reward_point_mutual_fund = RewardPoints.objects.filter(
        name=reputation_constants.MUTUAL_FUND).first()
    reward_point_insurance = RewardPoints.objects.filter(
        name=reputation_constants.INSURANCE).first()
    reward_point_wealth_advisory = RewardPoints.objects.filter(
        name=reputation_constants.WEALTH_ADVISORY).first()
    reward_point_portfolio= RewardPoints.objects.filter(
        name=reputation_constants.PORTFOLIO_MANAGEMENT).first()
    if advisor.financial_instruments:
        objects = json.loads(advisor.financial_instruments)
        for fin_objects in objects:
            if fin_objects['instruments'] == reputation_constants.EQUITY:
                Equity_experience = fin_objects['experience']
                ReputationIndex.objects.get_or_create(
                    reward_type=reward_point_equity,
                    user_profile=user_profile
                )
            if fin_objects['instruments'] == reputation_constants.MUTUAL_FUND:
                Mutual_Fund_experience = fin_objects['experience']
                ReputationIndex.objects.get_or_create(
                    reward_type=reward_point_mutual_fund,
                    user_profile=user_profile
                )
            if fin_objects['instruments'] == reputation_constants.INSURANCE:
                Insurance_experience = fin_objects['experience']
                ReputationIndex.objects.get_or_create(
                    reward_type=reward_point_insurance,
                    user_profile=user_profile
                )
            if fin_objects['instruments'] == reputation_constants.WEALTH_ADVISORY:
                Wealth_Advisory_experience = fin_objects['experience']
                ReputationIndex.objects.get_or_create(
                    reward_type=reward_point_wealth_advisory,
                    user_profile=user_profile
                )
            if fin_objects['instruments'] == reputation_constants.PORTFOLIO_MANAGEMENT:
                Wealth_Advisory_experience = fin_objects['experience']
                ReputationIndex.objects.get_or_create(
                    reward_type=reward_point_portfolio,
                    user_profile=user_profile
                )
    return True


def advisor_rating_and_ranking(user_profile):
    '''
    Description: Checking the peer rating and client ranking in terms of star and number of users casted
    '''
    advisor = Advisor.objects.get(user_profile = user_profile)
    advisor_rate = AdvisorRating.objects.filter(
        advisor = advisor).exclude(user_type = MEMBER_ROLE).count()
    advisor_rank = AdvisorRating.objects.filter(
        advisor = advisor).exclude(user_type = ADVISOR_ROLE).count()
    reward_point = None
    if advisor_rate:
        if advisor_rate>50:
            reward_point= RewardPoints.objects.filter(
                name = reputation_constants.PEER_RATE_FIFTY).first()
        elif advisor_rate>10 and advisor_rate<50:
            reward_point= RewardPoints.objects.filter(
                name = reputation_constants.PEER_RATE_TEN).first()
        elif advisor_rate>0 and advisor_rate<10:
            reward_point = RewardPoints.objects.filter(
                name = reputation_constants.PEER_RATE_ONE).first()
        ReputationIndex.objects.get_or_create(
            reward_type = reward_point,
            user_profile = user_profile
        )
    return True


def advisor_eipv(advisor):
    '''
    Description: Checking advisor's e-ipv status
    '''
    if advisor.ipv_status:
        reward_point_eipv = RewardPoints.objects.filter(
            name=reputation_constants.EIPV_VERIFIED).first()
        ReputationIndex.objects.get_or_create(
            reward_type=reward_point_eipv,
            user_profile=user_profile
        )
    return True


def crisil_verification(advisor):
    '''
    Description: Checking advisor's crisil certification and business code of conduct
    '''
    #==== Crisil verification
    if advisor.is_crisil_verified:
        crisil_duration = advisor.crisil_expiry_date - datetime.date.today()
        reward_point_crisil = RewardPoints.objects.filter(
            name=CRISIL_GOT_CERTIFICATE).first()
        ReputationIndex.objects.get_or_create(
            reward_type=reward_point_crisil,
            user_profile=user_profile
        )
    #==== Business code of conduct
    upload_documents = UploadDocuments.objects.filter(
        user_profile = user_profile,
        documents_type='code_conduct'
    ).first()
    if upload_documents:
        reward_point_code_conduct = RewardPoints.objects.filter(
            name=reputation_constants.BUSINESS_CODE_CONDUCT).first()
        ReputationIndex.objects.get_or_create(
            reward_type=reward_point_code_conduct,
            user_profile=user_profile
        )
    return True


def advisor_age(user_profile):
    '''
    Description : checking the advisor age
    '''
    reward_point_age = None
    if user_profile.birthdate:
        user_birthdate = user_profile.birthdate
        today = date.today()
        date_format_user_bdate = datetime.datetime.strptime(
            user_birthdate, "%Y-%m-%d").date()
        advisor_age = today.year - date_format_user_bdate.year - (
            (today.month, today.day) < (
                date_format_user_bdate.month, date_format_user_bdate.day)
            )
        if 20 <= advisor_age <= 30:
            reward_point_age = RewardPoints.objects.filter(
                name=reputation_constants.AGE_BETW_20AND30).first()
        elif 30<= advisor_age <= 40:
            reward_point_age = RewardPoints.objects.filter(
                name=reputation_constants.AGE_BETW_30AND40).first()
        elif 40<= advisor_age <= 50:
            reward_point_age = RewardPoints.objects.filter(
                name=reputation_constants.AGE_BETW_40AND50).first()
        elif advisor_age >= 50:
            reward_point_age = RewardPoints.objects.filter(
                name=reputation_constants.AGE_ABOVE50).first()

        if reward_point_age:
            ReputationIndex.objects.get_or_create(
                user_profile= user_profile, 
                reward_type=reward_point_age
            )
    return True


def advisor_office_address(user_profile):
    '''
    Description : checking the advisor office address
    '''
    if user_profile.primary_communication == 'office':
        if user_profile.company_address1 \
            and user_profile.company_address2\
            and user_profile.company_locality \
            and user_profile.company_city \
            and user_profile.company_pincode:
            rewrd_type = RewardPoints.objects.filter(
                name=reputation_constants.ADVISOR_OFFICE_ADDRESS).first()
            ReputationIndex.objects.get_or_create(
                user_profile= user_profile, 
                reward_type=rewrd_type
            )
    return True


def social_media_communication(user_profile):
    '''
    Description :checking advisor's social media communication id's
    '''
    if user_profile.facebook_media:
        reward_point_facebook= RewardPoints.objects.filter(
            name=reputation_constants.ADVISOR_FACEBOOK_ID).first()
        ReputationIndex.objects.get_or_create(
            user_profile=user_profile, 
            reward_type=reward_point_facebook
        )
    if user_profile.google_media:
        reward_point_google = RewardPoints.objects.filter(
            name=reputation_constants.ADVISOR_GOOGLE_ID).first()
        ReputationIndex.objects.get_or_create(
            user_profile=user_profile, 
            reward_type=reward_point_google
        )
    if user_profile.linkedin_media:
        reward_point_linkedin = RewardPoints.objects.filter(
            name=reputation_constants.ADVISOR_LINKEDIN_ID).first()
        ReputationIndex.objects.get_or_create(
            user_profile=user_profile, 
            reward_type=reward_point_linkedin
        )
    if user_profile.twitter_media:
        reward_point_twitter = RewardPoints.objects.filter(
            name=reputation_constants.ADVISOR_TWITTER_ID).first()
        ReputationIndex.objects.get_or_create(
            user_profile=user_profile, 
            reward_type=reward_point_twitter
        )
    return True

def advisor_meetup(user_profile):
    '''
    Description : adding reward points if advisor hosted meetup event
    '''
    meetup_hosted = MeetUpEvent.objects.filter(user_profile=user_profile).count()
    if meetup_hosted:
        if meetup_hosted < 5:
            meetup_reward_point = RewardPoints.objects.filter(
                name=reputation_constants.ADVISOR_MEETUP_HOSTED_BELOW_5).first()
        elif 5 <= meetup_hosted <= 10:
            meetup_reward_point = RewardPoints.objects.filter(
                name=reputation_constants.ADVISOR_MEETUP_HOSTED_BETW_5AND10).first()
        elif 10 <= meetup_hosted <=25:
            meetup_reward_point = RewardPoints.objects.filter(
                name=reputation_constants.ADVISOR_MEETUP_HOSTED_BETW_10AND25).first()

        if meetup_reward_point:
            ReputationIndex.objects.get_or_create(
                user_profile=user_profile, 
                reward_type=meetup_reward_point
            )
    return True


def advisor_webinar(user_profile):
    '''
    Description : adding reward points if advisor hosted meetup event
    '''
    webinar_event_count = TrackWebinar.objects.filter(user_profile=user_profile).count()
    if webinar_event_count:
        if webinar_event_count < 5:
            webinar_reward_point = RewardPoints.objects.filter(
                name=reputation_constants.ADVISOR_WEBINAR_HOSTED_BETW_1AND5).first()
        elif 5 <= webinar_event_count <= 10:
            webinar_reward_point = RewardPoints.objects.filter(
                name=reputation_constants.ADVISOR_WEBINAR_HOSTED_BETW_5AND15).first()
        elif 10 <= webinar_event_count <=25:
            webinar_reward_point = RewardPoints.objects.filter(
                name=reputation_constants.ADVISOR_WEBINAR_HOSTED_ABOVE_15).first()

        if webinar_reward_point:
            ReputationIndex.objects.get_or_create(
                user_profile=user_profile, 
                reward_type=webinar_reward_point
            )
    return True


def totol_clients_served_and_advisors_connected(advisor, user_profile):
    '''
    Description : adding reward points totol clients served and advisors connected
    '''
    if advisor.total_clients_served:
        clients_served_rewrd = None
        if advisor.total_clients_served < 50:
            clients_served_rewrd = RewardPoints.objects.filter(
                name=reputation_constants.TOTAL_CLIENTS_SERVED_BELOW_50).first()
        elif 50 <= advisor.total_clients_served <= 100:
            clients_served_rewrd = RewardPoints.objects.filter(
                name=reputation_constants.TOTAL_CLIENTS_SERVED_BETW_50AND100).first()
        elif 100 <= advisor.total_clients_served <= 500:
            clients_served_rewrd = RewardPoints.objects.filter(
                name=reputation_constants.TOTAL_CLIENTS_SERVED_BELOW_100AND500).first()
        elif advisor.total_clients_served > 500:
            clients_served_rewrd = RewardPoints.objects.filter(
                name=reputation_constants.TOTAL_CLIENTS_SERVED_ABOVE_500).first()

        if clients_served_rewrd:
            ReputationIndex.objects.get_or_create(
                user_profile=user_profile, 
                reward_type=clients_served_rewrd
            )

    if advisor.total_advisors_connected:
        reward_advisor_connected = None
        if advisor.total_advisors_connected < 10:
            reward_advisor_connected = RewardPoints.objects.filter(
                name=reputation_constants.TOTAL_ADVISORS_CONNECTED_BELOW_10).first()
        elif 10 <= advisor.total_advisors_connected <= 50:
            reward_advisor_connected = RewardPoints.objects.filter(
                name=reputation_constants.TOTAL_ADVISORS_CONNECTED_BETW_10AND50).first()
        elif advisor.total_advisors_connected > 50:
            reward_advisor_connected = RewardPoints.objects.filter(
                name=reputation_constants.TOTAL_ADVISORS_CONNECTED_ABOVE_50).first()

        if reward_advisor_connected:
            ReputationIndex.objects.get_or_create(
                user_profile=user_profile, 
                reward_type=reward_advisor_connected
            )
    return True


def advisor_loop_refer(user_profile):
    '''
    Description : adding reward for advisor looped
    '''
    advisor_invited = UserProfile.objects.filter(referred_by_id=user_profile.id)
    referred_register_advisor_count = Advisor.objects.filter(
        is_register_advisor = True, 
        user_profile__referred_by = user_profile.id
    )
    if advisor_invited:
        rewrd_type = RewardPoints.objects.filter(
            name=reputation_constants.ADVISORS_REFERRED).first()
        ReputationIndex.objects.get_or_create(
            user_profile= user_profile, 
            reward_type=rewrd_type
        )
    if referred_register_advisor_count:
        rewrd_type = RewardPoints.objects.filter(
            name=reputation_constants.REFERRED_REGISTERED_ADVISOR).first()
        ReputationIndex.objects.get_or_create(
            user_profile= user_profile, 
            reward_type=rewrd_type
        )
    return True

def advisor_rating(user_profile):
    '''
    Description : checking for advisor looped
    '''
    advisor_rate_invites = AdvisorRating.objects.filter(
        advisor = user_profile.advisor, 
        user_type = "advisor"
    )
    advisor_rated_count = advisor_rate_invites.exclude(avg_rating__lte=0.0).count()
    if advisor_rate_invites.count():
        rewrd_type = RewardPoints.objects.filter(
            name=reputation_constants.ADVISOR_REQUEST_FOR_RATING).first()
        ReputationIndex.objects.get_or_create(
            user_profile = user_profile, 
            reward_type = rewrd_type
        )
    if advisor_rated_count:
        rewrd_type = RewardPoints.objects.filter(
            name=reputation_constants.ADVISOR_RATED).first()
        ReputationIndex.objects.get_or_create(
            user_profile = user_profile, 
            reward_type = rewrd_type
        )
    return True


def member_ranking(user_profile):
    '''
    Description :checking for member ranking
    '''
    advisor_rank_invites = AdvisorRating.objects.filter(
        advisor = user_profile.advisor, 
        user_type = "member"
    )
    advisor_ranked = advisor_rank_invites.exclude(avg_rating__lte=0.0).count()
    if advisor_rank_invites.count():
        rewrd_type = RewardPoints.objects.filter(
            name=reputation_constants.ADVISOR_REQUEST_FOR_RANKING).first()
        ReputationIndex.objects.get_or_create(
            user_profile = user_profile, reward_type = rewrd_type
        )
    if advisor_ranked:
        rewrd_type = RewardPoints.objects.filter(
            name=reputation_constants.ADVISOR_RANKED).first()
        ReputationIndex.objects.get_or_create(
            user_profile = user_profile, 
            reward_type = rewrd_type
        )
    return True


def languages_known(user_profile):
    '''
    Description : checkig for languages known to advisor
    '''
    if user_profile.language_known:
        rewrd_type = None
        language_split = user_profile.language_known.split(",")
        languages_count = len(language_split)
        if languages_count == 1:
            rewrd_type = RewardPoints.objects.filter(
                name=reputation_constants.LANGUAGES_COUNT_ONE).first()
        elif languages_count == 2:
            rewrd_type = RewardPoints.objects.filter(
                name=reputation_constants.LANGUAGES_COUNT_TWO).first()
        elif languages_count == 3:
            rewrd_type = RewardPoints.objects.filter(
                name=reputation_constants.LANGUAGES_COUNT_THREE).first()
        elif languages_count == 4:
            rewrd_type = RewardPoints.objects.filter(
                name=reputation_constants.LANGUAGES_COUNT_FOUR).first()
        elif languages_count >= 5:
            rewrd_type = RewardPoints.objects.filter(
                name=reputation_constants.LANGUAGES_COUNT_ABOVE_5).first()

        if rewrd_type:
            ReputationIndex.objects.get_or_create(
                user_profile = user_profile, 
                reward_type = rewrd_type
            )
    return True


def languages_known_to_read_write(user_profile):
    '''
    Description : checkig for languages known to advisor for read and write
    '''
    if user_profile.languages_known_read_write:
        rewrd_type = None
        language_split = user_profile.languages_known_read_write.split(",")
        languages_read_write_count = len(language_split)
        if languages_read_write_count == 1:
            rewrd_type = RewardPoints.objects.filter(
                name=reputation_constants.LANGUAGES_READ_WRITE_COUNT_1).first()
        elif languages_read_write_count == 2:
            rewrd_type = RewardPoints.objects.filter(
                name=reputation_constants.LANGUAGES_READ_WRITE_COUNT_2).first()
        elif languages_read_write_count == 3:
            rewrd_type = RewardPoints.objects.filter(
                name=reputation_constants.LANGUAGES_READ_WRITE_COUNT_3).first()
        elif languages_read_write_count == 4:
            rewrd_type = RewardPoints.objects.filter(
                name=reputation_constants.LANGUAGES_READ_WRITE_COUNT_4).first()
        elif languages_read_write_count >= 5:
            rewrd_type = RewardPoints.objects.filter(
                name=reputation_constants.LANGUAGES_READ_WRITE_ABOVE_5).first()

        if rewrd_type:
            ReputationIndex.objects.get_or_create(
                user_profile = user_profile, 
                reward_type = rewrd_type
            )
    return True


def advisor_scoring_fb(email=None,access_token=None):
    """
    Used to pass facebook social connect info to textint
    inputs : email, access_token
    """
    if email and access_token:
        rank_fb_url = reputation_constants.RANK_API_URL \
            + reputation_constants.RANK_SCORING_FB
        payload = { "username": str(email), "token": access_token }
        response = requests.post(
            rank_fb_url,
            headers=reputation_constants.RANK_API_KEY_HEADER,
            json=payload,
            verify=SSL_VERIFY
        )
        return response


def advisor_scoring_linkedin(email=None, headLine=None, summary=None):
    """
    Used to pass linkedin social connect info to textint
    inputs : email, headLine, summary
    """
    if email and headLine and summary:
        rank_linkedin_url = reputation_constants.RANK_API_URL \
            + reputation_constants.RANK_SCORING_LINKEDIN
        payload = {
            "username": str(email),
            "headLine": headLine
        }
        if summary:
            payload['summary'] = summary
        response = requests.post(
            rank_linkedin_url,
            headers=reputation_constants.RANK_API_KEY_HEADER,
            json=payload,
            verify=SSL_VERIFY
        )
        return response


def advisor_hyperlocal_scoring(username=None, pincode=None, hyperlocal_type=None):
    """
    Method to call textient api for advisor hyperlocal native or transit scoring
    inputs : username, pincode, hyperlocal_type
    """
    if username and pincode and hyperlocal_type:
        if hyperlocal_type == reputation_constants.HYPERLOCAL_NATIVE:
            native_scoring_url = reputation_constants.RANK_API_URL \
                + reputation_constants.RANK_NATIVE_LOCATION_ADVISOR_SCORING
        else:
            native_scoring_url = reputation_constants.RANK_API_URL \
                + reputation_constants.RANK_TRANSIT_LOCATION_ADVISOR_SCORING
        payload = {
            "username": str(username),
            "pincode": pincode
        }
        logger.info("Native hyperloca url : "+str(native_scoring_url))
        logger.info("Native hyperloca payload : "+str(payload))
        response = requests.post(
            native_scoring_url,
            headers=reputation_constants.RANK_API_KEY_HEADER,
            json=payload,
            verify=SSL_VERIFY
        )
        return response


def advisor_scoring_points(advisor_meta_data=None):
    """
    Used to send and receive the advisor scoring points Trust Index
    input : advisor_meta_data
    """
    advisor_scoring_url = reputation_constants.RANK_API_URL \
        + reputation_constants.RANK_ADVISOR_SCORING
    ri_header = reputation_constants.RANK_API_KEY_HEADER
    logger.info("Reppute url : "+str(advisor_scoring_url))
    logger.info("Reppute payload : "+str(advisor_meta_data))
    if advisor_meta_data:
        payload = advisor_meta_data
        advisor_scoreing_response = requests.post(
            advisor_scoring_url,
            headers=ri_header,
            json=payload,
            verify=SSL_VERIFY
        )
        logger.info(
            "Response for reputation index scoring api response status is "+str(
                advisor_scoreing_response.status_code)
        )
        return advisor_scoreing_response
    else:
        """
        For now to check
        """
        logger.info("advisor_scoring_point: testing ")
        payload = {
            "username": "kantanand.usk@gmail.com",
            "eipv_verified": True,
            "dob": "yyyy-mm-dd",
            "total_languages": 0,
            "facebook_signup": True,
            "google_signup": True,
            "linkedin_signup": True,
            "direct_signup": True,
            "advisors_connected": 0,
            "crisil_verified": True,
            "irda_reg": True,
            "peer_rating": 0,
            "meetups_hosted": 0,
            "webinars_hosted": 0,
            "years_exp": 0,
            "clients_served": 0
        }
        advisor_scoreing_response = requests.post(
            advisor_scoring_url,
            headers=ri_header,
            json=payload, 
            verify=SSL_VERIFY
        )
        return advisor_scoreing_response


def store_advisor_insurance_meta_data(data=None):
    '''
    Method store_advisor_insurance_meta_data is to store required data to db, which is used to calculate score
    param : data (Its dictionary of fields, to be stored)
    '''
    if data:
        advisor_meta_data, created = ReputationIndexMetaData.objects.get_or_create(
            user_profile = data.get('user_profile',None)
        )
        # if not created:
        for k,v in data.iteritems():
            #code to store data to db
            setattr(advisor_meta_data,k,v)
        logger.info("ReputationIndexMetaData updating ...")

        # Commnted for future reference
        # else:
        #     logger.info("ReputationIndexMetaData creating ...")
        #     advisor_meta_data.facebook_signup = data.get('facebook_signup',None),
        #     advisor_meta_data.google_signup = data.get('google_signup',None),
        #     advisor_meta_data.direct_signup = data.get('direct_signup',None),
        #     advisor_meta_data.linkedin_signup = data.get('linkedin_signup',None)
        advisor_meta_data.save()
        logger.info("ReputationIndexMetaData save operation is successfully completed")
        return advisor_meta_data
    return None


def adv_scoring_point_for_insurance(advisor_meta_data):
    #Call to reputation index api call.
    serializer = ReputationIndexMetaDataSerializer(advisor_meta_data)
    advisor_scoring_points(jsom.dumps(serializer.data))


def get_insurance_metadata_by_user_profile(user_profile_instance):
    return ReputationIndexMetaData.objects.filter(
        user_profile=user_profile_instance).first()


def get_advisor_reputation_index_by_user_profile(user_profile_instance):
    return AdvisorReputationIndex.objects.filter(
        user_profile=user_profile_instance).first()


def get_insurance_metadata_by_pk(meta_data_id):
    return ReputationIndexMetaData.objects.filter(pk=meta_data_id).first()


def get_user_profile_by_email(email):
    return UserProfile.objects.filter(email=email).first()


def get_user_profile_by_id(id):
    return UserProfile.objects.filter(id=id).first()


def get_user_profile_by_advisor_id(adv_instance):
    adv = Advisor.objects.filter(id=adv_instance.id).first()
    if adv:
        return adv.user_profile
    return None


def save_advisor_reputation_index(email=None, advisor_reputation_data=None):
    '''
    Saving Advisor score in to AdvisorReputationIndex table
    '''
    if advisor_reputation_data and email:
        user_profile_instance = get_user_profile_by_email(email)
        if user_profile_instance:
            advisor_reputation_index, created = \
                AdvisorReputationIndex.objects.get_or_create(
                    user_profile = user_profile_instance
                )
            advisor_reputation_index.insurance = advisor_reputation_data
            advisor_reputation_index.save()
            logger.info(
                "Advisor scoring api response stored to AdvisorReputationIndex \
                successfully"
            )
            return advisor_reputation_index


def get_pincode_by_lat_long(lat=None, long=None):
    '''
    Getting pincode using latitude and longitude
    '''
    res = {}
    is_success = False
    if lat and long:
        geonames_url = reputation_constants.API_GOOGLE_GEONAMES\
                        +"?lat="+str(lat)\
                        +"&lng="+str(long)\
                        +"&username="+str(reputation_constants.KEY_GOOGLE_GEONAMES)\
                        +"&type=json"
        res = requests.get(geonames_url)
        if res.status_code == 200:
            is_success = True
            res = json.loads(res.text)
    return res, is_success


def advisors_rank_api(username=None, pincode=None):
    '''
    Getting Ranking score by pincode
    '''
    res = None
    if username and pincode:
        advisors_rank_url = reputation_constants.RANK_API_URL \
            + reputation_constants.RANK_ADVISORS_RANKING_API
        ri_header = reputation_constants.RANK_API_KEY_HEADER
        payload = {"username":username,"pincode":pincode}
        res = requests.post(
            advisors_rank_url,
            headers=ri_header, 
            json=payload, 
            verify=SSL_VERIFY
        )
        logger.info(
            "Response for reputation index rank api response status is "+str(
                res.status_code)
        )
    return res


def check_regulatory_reg_validation(exp_date):
    '''
    Checking Regulatory registration expire date
    '''
    if exp_date:
        if isinstance(exp_date, str):
            exp_date = datetime.datetime.strptime(exp_date, '%Y-%m-%d').date()
        td = datetime.date.today()
        if td < exp_date:
            return True
    return False


def construct_education_details_json(user_profile_instance=None):
    """
    used to return highest education category field
    input params: user_profile instance 
    """
    if user_profile_instance:
        edu_cat = getattr(user_profile_instance, "education_category", None)
        year_passout = getattr(user_profile_instance, "year_passout", "0")
        deg_name =  getattr(user_profile_instance, "qualification", None)
        univ_ins =  getattr(user_profile_instance, "college_name", None)
        add_qualification = getattr(
            user_profile_instance, "additional_qualification", None)
        _education_details_json_template = {
            "deg_type":"other_qualification",
            "year_passout": "0",
            "premium_inst": 0,
            "special_mba_diploma": 0,
            "prof_in_other_sub": 0
        }
        _special_mab_diploma_edu_cat = []
        _flag_filed = False
        _premium_edu_cat_array = [PROFESSIONAL_QUALIFICATION,OTHER_QUALIFICATION]
        #  check for education category
        if edu_cat:
            _flag_filed = HIGHEST_EDU_DICT.get(edu_cat, False)
            # set year of passout
            _education_details_json_template['year_passout'] = str(year_passout)
            # check for prime instute
            if edu_cat in _premium_edu_cat_array and univ_ins in PREMIUM_INSTUTIONS_LIST:
                _education_details_json_template['premium_inst'] = 1
            # set the education deg_type 
            if _flag_filed:
                _education_details_json_template['deg_type'] = _flag_filed
            # checking for specialization in mba or diploma
            if edu_cat in EDU_CAT_SPL_IN_MBA_OR_DIP_LIST:
                # check for additional qualification 
                if add_qualification:
                    _is_special_mba_diploma = False
                    for qualification in json.loads(add_qualification):
                        if qualification['additional_qualification'] in \
                            ADD_QUALIFICATION_IN_MBA_OR_DIP_LIST:
                            _is_special_mba_diploma = True
                    if _is_special_mba_diploma:
                        _education_details_json_template['special_mba_diploma'] = 1
            # checking for other qualification 
            if add_qualification:
                _is_prof_in_other_sub = False
                for qualification in json.loads(add_qualification):
                    if qualification['additional_qualification'] in PROF_IN_ADD_SUB:
                        _is_prof_in_other_sub = True
                if _is_prof_in_other_sub:
                        _education_details_json_template['prof_in_other_sub'] = 1
            return _education_details_json_template
        else:
            return None
    else:
        return None
