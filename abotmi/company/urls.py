# from django.conf.urls import include, url
from django.contrib import admin
from . import views
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^$', views.index, name='company'),
    url(r'^add_affiliate/', views.add_affiliate, name='add_affiliate'),
    url(r'^my_company_track/', views.my_company_track, name='my_company_track'),
    url(r'^employees_details/', views.employees_details, name='employees_details'),
    url(r'^save_add_affiliate_form/', views.save_add_affiliate_form,
        name='save_add_affiliate_form'),
    url(r'^fetch_advisor_details/', views.fetch_advisor_details, 
        name = 'fetch_advisor_details'),
    url(r'^update_company_details/', views.update_company_details, 
        name='update_company_details'),
    url(r'^check_email_exist_or_not/', views.check_email_exist_or_not, 
        name='check_email_exist_or_not'),
    url(r'^update_affiliate_company_status/', views.update_affiliate_company_status, 
        name='update_affiliate_company_status'),
    url(r'^why_we_are_asking/', views.why_we_are_asking, name='why_we_are_asking'),
    url(r'^confidence_assurance/', views.confidence_assurance, 
        name='confidence_assurance'),
    url(r'^change_password/', views.change_password, name='change_password'),
    url(r'^get_in_touch/', views.get_in_touch, name='get_in_touch'),
    url(r'^get_not_approved_advsors_list/', views.get_not_approved_advsors_list, 
        name="get_not_approved_advsors_list"),
    url(r'^get_approved_advisor_list/', views.get_approved_advisor_list, 
        name='get_approved_advisor_list'),
    url(r'^get_disown_advisors_list/', views.get_disown_advisors_list, 
        name='get_disown_advisors_list'),
    url(r'^upload_advisors_data/', views.upload_advisors_data, 
        name='upload_advisors_data'),
]
