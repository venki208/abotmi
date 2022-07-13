# python lib
import datetime
import hashlib
import json
from random import *
from collections import OrderedDict

# Django lib
from django.http import HttpResponse
from django.shortcuts import render

# Database models
from datacenter.models import (AdvisorSubscriptionPackageOrder, SubscriptionPackageMaster,
    SubscriptionCategoryMaster, FeatureListMaster, FeatureSubscriptionPkgMapping)

# Constants
from subscribe import constants as sub_constant


def get_pkg_list_by_type(type):
    '''
    Getting Package list by type of Subscription
    '''
    response = {}
    sub_cat = SubscriptionCategoryMaster.objects.filter(category_name=type).first()
    if sub_cat:
        sub_pkgs = SubscriptionPackageMaster.objects.filter(subscription_category=sub_cat)
        if sub_pkgs:
            for pkg in sub_pkgs:
                response[pkg.package_type] = json.loads(pkg.feature_data)
            return get_dict_order_as_required(
                    response,
                    cat_type=sub_constant.SUB_CAT_MICRO_LEARNING_PACK
                ), str(sub_cat.id)
    return None, None


def get_dict_order_as_required(pkg_feature_dict, cat_type=None):
    '''
    This function returns array of dict
    order of dict data is  
        ['STANDARD_DATA','DELUXE_DATA','PREMIUM_DATA','EXECUTIVE_DATA','PLATINUM_DATA']
    '''
    result = []
    if pkg_feature_dict:
        pkg_odr_list = sub_constant.PKG_ORDER_LIST
        ftr_odr_list = sub_constant.FEATURE_ORDET_LIST
        if cat_type == sub_constant.SUB_CAT_MICRO_LEARNING_PACK:
            ftr_odr_list = sub_constant.FEATURE_ORDET_LIST_FOR_MICRO_LEARNING
        for pol in pkg_odr_list:
            res = {}
            ress = []
            if pol in pkg_feature_dict.keys():
                if pkg_feature_dict[pol].keys():
                    for ft in ftr_odr_list:
                        if ft.keys():
                            if ft.keys()[0] in pkg_feature_dict[pol].keys():
                                ress.append(pkg_feature_dict[pol][ft.keys()[0]])
                        res[pol] = ress
            result.append(res)
    return result


def generate_unique_reference_key():
    '''
    Generating Unique Reference key
    '''
    unique_key = 'TR'
    crr_year_mon = datetime.datetime.today().strftime('%Y-%m')
    unique_key = unique_key+'-'+crr_year_mon
    random_no = randint(000000,999999)
    unique_key = unique_key+'-'+str(random_no)
    return unique_key
