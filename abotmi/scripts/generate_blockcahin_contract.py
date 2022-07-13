#!/home/divya/nfenv/bin/python

# solc - solidity compiler should be installed in the system to create contracts.
# for debian system , replace jessie with vivid for the above installation
import time

import os
import sys
#setting sys path to set the reia.settings
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE","reia.settings")
import django
django.setup()
import subprocess
import requests
from common import constants
from datacenter.models import BlockchainContracts
from pyethmobisir import EthJsonRpc
from blockchain.views import unlock_blockchain_account

def run(path):
    datas = path.split(":")
    file_name = datas[0]
    contract_name = datas[1]

    unlock_blockchain_account("admin")
    print file_name
    print contract_name
    with open(file_name, 'r') as myfile:
        source_code = myfile.read().replace("\n", "")

    c = EthJsonRpc(constants.BLOCKCHAIN_IP,constants.BLOCKCHAIN_PORT,tls=constants.BLOCKCHAIN_TLS)

    solc = subprocess.Popen(["solc","--bin", file_name], stdout=subprocess.PIPE)
    data = solc.communicate()[0].splitlines()
    contract_binary = "0x"+data[3]

    try:
        contract_tx = c.create_contract(c.eth_coinbase(), contract_binary, gas=300000)
    
        print "contract transation"
        print contract_tx

        print "please wait..........getting Contract Address"
        # time.sleep(120)
        while not c.eth_getTransactionReceipt(contract_tx):
            print "waiting for contract address"
            time.sleep(90)
        contract_address = c.get_contract_address(contract_tx)
        print contract_address

        contract_details, created = BlockchainContracts.objects.get_or_create(name=contract_name)
        print contract_details
        print created
        if created:
            contract_details.source_code = source_code
            contract_details.binary_format = contract_binary
            contract_details.contract_transaction_id = contract_tx
            contract_details.contract_address = contract_address
            contract_details.save()
        else:
            print "Contract Name already exists"
    except requests.exceptions.RequestException as e:
        print e
if __name__ == '__main__':
    path = sys.argv[1]
    run(path)
