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
from datacenter.models import RevenueType, Sequence

print "------Started to creating--------"
rev_nm = [
		{'id':'RVN00001', 'name':'GET_CERTIFIED_REVENUE_FEE'},
		{'id':'RVN00002', 'name':'CERTIFIED_PROVIDER_FEE'},
		{'id':'RVN00003', 'name':'GET_QUALIFIED_REVENUE_FEE'},
		{'id':'RVN00004', 'name':'QUALIFIED_PROVIDER_FEE'},
		{'id':'RVN00005', 'name':'GET_CONNECTED_REVENUE_FEE'},
		{'id':'RVN00006', 'name':'LISTING_REVENUE_FEE'},
		{'id':'RVN00007', 'name':'FACILITATION_REVENUE_FEE'},
		{'id':'RVN00008', 'name':'PRODUCT_EDUCTION_REVENUE_FEE'},
		{'id':'RVN00009', 'name':'PRODUCT_EDUCTION_PROVIDER_FEE'},
		{'id':'RVN00010', 'name':'TRANSACTION_MANAGEMENT_FEE'},
		{'id':'RVN00011', 'name':'ADV_FEE'},
		{'id':'RVN00012', 'name':'ADV_REF_ADV_FEE'},
		{'id':'RVN00013', 'name':'SEQ_ADV_REF_ADV_FEE_A'},
		{'id':'RVN00014', 'name':'SEQ_ADV_REF_ADV_FEE_B'},
		{'id':'RVN00015', 'name':'GRND_ADV_REF_ADV_FEE'},
		{'id':'RVN00016', 'name':'GRND_SEQ_ADV_REF_ADV_FEE_A'},
		{'id':'RVN00017', 'name':'GRND_SEQ_ADV_REF_ADV_FEE_B'},
		{'id':'RVN00018', 'name':'BY_CLI_ADV_FEE'},
		{'id':'RVN00019', 'name':'CLI_REF_CLI_FEE'},
		{'id':'RVN00020', 'name':'CLI_REF_CLI_FEE_NO_ADV_FEE'},
		{'id':'RVN00021', 'name':'UPWRDZ_ADV_FEE'}
	]
for data in rev_nm:
	print data
	obj = RevenueType.objects.get_or_create(revenue_code = data['id'], revenue_name = data['name'], is_active=1)
Sequence.objects.get_or_create(last_sequence="18", sequence_type = "Revenue", prefix="RVN", digit_len=5)

