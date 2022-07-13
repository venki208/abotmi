import logging, ast
from reia.celery import app as celery_app
from reputation_index.common_functions import  get_insurance_metadata_by_pk, advisor_scoring_points, save_advisor_reputation_index, advisor_hyperlocal_scoring, get_user_profile_by_email
from reputation_index.serializers import ReputationIndexMetaDataSerializer
from reputation_index import constants as reputation_constants
logger = logging.getLogger(__name__)

@celery_app.task(name="advisor_scoring_point_api_process", ignore_result=True)
def advisor_scoring_point_api_process(meta_data, email):
    logger.info("CELERY for advisor_scoring_point_api_process called ...")
    result =  advisor_scoring_points(meta_data)
    logger.info("Advisor scoring api response code = "+str(result.status_code))
    if result.status_code == 200:
        save_advisor_reputation_index(email, result.text)
        up_instance = get_user_profile_by_email(email)
        logger.info("CELERY for hyperlocal_advisor_scoring called for = "+str(up_instance.email))
        logger.info(meta_data)
        logger.info("--------------------")
        pin_arr = meta_data['pincodes']
        if pin_arr:
            try:
                pin_arr = ast.literal_eval(pin_arr)
                if pin_arr:
                    pin = pin_arr[0]
                    if pin:
                        hl_result = advisor_hyperlocal_scoring(username=email, pincode=pin, hyperlocal_type=reputation_constants.HYPERLOCAL_NATIVE)
                        logger.info("HYPERLOCAL native hl_result status code, after scoring called = "+str(hl_result.status_code))
            except:
                pass
        #Following code used for future use
        # if up_instance and up_instance.pincode:
        #     pincode = int(up_instance.pincode)
        #     hl_result = advisor_hyperlocal_scoring(username=email, pincode=pincode, hyperlocal_type=reputation_constants.HYPERLOCAL_NATIVE)
        #     logger.info("HYPERLOCAL native hl_result status code, after scoring called = "+str(hl_result.status_code))


@celery_app.task(name="hyperlocal_advisor_scoring", ignore_result=True)
def hyperlocal_advisor_scoring(username, pincode, hyperlocal_type):
    logger.info("CELERY for hyperlocal_advisor_scoring called ...")
    result = advisor_hyperlocal_scoring(username=username, pincode=pincode, hyperlocal_type=hyperlocal_type)
    logger.info("HYPERLOCAL native result status code, once pincode is cahnged = "+str(result.status_code))
