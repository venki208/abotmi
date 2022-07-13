from django.conf.urls import url
from my_growth import views

from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', views.index, name="my_growth"),
    url(r'trending_videos/', views.get_all_videos, name='get_all_videos')
]
