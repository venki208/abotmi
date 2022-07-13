from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^create_session/',views.launch_wpb_app, name='create_session'),
    url(r'^get_all_wpb_course/',views.get_all_wpb_course, name='get_all_wpb_course')
]