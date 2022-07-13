'''
Author: Kantanand US
Created: 29-06-2016
'''
from django.db import models
from django.contrib.auth.models import User

# from simple_history.models import HistoricalRecords

class UserLogRecord(models.Model):
    """
    Basic log UserLogRecord describing all user interaction with the UI.
    Will be propagated by a middle ware.
    This will be one BIG DB table!
    """
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True)
    sessionId = models.TextField(blank=True, null=True)

    requestUser = models.ForeignKey(User)
    requestPath  = models.TextField()
    requestQueryString = models.TextField()
    requestVars = models.TextField()
    requestMethod = models.CharField(max_length=4)
    requestSecure = models.BooleanField(default=False)
    requestAjax = models.BooleanField(default=False)
    requestMETA = models.TextField(null=True, blank=True)
    requestAddress = models.GenericIPAddressField()

    viewFunction = models.CharField(max_length=256)
    viewDocString = models.TextField(null=True, blank=True)
    viewArgs = models.TextField()

    responseCode = models.CharField(max_length=3)
    responseContent = models.TextField()
    # Historical data ===========
    # history = HistoricalRecords()

    class Meta:
        app_label = 'datacenter'
        managed = True

    def __unicode__(self):
        return self.requestUser.username