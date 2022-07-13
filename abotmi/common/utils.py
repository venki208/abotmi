# python lib
import hashlib
import json
import random
import requests
import string

# Django Modules
from django.conf import settings

# Database Models
from datacenter.models import Sequence

# Third Party modules
from bs4 import BeautifulSoup


def generate_key():
    '''
    Generating Activation key
    '''
    activation_key = hashlib.sha1(
        str(random.getrandbits(random.randrange(999)))
    ).hexdigest()[:17] + hashlib.sha1(
        str(random.getrandbits(333))
    ).hexdigest()[:13]

    return activation_key


def send_sms_alert(mobile_number, message_template, sms_sender_id=settings.SMS_SENDER_ID):
    '''
    Function for sending SMS
    required parameters:
        mobile_number --> accepts only number
        message_template --> need to pass sms text
    '''
    url = settings.SMS_URL
    post_data = {
        'username': settings.SMS_USERNAME,
        'pass': settings.SMS_PASSWORD,
        'senderid': sms_sender_id,
        'message': message_template,
        'dest_mobileno': mobile_number,
        'response': 'Y'
    }
    response = requests.post(url, data=post_data)
    return response


def calculate_certificate_value(amount, selected_years):
    '''
    Description: Calculating the CRISIL certificate value according to year
    '''
    final_amount = amount*(int(selected_years))
    return final_amount


def calculate_discount_amount(amount, discount_amount_percentage):
    '''
    Description: Caculating the amount using discount percentage
    '''
    discount_amount = (float(amount)/float(100))*(100-discount_amount_percentage)
    return discount_amount


def calculate_tax_amount(amount, tax_percentage):
    '''
    Description: caculating the tax with percentage
    '''
    amount = (float(amount)/float(100))*(tax_percentage)
    return amount


def calculate_final_amount_with_discount_and_tax_amount(actaul_certificate_cost,
                                                        selected_years, discount, tax):
    '''
    caculating the final amount of crisil after applying tax, discount
    '''
    certificate_value = calculate_certificate_value(
        actaul_certificate_cost, selected_years)
    amount_after_discount = calculate_discount_amount(certificate_value, discount)
    tax_amount = calculate_tax_amount(amount_after_discount, tax)
    final_cost_of_certificate = amount_after_discount+tax_amount
    return final_cost_of_certificate


def sequence_number(typ, pfix):
    '''
    Getting sequence number from current sequence
    '''
    seq, created = Sequence.objects.get_or_create(
        sequence_type=typ,
        prefix=pfix,
        digit_len=5
    )
    num = seq.last_sequence
    num = num + 1
    seq.last_sequence = num
    seq.save()
    num = "%0*d" % (int(seq.digit_len), num)
    num = pfix + num
    return num


def clean_text(html_text):
    '''
    used to remove html css scripts from given string and return clean text
    '''
    soup = BeautifulSoup(html_text, "html5lib")
    for s in soup(['script', 'style']):
        s.decompose()
    return ' '.join(soup.stripped_strings)


class JSONEncoder(json.JSONEncoder):
    '''
        JSONEncoder: encoding json
    '''
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        else:
            return None
        return json.JSONEncoder.default(self, o)


class UtilFunctions():

    @classmethod
    def generate_randome_password(
            self, size=6, chars=string.ascii_uppercase + string.digits):
        '''
        Generate randome alphanumeric password
        '''
        return ''.join(random.choice(chars) for x in range(size))
