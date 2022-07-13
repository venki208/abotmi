from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import json
from reputation_index.serializers import ReputationIndexMetaDataSerializer
from datacenter.models import UserProfile, Advisor, AdvisorRating, MeetUpEvent, TrackWebinar, ReputationIndexMetaData, CompanyAdvisorMapping
from advisor_check.models import BseData
from reputation_index.common_functions import store_advisor_insurance_meta_data, get_insurance_metadata_by_user_profile, advisor_scoring_points, save_advisor_reputation_index, get_insurance_metadata_by_pk
from reputation_index_signals.common_functions import check_data_change_for_reputation_index
from common import constants as common_constants
from reputation_index import constants as reputation_constants
from reputation_index_signals.tasks import advisor_scoring_point_api_process, hyperlocal_advisor_scoring
from common.views import get_practice_locations

@receiver(pre_save, sender=UserProfile)
def pre_save_user_profile(sender, instance, *args, **kwargs):
    if instance.is_advisor:
        instance.pincode_old = None
        if instance.pincode:
            instance.pincode_old = instance.__class__.objects.get(id=instance.id).pincode

@receiver(post_save, sender=UserProfile)
def post_save_user_profile(sender, instance, created, **kwargs):
    if instance.is_advisor:
        check_data_change_for_reputation_index(instance, instance.__class__.__name__, common_constants.INSURANCE_FINANCIAL_INSTRUMENTS)
        #Below code commented for future reference
        #Call api to hyperlocal
        # if instance.pincode and instance.pincode_old != instance.pincode:
        #     try:
        #         pin = int(instance.pincode)
        #         hyperlocal_advisor_scoring.apply_async((instance.email, pin, reputation_constants.HYPERLOCAL_NATIVE,))
        #     except:
        #         pass

@receiver(pre_save, sender=Advisor)
def pre_save_advisor(sender, instance, *args, **kwargs):
    instance.practice_details_old = None
    if instance.practice_details:
        instance.practice_details_old = instance.__class__.objects.get(id=instance.id).practice_details

@receiver(post_save, sender=Advisor)
def post_save_advisor(sender, instance, created, **kwargs):
    check_data_change_for_reputation_index(instance, instance.__class__.__name__, common_constants.INSURANCE_FINANCIAL_INSTRUMENTS)
    #Following code commeted for furure use
    # if instance.practice_details and instance.practice_details_old != instance.practice_details:
    #     try:
    #         practice_pincode_arr = get_practice_locations(instance)
    #         if practice_pincode_arr:
    #             practice_pincode_arr = [int(pincode) for pincode in practice_pincode_arr]
    #             hyperlocal_advisor_scoring.apply_async((instance.email, practice_pincode_arr, reputation_constants.HYPERLOCAL_NATIVE,))
    #     except:
    #         pass

@receiver(post_save, sender=ReputationIndexMetaData)
def post_save_insurance_meta_data(sender, instance, created, **kwargs):
    insurance_meta_obj = get_insurance_metadata_by_pk(instance.id)
    serializers = ReputationIndexMetaDataSerializer(insurance_meta_obj)
    advisor_scoring_point_api_process.apply_async((serializers.data,instance.user_profile.email,))

@receiver(post_save, sender=AdvisorRating)
def post_save_advisor_rating(sender, instance, created, **kwargs):
    check_data_change_for_reputation_index(instance, instance.__class__.__name__, common_constants.INSURANCE_FINANCIAL_INSTRUMENTS)

#Following code commented for future user
# @receiver(post_save, sender=MeetUpEvent)
# def post_save_meetup_event(sender, instance, created, **kwargs):
#     check_data_change_for_reputation_index(instance, instance.__class__.__name__, common_constants.INSURANCE_FINANCIAL_INSTRUMENTS)
#
# @receiver(post_save, sender=TrackWebinar)
# def post_save_track_webinar(sender, instance, created, **kwargs):
#     check_data_change_for_reputation_index(instance, instance.__class__.__name__, common_constants.INSURANCE_FINANCIAL_INSTRUMENTS)


# @receiver(post_save, sender=BseData)
# def post_save_bse_data(sender, instance, created, **kwargs):
#     pass
#     # check_data_change_for_reputation_index(instance, instance.__class__.__name__, common_constants.INSURANCE_FINANCIAL_INSTRUMENTS)
#
# @receiver(post_save, sender=CompanyAdvisorMapping)
# def post_save_company_advisor_mapping_data(sender, instance, created, **kwargs):
#     check_data_change_for_reputation_index(instance, instance.__class__.__name__, common_constants.INSURANCE_FINANCIAL_INSTRUMENTS)
