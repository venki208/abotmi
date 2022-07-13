from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index, name='login'),
    url(r'^social_media_login/', views.social_media_login, name='social_media_login'),
    url(r'^investor_social_media_login/', views.investor_social_media_login, name='investor_social_media_login'),
    url(r'^google_sm/', views.sm_google_login, name='sm_google_login'),
    url(r'^facebook_sm/', views.sm_facebook_login, name='sm_facebook_login'),
    url(r'^linkedin_sm/', views.sm_linkedin_login, name='sm_linkedin_login'),
    url(r'^user_login/', views.ajax_login, name='ajax_login'),
    url(r'^email_signup/', views.email_signup, name='email_signup'),
    url(r'^acknowledgement/', 
        views.activate_member_activation_link, name='activate_member_activation_link'),
    url(r'^validate_otp/', views.validate_otp, name='validate_otp'),
    url(r'^verify_otp_and_login/',
        views.verify_otp_and_login, name='verify_otp_and_login'),
    url(
        r'^get_enrolled_advisors/',
        views.get_advisor_check_total_enrolled_count,
        name="get_enrolled_advisors"
    ),
    url(r'^resend_otp/', views.resend_otps, name='resend_otps'),
    url(r'^set_user_role/', views.set_user_role, name='set_user_role'),
    url(r'^signup_otp/', views.send_signup_otp, name='signup_otp'),
    url(r'^resend_email_mobile_otps/', views.resend_email_mobile_otps, 
        name='resend_email_mobile_otps'),
    # linkedin url's
    url(r'^linkedin/', views.linkedin, name='linkedin'),
    url(r'^linkedin_callback/', views.callback, name='callback'),
]
