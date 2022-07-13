# python lib
import json
import logging
import requests

# Django Modules
from django.shortcuts import render

# Third Party Modules
from pyethmobisir import EthJsonRpc

# Database Models
from datacenter.models import BlockchainAccounts,BlockchainContracts,UserProfile
# Constatns
from common import constants

logger = logging.getLogger(__name__)
blockchain_url = constants.BLOCKCHAIN_URL


def start_mining():
    '''
    To start mining for transactions
    curl -X POST --data '{"jsonrpc":"2.0","method":"miner_start",
        "params":[],"id":67}' http://localhost:8545
    '''
    api_data = '{"jsonrpc":"2.0","method":"miner_start", "params":[],"id":"1"}'
    response = requests.post(
        blockchain_url, 
        api_data,
        verify=constants.BLOCKCHAIN_SSL_VERFIY
    )
    logger.info("Mining Started")


def stop_mining():
    '''
    To stop mining, once transactions is done
    curl -X POST --data '{"jsonrpc":"2.0","method":"miner_stop",
        "params":[],"id":67}' http://localhost:8545
    '''
    api_data = '{"jsonrpc":"2.0","method":"miner_stop", "params":[],"id":"1"}'
    response = requests.post(
        blockchain_url, 
        api_data,
        verify=constants.BLOCKCHAIN_SSL_VERFIY
    )
    logger.info("Mining Stopped")


def is_pending_transaction():
    '''
    Check Pending Transaction or not
    curl -X POST --data '{"jsonrpc":"2.0","method":"eth_getBlockByNumber",
        "params":["pending", true],"id":67}' http://localhost:8545
    '''
    api_data = '{"jsonrpc":"2.0","method":"eth_getBlockByNumber", \
        "params":["pending", true],"id":"1"}'
    response = requests.post(
        blockchain_url, 
        api_data,
        verify=constants.BLOCKCHAIN_SSL_VERFIY
    )
    data = json.loads(response.content)
    data = data['result']['transactions']
    logger.info("Pending Transaction"+str(data))
    return data


def mining():
    while is_pending_transaction():
        logger.info("mining......")
        start_mining()
    stop_mining()


def unlock_blockchain_account(account):
    '''
    Unlock blockchain account for the register advisor
    curl -X POST --data '{"jsonrpc":"2.0","method":"personal_unlockAccount",
        "params":["0x7642b...", "password"],"id":67}' http://localhost:8545
    '''

    if account == "admin":
        account  = constants.BLOCKCHAIN_ADMIN_ACCOUNT
        id = "1"
    else:
        account = account.account
        id = account.id
    api_data = '{"jsonrpc":"2.0","method":"personal_unlockAccount",\
        "params":["'+account+'","'+constants.BLOCKCHAIN_ADMIN_PWD+'"],\
        "id":"advisor-'+id+'"}'
    unlock_response = requests.post(
        blockchain_url, 
        api_data,
        verify=constants.BLOCKCHAIN_SSL_VERFIY
    )
    logger.info("Unlock Response"+str(unlock_response))

def create_blockchain_account(user_profile_id):
    '''
    Create blockchain account for the register advisor
    curl -X POST --data '{"jsonrpc":"2.0","method":"personal_newAccount",
        "params":  ["restart"],"id":74}' http://0.0.0.xxx:8545
    '''
    try:
        user_details = ""
        user_profile = UserProfile.objects.get(pk=user_profile_id)
        unlock_blockchain_account("admin")
        contract_detail = BlockchainContracts.objects.filter(name=constants.KYC_CONTRACT)
        logger.info("Fetched Contract Details")
        if contract_detail:    
            contract_detail = contract_detail.first()
            '''
            create record in Blockchain accounts table for the user with user profile id 
            and contract_address
            '''
            data,is_created = BlockchainAccounts.objects.get_or_create(
                user_profile=user_profile,
                contract_address=contract_detail
            )
            if not data.is_account_created:
                api_data = '{"jsonrpc":"2.0","method":"personal_newAccount","params":["'\
                +constants.BLOCKCHAIN_ADMIN_PWD+'"],"id":"advisor-'+str(user_profile.id)\
                +'"}' 
                try:
                    accounts_response = requests.post(
                        blockchain_url,
                        api_data,
                        verify=constants.BLOCKCHAIN_SSL_VERFIY
                    )
                    account_address = accounts_response.json()['result']
                    data.accounts = account_address
                    data.is_account_created = 1
                    data.save()
                    logger.info("Blockchain Accounts created for"+ str(user_profile.email))
                except:
                    pass
            else:
                logger.info(
                    "Already Blockchain Accounts created for"+ str(user_profile.email))
                account_address = data.accounts
            try:
                #store the user details using the contract KYC_CONTRACT
                #if any column has None object convert the string to empty ''
                user_details = account_address+","+str(user_profile.first_name or '')+","\
                +str(user_profile.last_name or '')+","+str(user_profile.father_name or '')\
                +str(user_profile.birthdate or '')+str(user_profile.gender or '')+","\
                +str(user_profile.address or '')+str(user_profile.mobile or '') \
                +","+str(user_profile.email or '')+","+str(user_profile.adhaar_card or '')\
                +","+str(user_profile.passport_no or '')
                eth_connection = EthJsonRpc(
                    constants.BLOCKCHAIN_IP,
                    constants.BLOCKCHAIN_PORT,
                    tls=constants.BLOCKCHAIN_TLS
                )
                transaction = eth_connection.call_with_transaction(
                    eth_connection.eth_coinbase(),
                    contract_detail.contract_address,
                    'set_s(string)',
                    [user_details]
                )
                '''
                save the transaction id of the above process to retrieve the stored details of the user
                '''
                data.accounts_creation_transaction_id = transaction
                data.save()
                mining()
                logger.info(
                    "Set user data with Blockchain Accounts"+ str(user_profile.email))
            except:
                logger.info("set data Except Error")
    except:
        logger.info("creating blockchian Except Error")

def get_userdetails_by_transactionid(transaction_id):
    '''
    get decoded stored user details for the given transction_id
    '''
    try:
        unlock_blockchain_account("admin")
        eth_connection = EthJsonRpc(
            constants.BLOCKCHAIN_IP,
            constants.BLOCKCHAIN_PORT,
            tls=constants.BLOCKCHAIN_TLS
        )
        get_transaction_details = eth_connection.eth_getTransactionByHash(transaction_id)
        get_input_hex = get_transaction_details['input']
        get_readable_detail = get_input_hex[138:].decode('hex').split('\x00')[0]
        return get_readable_detail
    except:
        pass