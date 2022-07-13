# python lib
import json
import logging

# Django imports
from django.apps import apps
from django.db.models import F

# Database Models
from advisor_check.models import IrdaData, SebiData, AmfiData, AdvisorData

# Constants
from common.constants import REGION_IN, ADVISOR_CHECK_APP

logger = logging.getLogger(__name__)

class AdvisorCheckCommonFunctions:
    """docstring forAdvisorCheckCommonFunctions."""
    def __init__(self):
        logger.info('object created for advisor check common functions')

    def get_regulatory_status(self, object_dict=None):
        if object_dict:
            kwargs = {}
            adv_chk_column_name = object_dict.get('column_name', None)
            reg_no = object_dict.get('reg_no', None)
            if adv_chk_column_name and reg_no:
                if adv_chk_column_name == 'arn':
                    table_name = AmfiData
                    kwargs['arn'] = reg_no
                elif adv_chk_column_name == 'irda_urn':
                    table_name = IrdaData
                    kwargs['irda_urn'] = reg_no
                elif adv_chk_column_name == 'reg_no':
                    table_name = SebiData
                    kwargs['reg_no'] = reg_no
                adv_chk_obj = table_name.objects.filter(**kwargs)
                if adv_chk_obj:
                    return True
                else:
                    return False
            else:
                return None
        else:
            return None

    def check_matching_card(self, object_dict=None):
        '''
        Description: Cheking the Advisor is peresent in Advisor check according to priority
            priotity:
                1. Primary Email
                2. Secondary Email
                3. Primary Mobile Number
                4. Secondary Mobile Number
        '''
        if object_dict:
            pri_email_id = object_dict.get('email', None)
            pri_mobile_no = object_dict.get('primary_mobile', None)
            first_name = object_dict.get('first_name', None)
            table_name = object_dict.get('type_of_advisor', None)
            adv_chk_obj = None
            final_adv_obj = None
            add_priority_params = []
            priority_params = [
                ('email', pri_email_id),
            ]
            if pri_mobile_no:
                priority_params += [
                    ('mobile__contains', pri_mobile_no),
                ]
            if table_name == AdvisorData:
                add_priority_params = [
                    ('secondary_email', pri_email_id),
                ]
                if pri_mobile_no:
                    add_priority_params += [
                        ('mobile2__contains', pri_mobile_no)
                    ]
            priority_params = priority_params + add_priority_params

            for col, params in priority_params:
                kwargs = {}
                kwargs[col] = params
                adv_obj = table_name.objects.filter(**kwargs).values(
                    'id', 'email', 'mobile', 'advisor_id'
                )
                if adv_obj:
                    adv_chk_obj = adv_obj
                    break
            
            if adv_chk_obj:
                obj_count = adv_chk_obj.count()
                if obj_count == 1:
                    final_adv_obj = adv_chk_obj.first()
                else:
                    if pri_mobile_no:
                        mobile_obj = adv_chk_obj.filter(mobile__contains=pri_mobile_no)
                        if mobile_obj.count() == 1:
                            final_adv_obj = mobile_obj.first()
                        elif mobile_obj.count() > 1:
                            name_obj = mobile_obj.filter(
                                name__icontains=first_name)
                            if name_obj:
                                final_adv_obj = name_obj.first()
                            else:
                                final_adv_obj = mobile_obj.first()
                        else:
                            final_adv_obj = mobile_obj.first()
                    else:
                        final_adv_obj = adv_chk_obj.first()
            return final_adv_obj
        else:
            return False

    @staticmethod
    def get_table_name(cat_type=None):
        '''
        Returning Advisor check Model class
        cat_type -> catogery type(ex: SEBI, CA, etc...)
        '''
        cat_type = cat_type.upper()
        t_name = 'AdvisorData'
        if not cat_type: t_name = 'AdvisorData'
        elif cat_type == 'SEBI': t_name = 'SebiData'
        elif cat_type == 'IRDA': t_name = 'IrdaData'
        elif cat_type == 'AMFI': t_name = 'AmfiData'
        elif cat_type == 'BSE': t_name = 'BseData'
        elif cat_type == 'CA': t_name = 'CaData'
        elif cat_type == 'US': t_name = 'UnitedStatesAdvisors'
        elif cat_type == 'SG': t_name = 'SingaporeAdvisors'
        elif cat_type == 'MY': t_name = 'MalaysianAdvisors'
        else: t_name = 'AdvisorData'
        ad_chk_model = apps.get_model(ADVISOR_CHECK_APP, t_name)
        return ad_chk_model

    @staticmethod
    def get_profile_view_fields(model_name=None):
        '''
        Returing Fields names of the table for getting the data
        model_name -> Model Class Name in string format
        '''
        default_col = ['name', 'email', 'mobile', 'city']
        rename_col = {}  # Renaming columns into common json
        if model_name == 'AdvisorData':
            model_col = []
        elif model_name == 'SebiData':
            model_col = ['reg_no']
        elif model_name == 'IrdaData':
            model_col = ['reg_no']
            rename_col['reg_no'] = F('license_no')
        elif model_name == 'AmfiData':
            model_col = ['reg_no']
            rename_col['reg_no'] = F('arn')
        elif model_name == 'BseData':
            model_col = ['reg_no']
            rename_col['reg_no'] = F('bse_clearing_number')
        elif model_name == 'CaData':
            model_col = ['reg_no']
            rename_col['reg_no'] = F('reg_id')
        elif model_name == 'UnitedStatesAdvisors':
            model_col = ['reg_no']
            rename_col['reg_no'] = F('lic_id')
        elif model_name == 'SingaporeAdvisors':
            model_col = ['reg_no']
            rename_col['reg_no'] = F('regulatory_no')
        elif model_name == 'MalaysianAdvisors':
            model_col = ['reg_no']
            rename_col['reg_no'] = F('licence_number')
        query_col = default_col + model_col
        return query_col, rename_col
