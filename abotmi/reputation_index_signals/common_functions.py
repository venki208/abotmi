import json, logging, datetime,ast
from common import constants as common_constants
from common.views import get_exp_from_financial_instruments_for_type, get_number_of_language, get_advisor_meetup_hosted_count, get_advisor_webinar_hosted_count, get_advisor_rating, get_advisor_education_detils, get_no_of_regulatory_registrations, get_advisor_associated_organization_count, check_rera_reg_state_same_as_practice_state, get_adv_rate_count_by_user_type
from reputation_index.common_functions import get_insurance_metadata_by_user_profile, store_advisor_insurance_meta_data, get_user_profile_by_id, get_user_profile_by_advisor_id, check_regulatory_reg_validation
from reputation_index.common_functions import construct_education_details_json
from reputation_index import constants as rpi_constants
logger = logging.getLogger(__name__)

def check_data_change_for_reputation_index(instance, table_name, category):
    if category == common_constants.INSURANCE_FINANCIAL_INSTRUMENTS:
        insurance_call_data_check_by_table(table_name, instance)

def insurance_call_data_check_by_table(table_name, instance):
    if table_name == common_constants.TABLE_USER_PROFILE:
        insurance_user_profile_data_store(instance)
    elif table_name == common_constants.TABLE_ADVISOR:
        insurance_advisor_data_store(instance)
    elif table_name == common_constants.TABLE_ADVISOR_RATING:
        insurance_advisor_rating_data_store(instance)
    elif table_name == common_constants.TABLE_MEETUP_EVENT:
        insurance_meetup_event_data_store(instance)
    elif table_name == common_constants.TABLE_TRACK_WEBINAR:
        insurance_track_webinar_data_check(instance)
    elif table_name == common_constants.TABLE_BSE_DATA:
        bse_data_store(instance)
    elif table_name == common_constants.TABLE_COMPANY_ADVISOR_MAPPING:
        company_advisor_mapping_data_store(instance)

def insurance_user_profile_data_store(instance):
    #In this function some come has been commented for future reference
    insurance_meta_obj = get_insurance_metadata_by_user_profile(instance)
    # instance.total_languages= 0
    # instance.dob = ""
    need_to_store = False
    instance.education_details = None
    instance.ekyc = True if instance.adhaar_card else False
    instance.pan = 2 if instance.pan_no else 0
    education_details = construct_education_details_json(user_profile_instance=instance)
    if education_details:
        instance.education_details = json.dumps(education_details)
    # instance.no_sm_connected = json.dumps(total_sm_connected(instance))
    # edu_details = get_advisor_education_detils(instance)
    # instance.edu = json.dumps(edu_details) if edu_details else None
    if insurance_meta_obj:
        # instance.total_languages = get_number_of_language(instance.language_known)
        # if instance.birthdate:
        #     instance.dob = str(instance.birthdate)

        # put below code in following if condition
        # instance.dob != str(insurance_meta_obj.dob) or \
        # instance.edu != insurance_meta_obj.edu or \
        # instance.no_sm_connected != insurance_meta_obj.no_sm_connected:
        #instance.total_languages != insurance_meta_obj.total_languages or \
        if instance.ekyc != insurance_meta_obj.ekyc or \
            instance.pan != insurance_meta_obj.pan or \
            instance.pincode_old != instance.pincode or \
            instance.education_details != insurance_meta_obj.education_details:
            need_to_store = True
    else:
        need_to_store = True
    if need_to_store:
        meta_obj = user_profile_get_insurance_meta_obj_to_store(instance, insurance_meta_obj)
        logger.info("UserProfile fields for reputation index got changed")
        store_advisor_insurance_meta_data(meta_obj)

def insurance_advisor_data_store(instance):
    #In this function some come has been commented for future reference
    insurance_meta_obj = get_insurance_metadata_by_user_profile(instance.user_profile)
    need_to_store = False
    instance.is_irda = True if instance.irda_number else False
    instance.is_sebi = True if instance.sebi_number else False
    instance.is_amfi = True if instance.amfi_number else False
    instance.is_amfi_validate = check_regulatory_reg_validation(instance.amfi_expiry_date)
    instance.is_sebi_validate = check_regulatory_reg_validation(instance.sebi_expiry_date)
    instance.is_irda_validate = check_regulatory_reg_validation(instance.irda_expiry_date)
    instance.eipv_verified = 2 if instance.ipv_status else 0
    instance.is_rera_reg_in_practice_state = check_rera_reg_state_same_as_practice_state(instance)
    if insurance_meta_obj:
        # instance.is_rera = instance.is_rera
        # instance.no_reg_regs, instance.no_reg_regs_validate = get_no_of_regulatory_registrations(instance)
        # instance.no_reg_regs_validate = json.dumps(instance.no_reg_regs_validate)
        # instance.years_exp = get_exp_from_financial_instruments_for_type(instance.financial_instruments, common_constants.INSURANCE_FINANCIAL_INSTRUMENTS)

        # put below code in following if condition
        # instance.total_advisors_connected != insurance_meta_obj.advisors_connected or \
        # instance.is_crisil_verified != insurance_meta_obj.crisil_verified or \
        # instance.total_clients_served != insurance_meta_obj.clients_served or \
        # instance.years_exp != insurance_meta_obj.years_exp or \
        # instance.is_rera != insurance_meta_obj.is_rera or \
        # instance.no_reg_regs != insurance_meta_obj.no_reg_regs or \
        # instance.no_reg_regs_validate != insurance_meta_obj.no_reg_regs_validate:
        # instance.ipv_status != insurance_meta_obj.eipv_verified or \
        if instance.is_irda != insurance_meta_obj.is_irda or \
            instance.is_amfi != insurance_meta_obj.is_amfi or \
            instance.is_sebi != insurance_meta_obj.is_sebi or \
            instance.is_sebi_validate != insurance_meta_obj.is_sebi_validate or \
            instance.is_amfi_validate != insurance_meta_obj.is_amfi_validate or \
            instance.is_irda_validate != insurance_meta_obj.is_irda_validate or \
            instance.eipv_verified != insurance_meta_obj.eipv_verified or \
            instance.is_rera_reg_in_practice_state != insurance_meta_obj.is_rera_reg_in_practice_state:
            need_to_store = True
    else:
        need_to_store = True
    if need_to_store:
        meta_obj = advisor_get_insurance_meta_obj_to_store(instance)
        logger.info("Advisor fields for reputation index got changed")
        store_advisor_insurance_meta_data(meta_obj)

def insurance_advisor_rating_data_store(instance):
    #In this function some come has been commented for future reference
    need_to_store = False
    instance.user_profile = get_user_profile_by_advisor_id(instance.advisor)
    insurance_meta_obj = get_insurance_metadata_by_user_profile(instance.user_profile)
    instance.client_rate_count,instance.percent_client_rating = get_adv_rate_count_by_user_type(instance.advisor, common_constants.MEMBER_ROLE)
    instance.peer_rate_count, instance.percent_peer_rating = get_adv_rate_count_by_user_type(instance.advisor, common_constants.ADVISOR_ROLE)
    if insurance_meta_obj:
        if instance.client_rate_count != insurance_meta_obj.client_rate_count or \
            instance.peer_rate_count != insurance_meta_obj.peer_rate_count or \
            instance.percent_peer_rating != insurance_meta_obj.percent_peer_rating or \
            instance.percent_client_rating != insurance_meta_obj.percent_client_rating:
            need_to_store = True
    else:
        need_to_store = True

    if need_to_store:
        meta_obj = advisor_rating_get_insurance_meta_obj_to_store(instance)
        logger.info("AdvisorRating fields for reputation index got changed")
        store_advisor_insurance_meta_data(meta_obj)

def insurance_meetup_event_data_store(instance):
    insurance_meta_obj = get_insurance_metadata_by_user_profile(instance.user_profile)
    if insurance_meta_obj:
        instance.meetups_hosted = get_advisor_meetup_hosted_count(instance.user_profile)
        if instance.meetups_hosted != insurance_meta_obj.meetups_hosted:
            meta_obj = meetup_event_get_insurance_meta_obj_to_store(instance)
            logger.info("MeetUpEvent fields for reputation index got changed")
            store_advisor_insurance_meta_data(meta_obj)

def insurance_track_webinar_data_check(instance):
    insurance_meta_obj = get_insurance_metadata_by_user_profile(instance.user_profile)
    if insurance_meta_obj:
        instance.webinars_hosted = get_advisor_webinar_hosted_count(instance.user_profile)
        if instance.webinars_hosted != insurance_meta_obj.webinars_hosted:
            meta_obj = webinar_get_insurance_meta_obj_to_store(instance)
            logger.info("TrackWebinar fields for reputation index got changed")
            store_advisor_insurance_meta_data(meta_obj)

def bse_data_store(instance):
    instance.user_profile = get_user_profile_by_id(instance.advisor_id.user_profile.id)
    insurance_meta_obj = get_insurance_metadata_by_user_profile(instance.user_profile)
    instance.disciplinary_action = False if instance.diciplinery_action_against_ap != "Y" else True
    if instance.diciplinery_action_against_ap != instance.disciplinary_action:
        meta_obj = bse_data_get_insurance_meta_obj_to_store(instance)
        store_advisor_insurance_meta_data(meta_obj)

def company_advisor_mapping_data_store(instance):
    insurance_meta_obj = get_insurance_metadata_by_user_profile(instance.advisor_user_profile)
    instance.associated_organization = get_advisor_associated_organization_count(instance.advisor_user_profile)
    if instance.associated_organization != insurance_meta_obj.associated_organization:
        meta_obj = company_adv_mapping_get_insurance_meta_obj_to_store(instance)
        store_advisor_insurance_meta_data(meta_obj)

def advisor_rating_get_insurance_meta_obj_to_store(instance):
    #In this function some come has been commented for future reference
    advisor_meta_obj = {"username" : instance.user_profile.email, "user_profile" : instance.user_profile}
    # advisor_meta_obj['peer_rating'] = instance.peer_rating
    advisor_meta_obj['client_rate_count'] = instance.client_rate_count
    advisor_meta_obj['peer_rate_count'] = instance.peer_rate_count
    advisor_meta_obj['percent_peer_rating'] = instance.percent_peer_rating
    advisor_meta_obj['percent_client_rating'] = instance.percent_client_rating
    return advisor_meta_obj

def webinar_get_insurance_meta_obj_to_store(instance):
    advisor_meta_obj = {"username" : instance.user_profile.email, "user_profile" : instance.user_profile}
    advisor_meta_obj['webinars_hosted'] = instance.webinars_hosted
    return advisor_meta_obj

def meetup_event_get_insurance_meta_obj_to_store(instance):
    advisor_meta_obj = {"username" : instance.user_profile.email, "user_profile" : instance.user_profile}
    advisor_meta_obj['meetups_hosted'] = instance.meetups_hosted
    return advisor_meta_obj

def advisor_get_insurance_meta_obj_to_store(instance):
    #In this function some come has been commented for future reference
    advisor_meta_obj = {"username" : instance.user_profile.email, "user_profile" : instance.user_profile}
    # advisor_meta_obj['eipv_verified'] = instance.ipv_status
    # advisor_meta_obj['advisors_connected'] = instance.total_advisors_connected
    # advisor_meta_obj['crisil_verified'] = instance.is_crisil_verified
    advisor_meta_obj['is_rera_reg_in_practice_state'] = instance.is_rera_reg_in_practice_state
    advisor_meta_obj['is_irda'] = instance.is_irda
    advisor_meta_obj['is_amfi'] = instance.is_amfi
    advisor_meta_obj['is_sebi'] = instance.is_sebi
    advisor_meta_obj['eipv_verified'] = instance.eipv_verified
    advisor_meta_obj['is_amfi_validate'] = instance.is_amfi_validate
    advisor_meta_obj['is_sebi_validate'] = instance.is_sebi_validate
    advisor_meta_obj['is_irda_validate'] = instance.is_irda_validate
    # advisor_meta_obj['years_exp'] = instance.years_exp
    # advisor_meta_obj['clients_served'] = instance.total_clients_served
    # advisor_meta_obj['is_rera'] = instance.is_rera
    # advisor_meta_obj['no_reg_regs'] = instance.no_reg_regs
    # advisor_meta_obj['no_reg_regs_validate'] = instance.no_reg_regs_validate
    return advisor_meta_obj

def user_profile_get_insurance_meta_obj_to_store(instance, ri_meta):
    #In this function some come has been commented for future reference
    advisor_meta_obj = {"username" : instance.email, "user_profile" : instance}
    # advisor_meta_obj = get_signup_detail_obj(instance, advisor_meta_obj)
    # advisor_meta_obj['total_languages'] = instance.total_languages
    # advisor_meta_obj['dob'] = instance.dob
    advisor_meta_obj['ekyc'] = instance.ekyc
    advisor_meta_obj['pan'] = instance.pan
    advisor_meta_obj['education_details'] = instance.education_details
    # advisor_meta_obj['no_sm_connected'] = instance.no_sm_connected
    # advisor_meta_obj['edu'] = instance.edu
    pincode_arr = []
    if instance.pincode:
        if ri_meta:
            if ri_meta.pincodes:
                try:
                    pincode_arr = ast.literal_eval(ri_meta.pincodes)
                    if instance.pincode not in pincode_arr:
                        pincode_arr = [instance.pincode]
                        #Below code for practice location
                        #pincode_arr.append(int(instance.pincode))
                except:
                    pass
        if not pincode_arr:
            pincode_arr = [instance.pincode]
            #Below code for practice location
            # pincode_arr.append(int(instance.pincode))

    advisor_meta_obj['pincodes'] = str(pincode_arr)
    return advisor_meta_obj

def get_signup_detail_obj(instance, advisor_meta_obj):
    if instance.source_media == common_constants.SIGNUP_WITH_EMAIL:
        advisor_meta_obj['direct_signup'] = True
        advisor_meta_obj['facebook_signup'] = False
        advisor_meta_obj['google_signup'] = False
        advisor_meta_obj['linkedin_signup'] = False
    elif instance.source_media == common_constants.FACEBOOK_MEDIA:
        advisor_meta_obj['facebook_signup'] = True
        advisor_meta_obj['direct_signup'] = False
        advisor_meta_obj['google_signup'] = False
        advisor_meta_obj['linkedin_signup'] = False
    elif instance.source_media == common_constants.LINKEDIN_MEDIA:
        advisor_meta_obj['linkedin_signup'] = True
        advisor_meta_obj['facebook_signup'] = False
        advisor_meta_obj['google_signup'] = False
        advisor_meta_obj['direct_signup'] = False
    elif instance.source_media == common_constants.GOOGLE_MEDIA:
        advisor_meta_obj['google_signup'] = True
        advisor_meta_obj['facebook_signup'] = False
        advisor_meta_obj['direct_signup'] = False
        advisor_meta_obj['linkedin_signup'] = False
    else:
        advisor_meta_obj['google_signup'] = False
        advisor_meta_obj['facebook_signup'] = False
        advisor_meta_obj['direct_signup'] = False
        advisor_meta_obj['linkedin_signup'] = False

    if instance.facebook_media:
        advisor_meta_obj['facebook_media'] = True
    if instance.linkedin_media:
        advisor_meta_obj['linkedin_media'] = True
    if instance.google_media:
        advisor_meta_obj['google_media'] = True
    return advisor_meta_obj

def bse_data_get_insurance_meta_obj_to_store(instance):
    advisor_meta_obj = {"username" : instance.user_profile.email, "user_profile" : instance.user_profile}
    advisor_meta_obj['disciplinary_action'] = instance.disciplinary_action
    return advisor_meta_obj

def company_adv_mapping_get_insurance_meta_obj_to_store(instance):
    advisor_meta_obj = {"username" : instance.advisor_user_profile.email, "user_profile" : instance.advisor_user_profile}
    advisor_meta_obj['associated_organization'] = instance.associated_organization
    return advisor_meta_obj

def total_sm_connected(instance):
    sm_connected = {}
    sm_connected['facebook'] = True if instance.facebook_media else False
    sm_connected['linkedin'] = True if instance.linkedin_media else False
    sm_connected['google'] = True if instance.google_media else False
    return sm_connected
