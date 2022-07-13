'''
Author: Kantanand US.
Created: 17-08-2016
Description: Log all interaction with user to the DB
Reference: https://djangosnippets.org/snippets/2325/
'''
from datetime import datetime
from django.utils import timezone
import simplejson as json

from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import resolve

from datacenter.models import UserLogRecord
from django.conf import settings

import logging
logger = logging.getLogger(__name__)

class LogAllMiddleware(object):

    def process_request(self,request):
        """
        process: REQUEST
        """
        # Only log requests of authinticate users
        try:
            if not request.user.is_authenticated():
                return None
        except AttributeError:
            return None

        # Skip favicon requests cause I do not care about them
        if request.path == "/favicon.ico":
            return None

        # -------------------------------------------------
        # Collect request IP and request Query String
        # -------------------------------------------------
        req_var_json = None
        match = resolve(request.path)
        ip_address = request.META.get('REMOTE_ADDR')
        # request Query 
        if request.method == 'GET':
            req_var_json = json.dumps(request.GET.__dict__)
        if request.method == 'POST':
            req_var_json = json.dumps(request.POST.__dict__)
        # request IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[-1].strip()
        else:
            ip_address = request.META.get('REMOTE_ADDR')
        # -------------------------------------------------
        logger.info("process: REQUEST user : " + str(request.user) + " path :" + str(request.path))
        
        newUserLogRecord = UserLogRecord(
            sessionId = request.session.session_key,
            requestUser = request.user,
            requestPath = request.path,
            requestMethod = request.method,
            requestAddress = ip_address,
            requestMETA = request.META['HTTP_USER_AGENT'],
            created_at = timezone.now(),
        )

        # enable if you want to record following :
        # newUserLogRecord.requestMETA = request.META.__str__() 
        newUserLogRecord.requestQueryString = request.META["QUERY_STRING"]
        newUserLogRecord.requestVars = req_var_json
        newUserLogRecord.requestSecure = request.is_secure()
        newUserLogRecord.requestAjax = request.is_ajax()
        newUserLogRecord.viewFunction = match._func_path
        newUserLogRecord.save()

        return None

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        process: VIEW
        """
        try:
            if not request.user.is_authenticated():
                return None
        except AttributeError:
            return None

        # Fix the issue with the authrization request
        try:
            # -------------------------------------------------
            # Collect request IP and request Query String
            # -------------------------------------------------
            req_var_json = None
            match = resolve(request.path)
            ip_address = request.META.get('REMOTE_ADDR')
            # request Query 
            if request.method == 'GET':
                req_var_json = json.dumps(request.GET.__dict__)
            if request.method == 'POST':
                req_var_json = json.dumps(request.POST.__dict__)
            # request IP
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip_address = x_forwarded_for.split(',')[-1].strip()
            else:
                ip_address = request.META.get('REMOTE_ADDR')
            # -------------------------------------------------
            logger.info("process: VIEW user : " + str(request.user) + " path :" + str(request.path))

            theUserLogRecord = UserLogRecord.objects.filter(
                sessionId = request.session.session_key,
                requestUser = request.user,
                requestPath = request.path,
                requestMethod = request.method,
                requestAddress = ip_address,
                requestMETA = request.META['HTTP_USER_AGENT'],
            ).order_by('-created_at').first()

            # Enable if you want to record following :
            # theUserLogRecord.requestMETA = request.META.__str__() 
            # theUserLogRecord.viewDocString = view_func.func_doc
            # theUserLogRecord.viewArgs = json.dumps(view_kwargs)
            # theUserLogRecord.requestQueryString = request.META["QUERY_STRING"]
            # theUserLogRecord.requestVars = req_var_json
            # theUserLogRecord.requestSecure = request.is_secure()
            # theUserLogRecord.requestAjax = request.is_ajax()
            theUserLogRecord.viewFunction = match._func_path
            theUserLogRecord.save()

        except  ObjectDoesNotExist:
            pass

        return None


    def process_response(self, request, response):
        """
        process: RESPONSE
        """
        # Only log authorized requests
        try:
            if not request.user.is_authenticated():
                return response
        except AttributeError:
            return response

        # Skip favicon requests cause I do not care about them
        if request.path =="/favicon.ico":
            return response

        # Only log autherized requests
        if not request.user.is_authenticated():
            return response

        try:
            # -------------------------------------------------
            # Collect request IP and request Query String
            # -------------------------------------------------
            req_var_json = None
            match = resolve(request.path)
            ip_address = request.META.get('REMOTE_ADDR')
            # request Query 
            if request.method == 'GET':
                req_var_json = json.dumps(request.GET.__dict__)
            if request.method == 'POST':
                req_var_json = json.dumps(request.POST.__dict__)
            # request IP
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip_address = x_forwarded_for.split(',')[-1].strip()
            else:
                ip_address = request.META.get('REMOTE_ADDR')
            # -------------------------------------------------
            if getattr(response, 'status_code', None):
                logger.info("process: RESPONSE user : " + str(request.user) + " path :" + str(request.path) + "response: " + str(response.status_code))

            if request.user.is_authenticated():
                # there can be more than one record so we are taking LIFO
                theUserLogRecord = None
                theUserLogRecord = UserLogRecord.objects.filter(
                    sessionId = request.session.session_key,
                    requestUser = request.user,
                    requestPath = request.path,
                    requestMethod = request.method,
                    requestAddress = ip_address,
                    requestMETA = request.META['HTTP_USER_AGENT'],
                ).order_by('-created_at').first()

                if not theUserLogRecord:
                    # if record does not exists create 
                    theUserLogRecord = UserLogRecord.objects.create(
                        sessionId = request.session.session_key,
                        requestUser = request.user,
                        requestPath = request.path,
                        requestMethod = request.method,
                        requestAddress = ip_address,
                        requestMETA = request.META['HTTP_USER_AGENT'],
                    )

                if theUserLogRecord:
                    # Enable if you want to record following :
                    # theUserLogRecord.requestMETA = request.META.__str__() 
                    theUserLogRecord.requestQueryString = request.META["QUERY_STRING"]
                    theUserLogRecord.requestVars = req_var_json
                    theUserLogRecord.requestSecure = request.is_secure()
                    theUserLogRecord.requestAjax = request.is_ajax()
                    theUserLogRecord.viewFunction = match._func_path
                    theUserLogRecord.responseCode = response.status_code

                    # Decide wether we want to log the a full html response
                    # as this will probabaley will take a LOT of space.
                    # In my case most of the replies I want to catch happen
                    # to be plain text ajax replies
                    if settings.LOGALL_LOG_HTML_RESPONSE:
                        # IF set to true then log the respoce regardless
                        theUserLogRecord.responseContent = response.content
                    else:
                        theUserLogRecord.responseContent = "Not required"

                    theUserLogRecord.save()
                else:
                    return response
            else:
                return response

        except  ObjectDoesNotExist:
            pass

        return response