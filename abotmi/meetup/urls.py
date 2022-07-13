from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^list_meetup_events/$',
        views.list_meetup_events, name='list_meetup_events'),
    url(r'^create_meetup_event/$',
        views.create_meetup_event, name='create_meetup_event'),
    url(r'^delete_meetup_event/(?P<event_id>\w+)/$',
        views.delete_meetup_event, name='delete_meetup_event'),
    url(r'^delete_meetup_event_from_post/$',
        views.delete_meetup_event_from_post, name='delete_meetup_event_from_post'),
    url(r'^send_meetup_invitation/$',
        views.send_meetup_invitation, name='send_meetup_invitation'),
    url(r'^list_mail_invitation/$',views.list_mail_invitation, name='list_mail_invitation'),
    url(r'^update_events/$', views.update_events, name='update_events')
]
