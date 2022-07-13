'''
author: Madhu C H, BalaKrishnan
created_date: 25-03-2016
'''

import os
import time

from django.db import models

def path_to_upload(instance, filename):
    '''
    This method returns the path to
    store the uploaded file based on its type image or document
    '''
    #if 'Document' in instance.__str__():
    return 'documents/{0}/{1}'.format(instance.opportunity.id, filename)
