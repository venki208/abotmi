from django.conf.urls import url
from django.views.generic import TemplateView
from login import views as login_views
from home import views

urlpatterns = [
    url(r'^$', login_views.index, name='login'),
    url(r'^logout_user/', views.user_logout, name='logout_user'),
    url(r'^change_password/', views.change_password, name='change_password'),
    url(r'^code_of_coduct/', views.code_of_coduct, name='code_of_coduct'),
    url(r'^get_in_touch/', views.get_in_touch, name='get_in_touch'),
    url(r'^contact_us_reia/', views.contact_us_reia, name='contact_us_reia'),
    url(r'^privacy_and_policy/', views.privacy_and_policy, name='privacy_and_policy'),
    # url(r'^learn_more_resources/', views.learn_more_resources,
    #     name='learn_more_resources'),
    url(r'^advisor_loop_termsandconditions/', views.advisor_loop_termsandconditions,
        name='advisor_loop_termsandconditions'),
    url(r'^kyc_registration_terms_conditions/', views.kyc_registration_terms_conditions,
        name='kyc_registration_terms_conditions'),
    url(r'^home-page/', views.home, name='home'),
    url(r'^apply_crisil_verification/', views.apply_crisil_verification,
        name='apply_crisil_verification'),
    url(r'^crisil_verified_advisor/', views.crisil_verified_advisor,
        name='crisil_verified_advisor'),
    url(r'^notification_services_status/', views.notification_services_status,
        name='notification_services_status'),
    url(r'^signup_terms_and_conditions/', views.signup_terms_and_conditions,
        name='signup_terms_and_conditions'),
    url(r'^server_health/', views.server_health, name='server_health'),
    url(r'^user_service_status_update/', views.user_service_status_update,
        name='user_service_status_update'),
    url(r'^digital-identity-modal/',
        TemplateView.as_view(template_name="home/digital_identity_modal.html")
        ),
    url(r'^micro-learning-modal/',
        TemplateView.as_view(template_name="home/micro_learning_modal.html")
        ),
    url(r'^reputation-index-modal/',
        TemplateView.as_view(template_name="home/reputation_index_modal.html")
        ),
    url(r'^load-reputation-video-modal/',
        TemplateView.as_view(template_name="home/video.html")
        ),
    url(r'^summary_of_abotmi_privacy_policy/',  
        views.summary_of_abotmi_privacy_policy, name='summary_of_abotmi_privacy_policy'),
    url(r'^get_advice_page/', views.get_advice_page, name='get_advice_page'),
    # commented temporarly we use future purpose
    # url(r'^build_page/', views.build_page, name='build_page'),
    url(r'^opportunities_page/', views.opportunities_page, name='opportunities_page'),
    url(r'^summary_of_terms_condtions/',
        views.summary_of_terms_condtions, name='summary_of_terms_condtions'),
    url(r'^advisor_page/', views.advisor_page, name='advisor_page'),
    url(r'^cookie_policy/', views.cookie_policy, name='cookie_policy'),
    url(r'^copyright_policy/', views.copyright_policy, name='copyright_policy'),
    url(r'^ethical_commitment_page/', 
        views.ethical_commitment_page, name='ethical_commitment_page'),
    url(r'^purpose_page/', views.purpose_page, name='purpose_page'),
    url(r'^people_page/', views.people_page, name='people_page'),
    url(r'^partners_page/', views.partners_page, name='partners_page'),
    url(r'^protection_page/', views.protection_page, name='protection_page'),
    url(r'^refer_advice_page/', views.refer_advice_page, name='refer_advice_page'),
    url(r'^rate_advice_page/', views.rate_advice_page, name='rate_advice_page'),
    url(r'^abotmi_faq/', views.abotmi_faq, name='abotmi_faq'), 
    url(r'^how_it_work/', views.how_it_work, name='how_it_work'),
    url(r'^refer_friend/', views.refer_friend, name='refer_friend'),
    url(r'^about_us/', views.about_us, name='about_us'),
    url(r'^why_us/', views.why_us, name='why_us'),
    url(r'^advisors/', views.advisors, name='advisors'),
    url(r'^investors/', views.investors, name='investors'),

    # Notification URLS
    url(r'^notification/', views.list_notifications, name='notification'),
    url(r'^get_notification/', views.list_notifications, name='get_notification'),
    url(r'get_notification_count/', views.get_notification_count,
        name='get_notification_count'),
    url(
        r'update_notification_status/',
        views.update_notification_status,
        name='update_notification_status'
    ),
]
