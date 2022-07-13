from django.conf.urls import url
from my_repute import views

urlpatterns = [
    url(r'^$', views.index, name="my_repute"),
    url(r'^my_repute_static/', views.my_repute_static, name='my_repute_static'),
    url(r'^manage_reputation/', views.manage_reputation, name='manage_reputation'),
    url(r'^build_reputation/', views.build_reputation, name='build_reputation'),
    url(r'^share_reputation/', views.share_reputation, name='share_reputation'),
    url(r'^(?P<shared_up_id>[A-Za-z0-9_-]+)/$', views.index, name='my_repute'),
]
