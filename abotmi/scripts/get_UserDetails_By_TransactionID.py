import os
import sys
#setting sys path to set the reia.settings
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE","reia.settings")
import django
django.setup()
from blockchain.views import unlock_blockchain_account,get_userdetails_by_transactionid

def run(path):
    file_name = path

    unlock_blockchain_account("admin")
    print "input filename"
    print file_name

    print "output filename"
    print "outputfile.txt"

    outputfile = open('outputfile.txt','w')

    with open(file_name, 'r') as inputfile:
        for transid in inputfile:
            #if not splitted new line is added to the value , hence throws exception
            transid = transid.split('\n')[0]
            result = get_userdetails_by_transactionid(transid)
            outputfile.write("%s\n" % result)
   
    outputfile.close()

if __name__ == '__main__':
    path = sys.argv[1]
    run(path)
