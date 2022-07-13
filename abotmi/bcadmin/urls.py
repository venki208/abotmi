from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="bcadmin"),
    url(r'^accounts/', views.get_all_accounts, name="accounts"),
    url(r'^contracts/', views.get_all_contracts, name="contracts"),
]