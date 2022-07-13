'''
author: Kantanand US
created date: 06-03-2017
'''

from django.conf.urls import url
from aadhaar import views

urlpatterns = [
    url(r'create_aadhaar_form_data/', views.create_aadhaar_form_data, name="create_aadhaar_form_data"),
    url(r'^success', views.success, name='success'),
    url(r'^failed', views.failed, name='failed'),
    url(r'^member_success', views.member_success, name='member_success'),
    url(r'^member_failed', views.member_failed, name='member_failed'),
    url(r'^check_aadhaar_present/', views.check_aadhaar_present, name='check_aadhaar_present'),
    url(r'^create_client_in_uplyf/', views.create_client_in_uplyf, name='create_client_in_uplyf'),
    url(r'^delete_session_aadhaar_values/', views.delete_session_aadhaar_values, name='delete_session_aadhaar_values'),
    url(r'^upwrdz_aadhaar_check/', views.upwrdz_aadhaar_check, name='upwrdz_aadhaar_check'),
]
