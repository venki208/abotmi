#!/usr/bin/env python
import os
import sys
import time
import json
import threading
import pandas as pd

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reia.settings")
    from django.core.management import execute_from_command_line

# from advisor_check.models import AdvisorData
from django.db import connection
# Global Configuration 
location = '/home/kantanand/projects/nfdata/advisorcheck/working/CA_no_mobile_number.xlsx'
df = pd.read_excel(location)
df['address']=df['ADDR_1']+" "+ df['ADDR_2']+" "+df['ADDR_3']+" "+df['ADDR_4']
total_rows = len(df)
print "going to sleep"
time.sleep(2)
print "i am back"
created = 0
duplicate = 0
x = 0

def worker():
    """thread worker function"""
    from advisor_check.models import AdvisorData
    global x, total_rows, df, created, duplicate 
    while not x >= total_rows -1:
        x += 1
        name = None; mobile = None; email = None; secondary_email = None; mobile2 = None
        address = "NILL"; city = "NILL"; state = "NILL"; country = "India"; pincode = "NILL"
        company_name = None; advisor_type = None; reg_id = None; reg_type = None
        valid_from = None; valid_till = None; company_license_code = None
        
        name = df.loc[x].user_name
        if str(df.loc[x].user_name) == "nan":
            name = None
        mobile = df.loc[x].mobile
        # if str(df.loc[x].mobile) == "nan":
        #     mobile = None

        # primary fields check
        if name and mobile:
            email   = str(df.loc[x].email)
            email = "NILL"
            address = df.loc[x].address
            city    = str(df.loc[x].city)
            state = str(df.loc[x].state)
            pincode = str(df.loc[x].pincode)
            advisor_type = str(df.loc[x].advisor_type)
            # advisor_type = "insurance"
            reg_type = "CA"
            reg_id = str(df.loc[x].reg_id)
            if str(df.loc[x].reg_id) == "nan":
                reg_id = None
                # reg_type = str(df.loc[x].reg_type)
                # valid_from = str(df.loc[x].valid_from)
                # valid_till = str(df.loc[x].valid_till)
            extra_field = True
            company_name = str(df.loc[x].company_name)
            # company_license_code = str(df.loc[x].License_Code)
            try:
                advisor, status = AdvisorData.objects.get_or_create(name=name,mobile=mobile)
                print 'Advisor %d %s mobile: %s Created: %s' %(x,name,mobile,status)
                # basic details 
                advisor.name = name
                advisor.email = email
                advisor.mobile = mobile
                advisor.address = address
                advisor.city = city
                advisor.state = state 
                advisor.pincode = pincode
                advisor.country = country
                # advisor company info
                advisor.company = company_name
                # advisor type and registrations
                if not "other" in advisor.advisor_type:
                    advisor.advisor_type = "other"
                if not advisor_type in advisor.advisor_type:
                    advisor.advisor_type += ",%s" %advisor_type
                if reg_id:
                    json_list = []
                    # registration = { "registration_id": reg_id, "registration_type": reg_type, "valid_from": valid_from, "valid_till": valid_from }
                    registration = { "registration_id": reg_id, "registration_type": reg_type }
                    if advisor.registrations:
                        json_list = json.loads(advisor.registrations)
                    json_list.append(registration)
                    json_str = json.dumps(json_list)
                    advisor.registrations = json_str
                if extra_field:
                    extra_field_json_list = []
                    extra_field = { 
                        "file_name": "CA_no_mobile_number"
                        # "company_name": company_name,
                        # "company_license_code": company_license_code
                    }
                    if advisor.extra_fields:
                        extra_field_json_list = json.loads(advisor.extra_fields)
                    extra_field_json_list.append(extra_field)
                    extra_field_json_str = json.dumps(extra_field_json_list)
                    advisor.extra_fields = extra_field_json_str
                advisor.save()
                connection.close()
                if status:
                    created = created + 1
                else:
                    duplicate = duplicate + 1
            except Exception:
                pass
        else:
            pass
            # print str(df.loc[x].to_json())
    return

threads = []
for i in range(0,2):
    t = threading.Thread(target=worker)
    threads.append(t)
    t.start()

# print "Advisor Data is loaded"
# total = created + duplicate
# print "Total advisor : %s" %str(total)
# print "New Advisor: %s" %str(created)
# print "Existing Advisor: %s" %str(duplicate)
exit()