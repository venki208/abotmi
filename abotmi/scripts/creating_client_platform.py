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
from datacenter.models import ClientPlatform, Sequence

print "------Started to creating--------"
ClientPlatform.objects.get_or_create(platform_name="UPWRDZ", platform_code = "PLT00001", platform_email="admin@upwrdz.com")
ClientPlatform.objects.get_or_create(platform_name="ADVISOR_GROUP", platform_code = "PLT00002", platform_email="ADVISOR_GROUP")
ClientPlatform.objects.get_or_create(platform_name="CLIENT_GROUP", platform_code = "PLT00003", platform_email="CLIENT_GROUP")
Sequence.objects.get_or_create(last_sequence="3", sequence_type = "Platform", prefix="PLT", digit_len=5)

