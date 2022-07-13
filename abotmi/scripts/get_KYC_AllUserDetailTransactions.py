import os
import sys
#setting sys path to set the reia.settings
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE","reia.settings")
import django
django.setup()
from blockchain.views import unlock_blockchain_account,get_userdetails_by_transactionid
from datacenter.models import BlockchainAccounts


def run():
    unlock_blockchain_account("admin")

    print "output filename - all_user_details_output.txt"

    outputfile = open('all_user_details_output.txt','w')
    outputfile.write("AdvisorId,TransactionId,UserDetails\n")

    print "get details - started"
    db_data = BlockchainAccounts.objects.exclude(accounts_creation_transaction_id__isnull=True).exclude(accounts_creation_transaction_id__exact='')
    for data in db_data:
        id = data.user_profile.id
        transid = data.accounts_creation_transaction_id
        result = get_userdetails_by_transactionid(transid)
        outputfile.write("%s,%s,%s\n" % (id,transid,result))
   
    outputfile.close()
    print "get details - finished"

if __name__ == '__main__':
    run()