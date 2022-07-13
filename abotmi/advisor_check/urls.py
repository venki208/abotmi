from django.conf.urls import include, url
from advisor_check import views, api_views
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^search/', views.search, name='search'),
    url(r'^check_advisor/', views.check_advisor, name='check_advisor'),
    url(r'^create_advisor/', views.create_advisor, name='create_advisor'),
    url(r'^get_advisor_information/', views.get_advisor_information, 
        name='get_advisor_information'),
    url(r'^get_advisor_card/', views.get_advisor_card, name='get_advisor_card'),
    url(r'^save_advisor_card/', views.save_advisor_card, name='save_advisor_card'),
    url(r'^send_otp_to_match_card/', views.send_otp_to_match_card, 
        name='send_otp_to_match_card'),
    url(r'^validate_otp/', views.validate_otp, name="validate_otp"),
    url(r'^get_certified_card/', views.get_certified_card, name='get_certified_card'),
    url(r'^get_advisor_navigation_url/',
        views.get_advisor_navigation_url, name='get_advisor_navigation_url'),
    url(r'^profile/([0-9]+)/([A-Za-z]+)/$', views.profile, name="profile"),
    url(r'^connect_advisor/', views.connect_advisor, name='connect_advisor'),   
    # api_urls
    url(r'^search_advisors/', api_views.search_advisors, name='search_advisors'),
    url(r'^advisor_connect/', api_views.advisor_connect, name='advisor_connect'),
    url(r'^get_calendly_link/', views.get_calendly_link, name='get_calendly_link'),
    
]
