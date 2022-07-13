import datetime

from django import template
from django.conf import settings
register = template.Library()


@register.filter
def keyvalue(dict, key):
    '''
        This filter is convert string to json object
        Usage django template : {{dictionary|keyvalue:key_variable}}
    '''
    return dict[key]


@register.filter
def split_path(value, key):
    """
        Splitted and Returns the value turned into a list.
    """
    return value.split(key)


@register.filter()
def format_date(value, date_format=None):
    date_obj = datetime.datetime.strptime(value, date_format)
    return date_obj
