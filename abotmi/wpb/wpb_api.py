# python libs
import requests
import logging
import json

# django libs
from django.conf import settings

logger = logging.getLogger(__name__)


def get_wpb_auth_token():
    url = settings.WPB_AUTH_URL
    data = {"username": settings.WPB_USER_ID, "password": settings.WPB_PASSWORD}
    try:
        req = requests.post(url, data=data, timeout=5)
        logger.debug(req.status_code)
        logger.debug(req.text)
        json_res = '%s' % req.text
        token_obj = json.loads(json_res)
        logger.debug('token')
        logger.debug(token_obj)
        token = token_obj['token']
        settings.WPB_TOKEN = token
        return True
    except Timeout as t:
        logger.error(
            logme(
                'Timeout request from wpb request/response is not completed in 5sec',
                request
            )
        )
    except Exception as e:
        logger.error(
            logme(
                'Unable to get Authentication token from wpb. error:{}'.format(e),
                request
            )
        )
        return False
