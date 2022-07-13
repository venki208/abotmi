"""reia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.contrib import admin
from django.conf.urls import include, url, patterns
from django.conf.urls.static import static
from login import views as login_views
from . import views
from home import views as home_views

from my_identity.views import index, guest_details
from my_repute.views import demo_repute
from signup.views import investor_identity

admin.autodiscover()

urlpatterns = [
    url(r'^', include('home.urls', namespace='home')),
    url(r'^home/', home_views.index, name='index'),
    url(r'^login/', include('login.urls'), name='login'),
    url(r'^logout/', login_views.user_logout, name='logout'),
    url(r'^nfadmin/', include('nfadmin.urls', namespace='nfadmin')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/', views.get_protected_media, name='get_protected_media'),
    # URL based redirection need to implement
    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^signup/', include('signup.urls', namespace='signup')),
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^webinar/', include('webinar.urls', namespace='webinar')),
    url(r'^meetup/', include('meetup.urls', namespace='meetup')),
    url(r'^dashboard/', include('dashboard.urls', namespace='dashboard')),
    url(r'^guest/(?P<slug>[A-Za-z0-9_-]+)/$', guest_details, name='guest'),
    url(r'^profile/(?P<slug>[A-Za-z0-9_-]+)/$', index, name='profile'),
    url(r'^investor_profile/(?P<slug>[A-Za-z0-9_-]+)/$',
        investor_identity, name='investor_identity'),
    url(r'^repute_index/(?P<slug>[A-Za-z0-9_-]+)/$', demo_repute, name='demo_repute'),
    url(r'^company/', include('company.urls', namespace='company')),
    url(r'^advisor_check/', include('advisor_check.urls', namespace='advisor_check')),
    url(r'^aadhaar/', include('aadhaar.urls', namespace='aadhaar')),
    url(
        r'^reputation-index/', include(
            'reputation_index.urls', namespace='reputation-index')
    ),
    url(r'^my_identity/', include('my_identity.urls', namespace='my_identity')),
    url(r'^revenue/', include('revenue.urls', namespace='revenue')),
    url(r'^my_growth/', include('my_growth.urls', namespace='my_growth')),
    url(r'^my_repute/', include('my_repute.urls', namespace='my_repute')),
    url(r'^revenue/', include('revenue.urls', namespace='revenue')),
    url(r'^subscribe/', include('subscribe.urls', namespace='subscribe')),
    url(r'^member/', include('member.urls', namespace='member')),
    url(r'^bcadmin/', include('bcadmin.urls', namespace='bcadmin')),
    url(r'^wpb/', include('wpb.urls', namespace='wpb')),

]
