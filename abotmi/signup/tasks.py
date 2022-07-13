'''
This program calls the signzy API for verification
of user uploaded documents

author: Madhu CH
created date: 16-07-2016
'''
import os
import json
import requests
from django.conf import settings
from common import constants
from datacenter.models import Signzy, UserProfile
from reia.celery import app as celery_app

from PIL import Image
from StringIO import StringIO

'''
We need the below function to get the access token in v2
currently due to lack of documentation we are falling back
to beta v1 of signzy
'''

# def get_session_access_token():
#     url = constants.SIGNZY_AUTHENTICATION_URL
#     data = {
#         'username': settings.SIGNZY_USERNAME,
#         'password': settings.SIGNZY_PASSWORD
#     }
#     headers = {
#         'accept-language': "en-US,en;q=0.8",
#         'content-type': "application/json",
#         'accept': "*/*"
#     }
#     response = requests.request(
#         "POST",
#         url,
#         data=json.dumps(data),
#         headers=headers,
#     )
#     response = json.loads(response.text)
#     return response.get('id')


def upload_file_signzy(filename, content_type):
    with open(filename, 'rb') as _file:
        upload_response = requests.post(
            constants.SIGNZY_UPLOAD_URL,
            files={
                'file': (
                    filename,
                    _file,
                    content_type
                )
            }
        )
    return upload_response


@celery_app.task(name="verify_documents", ignore_result=True)
def verify_documents(
    image_file,
    document_type,
    filename,
    content_type,
    user_profile_id
):
    '''
    This is a task that will verify user uploaded
    documents ex: PAN and Aadhar
    TODO: verify ssl certificate
    '''
    # access_token = get_session_access_token()
    user_profile = UserProfile.objects.get(id=user_profile_id)
    querystring = {"type": document_type}
    headers = {
        'content-type': 'application/json',
        'authorization': settings.SIGNZY_API_KEY
    }
    image_url = image_file['documents']
    image_byte_code = requests.get(image_url)
    image_file = Image.open(StringIO(image_byte_code.content))
    image_file.save(filename)
    upload_response = upload_file_signzy(filename, content_type)
    os.remove(filename)
    if upload_response.status_code == 200:
        signzy, created = Signzy.objects.get_or_create(
            user_profile=user_profile,
            documents_type=document_type
        )
        if document_type == 'pan':
            signzy.urls = json.loads(
                upload_response.text)['file']['directURL']
            signzy.save()
        elif document_type == 'aadhaar' and created:
            signzy.urls = json.loads(
                upload_response.text)['file']['directURL'] + ', '
            signzy.save()
            return False
        else:
            signzy.urls += json.loads(
                upload_response.text)['file']['directURL']
            signzy.save()
        data = {"files": signzy.urls.split(',')}
        extraction_response = requests.post(
            constants.SIGNZY_EXTRACTION_URL,
            data=json.dumps(data),
            headers=headers,
            params=querystring,
        )
        if extraction_response.status_code == 200:
            signzy.extracted_data = extraction_response.text
            signzy.save()
            data = json.loads(extraction_response.text)['result']
            verification_response = requests.post(
                constants.SIGNZY_VERIFICATION_URL,
                data=json.dumps(data),
                headers=headers,
                params=querystring,
            )
            signzy.verification_data = verification_response.text
            signzy.save()
            return json.loads(
                verification_response.text
            )['result']['verified']
        return json.loads(
            extraction_response.text
        )['error']
    return json.loads(
        upload_response.text
    )['error']
