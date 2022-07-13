# python lib
import hashlib
import logging
# Django Modules
from django.conf import settings
# Database Models
from datacenter.models import AllTransactionsDetails
# Local Imports
from common.views import logme

logger = logging.getLogger(__name__)

class Payment:
    '''
    Description: Common funcitons for EBS payment
    '''
    def online_ebs_payment(self, amount, request, payment_description, 
                            name, return_url,urk_hash):
        '''
        Descrption: Settings values which is required for EBS Payment navigation
        '''
        user = request.user
        user_profile = user.profile
        advisor = user_profile.advisor
        self.secrete_key = settings.EBS_SECRETE_KEY
        self.account_id = settings.EBS_ACCOUNT_ID
        self.address = user_profile.address
        self.amount = amount
        self.channel = settings.EBS_CHANNEL
        self.city = user_profile.city
        self.country = settings.EBS_COUNTRY
        self.currency = settings.EBS_COURENCY
        self.payment_description = payment_description
        self.email = user_profile.email
        self.phone = user_profile.mobile
        self.mode = settings.EBS_MODE
        self.name = name
        self.postal_code = user_profile.pincode
        self.reference_no = urk_hash
        self.return_url = return_url
        self.hash_data = self.secrete_key+'|'+str(self.account_id)+'|'+self.address+'|'\
            +str(self.amount)+'|'+str(self.channel)+'|'+self.city+'|'+self.country+'|'\
            +self.currency+'|'+self.payment_description+'|'+self.email+'|'+self.mode+'|'\
            +self.name+'|'+str(self.phone)+'|'+self.postal_code+'|'+str(self.reference_no)\
            +'|'+self.return_url
        self.secure_hash_key = hashlib.sha512(self.hash_data).hexdigest().upper()
        return self


    def payment_transaction(self, payment_details, request):
        """
        Descrption: Common function of all online transaction which helps to display payment form. User able to give all payment like credit / debit card details
        """
        tr_created = AllTransactionsDetails.objects.create(
            order_id = payment_details['order_id'],
            transaction_value = payment_details['transaction_value'],
            transaction_type = payment_details['transaction_type'],
            status = payment_details['status'],
            service_type = payment_details['service_type'],
            unique_reference_key = payment_details['unique_reference_key'],
        )
        payment_obj = None
        if tr_created:
            amount = payment_details['transaction_value']
            payment_description = payment_details['package_type']
            urk_hash = payment_details['unique_reference_key']
            payment_name = payment_details['category_name']+" - "\
                +payment_details['package_type']+" package Payment"
            return_url = settings.DEFAULT_DOMAIN_URL+\
                '/subscribe/subscribe-package-payment-success/'
            payment_obj = self.online_ebs_payment(
                amount, request, payment_description,
                payment_name, return_url, urk_hash
            )
            logger.info(
                logme('Advisor requested online payment for micro learning ,\
                    Navigated to EBS payment page', request)
            )
            return True, payment_obj
        return False, payment_obj