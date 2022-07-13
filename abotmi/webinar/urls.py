from django.conf.urls import url

from . import views
from .views import WebinarMemberRegistration

urlpatterns = [
    url(r'^$',views.dashboard, name='dashboard'),
    url(r'^create_webinar/$',views.create_webinar, name='create_webinar'),
    url(r'^delete_webinar/$',views.delete_webinar, name='delete_webinar'),
    url(r'^check_room_name/$',views.check_room_name, name='check_room_name'),
    url(
        r'^register_member/(?P<room_id>[a-zA-Z0-9]\w{6})/$',
        WebinarMemberRegistration.as_view(),
        name='register_member'
    ),
]
