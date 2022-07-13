import logging
from reia.celery import app as celery_app
from common.views import create_user_from_uploaded_file
logger = logging.getLogger(__name__)

@celery_app.task(name="bulk_advisor_data_creation", ignore_result=True)
def bulk_advisor_data_creation(advisor_data,user_profile_id):
    logger.info("CELERY for bulk advisor data creation ...")
    create_user_from_uploaded_file(advisor_data, user_profile_id)
    logger.info("CELERY for bulk advisor data creation ...complete ")
