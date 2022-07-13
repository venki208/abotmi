import urllib
import requests
import json
import logging

from django.conf import settings
logger = logging.getLogger(__name__)


class LinkiedinOAuth:
    '''
    Linkedin OAuth Functionality to get the email, profile
    '''

    __client_id = settings.LINKEDIN_CLIENT_ID
    __secrete_id = settings.LINKEDIN_SECRET_ID
    __state = settings.LINKEDIN_STATE
    __scope = 'r_liteprofile,r_emailaddress'
    __auth_url = 'https://www.linkedin.com/oauth/v2/authorization'
    __token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
    __get_email_url = 'https://api.linkedin.com/v2/emailAddress?q=members&projection=\
        (elements*(handle~))'
    __get_profile_url = 'https://api.linkedin.com/v2/me?projection=(id,firstName,\
        lastName,profilePicture(displayImage~:playableStreams))'
    __redirect_uri = settings.LINKEDIN_REDIRECT_URI
    __response_type = 'code'
    __grant_type = 'authorization_code'
    __access_token = None

    def __init__(self, *args, **kwargs):
        self.__access_token = None

    def get_autherization_url(self, *args, **kwargs):
        '''
        Returns Linkedin Access token url to redirect into Linkedin site
        '''
        url = self.__auth_url + '?'
        data = {
            'response_type': self.__response_type,
            'client_id': self.__client_id,
            'redirect_uri': self.__redirect_uri,
            'state': self.__state,
            'scope': self.__scope,
        }
        get_params = urllib.urlencode(data)
        logger.debug('Authorization url Created to navigate to linkedin page')
        return url + get_params

    def get_auth_token(self, request, *args, **kwargs):
        '''
        Gets the authorization/JWT token from linkedin
        '''
        code = request.GET.get('code', None)
        state = request.GET.get('state', None)
        # Getting auth token from linkedin
        linkedin = requests.post(
            self.__token_url,
            data={
                'grant_type': self.__grant_type,
                'code': code,
                'redirect_uri': self.__redirect_uri,
                'client_id': self.__client_id,
                'client_secret': self.__secrete_id
            }
        )
        if linkedin.status_code == 200:
            ln_res = json.loads(linkedin.content)
            self.__access_token = ln_res['access_token']
            logger.info('Succussfully got Authorization toke from linkedin')
        else:
            logger.error(
                'Unable to get Authorization token. error- {}'.format(linkedin.content))
        return self.__access_token

    def get_email(self, *args, **kwargs):
        '''
        Gets the Email from linkedin by using authorization/JWT token
        '''
        email = ''
        headers = {'Authorization': 'Bearer %s' % self.__access_token}
        email_res = requests.get(
            self.__get_email_url,
            headers=headers
        )
        if email_res.status_code == 200:
            email_res = json.loads(email_res.content)
            email = email_res['elements'][0]['handle~']['emailAddress']
            logger.info('Got Email from Linkedin')
        else:
            logger.error(
                'Unable to get email from linkedin api. error- {}'.format(
                    email_res.content))
        return email

    def get_profile(self, *args, **kwrgs):
        '''
        Gets the profile data from linkedin by using authorization/JWT token
        '''
        headers = {'Authorization': 'Bearer %s' % self.__access_token}
        profile_res = requests.get(
            self.__get_profile_url,
            headers=headers
        )
        if profile_res.status_code == 200:
            profile_res = json.loads(profile_res.content)
            first_name = profile_res['firstName']['localized']['en_US']
            last_name = profile_res['lastName']['localized']['en_US']
            logger.info('Got Profile details from Linkedin')
            return {
                'first_name': first_name,
                'last_name': last_name
            }
        else:
            logger.error(
                'Unable to get the profile data from Linkedin api. error- {}'.format(
                    profile_res.content))
            return {
                'first_name': '',
                'last_name': ''
            }
