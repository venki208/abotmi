# python lib
import logging

# Third party modules
from celery import Task

# Database Models
from datacenter.models import UserProfile,BlockchainAccounts

# Local Imports
from reia.celery import app as celery_app
from blockchain.views import create_blockchain_account

logger = logging.getLogger(__name__)

@celery_app.task(name="blockchain_task")
def create_user_blockchain_account_and_transaction(user_profile_id):
    logger.info("Blockchain Started")
    return create_blockchain_account(user_profile_id)