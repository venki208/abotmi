from django.conf import settings
from django import forms
from django.contrib.auth.models import check_password

from signup.models import Users
import logging


# logger = logging.getLogger(__name__)
class SettingBackend(object):

    def authenticate(self, username=None, password=None):
        try:
            user = Users.objects.get(username=username)
            #  pwd = check_password(password, user.password)
            if(user.password == password):
                return user
        except Users.DoesNotExist:
            return None

    def get_user(self, username):
        try:
            user = Users.objects.get(username=username)
            if user.is_active:
                return user
            return None
        except Users.DoesNotExist:
            return None