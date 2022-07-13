import os

from django.db import models
from datacenter.models import UserProfile


class GetAdvice(models.Model):
    '''
    Used to store the Questions which getting advice from members
    question_title --> title of question
    description --> description of question
    document_ids --> store document ids as list
    advisor_email --> to whom u sent query
    user_profile --> asked by whom
    '''
    user_profile = models.ForeignKey(UserProfile, null=True, blank=True)
    question_title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    document_ids = models.TextField(null=True, blank=True)
    advisor_email = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        app_label = 'datacenter'
        managed = True

    def __unicode__(self):
        return self.question_title


class GiveAdvice(models.Model):
    '''
    Used to store the Answers which giving advice by advisors
    queestion --> GetAdvice object
    answer --> Answer of the question
    document_ids --> store document ids as list
    status --> Accepted/Rejected
    remarks --> collect Remark for Answer if member rejects the Answer
    rating --> collect Rating for Answer if member accepts the Answer
    '''
    user_profile = models.ForeignKey(UserProfile, null=True, blank=True)
    question = models.ForeignKey(GetAdvice, null=True, blank=True)
    answer = models.TextField(blank=True, null=True)
    document_ids = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    remarks = models.CharField(max_length=250, blank=True, null=True)
    rating = models.FloatField(default=0)
    activation_key = models.TextField(blank=True,null=True)
    created_date = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        app_label = 'datacenter'
        managed = True

    def __unicode__(self):
        return self.answer
