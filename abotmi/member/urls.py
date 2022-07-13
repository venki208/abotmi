from django.conf.urls import url
from django.views.generic import TemplateView

from member import views
from member.views import MemberIndexClass

urlpatterns = [
    url(r'^$', MemberIndexClass.as_view()),
    url(r'^advice_form/', views.GetFormAdviceClass.as_view(), name='advice_form'),
    url(r'^get_advice/', views.get_advice, name='get_advice'),
    # Give advice urls
    url(r'^get_questions_list/', views.get_questions_list, name='get_questions_list'),
    url(r'^read_more_answer/', views.read_more_answer, name='read_more_answer'),
    url(r'^answers_archive/', views.answers_archive, name='answers_archive'),
    url(r'^get_member_response/', views.get_member_response, name='get_member_response'),
    url(r'^get_member_rating/', views.get_member_rating, name='get_member_rating'),
    url(r'^connect_advisor/', views.connect_advisor, name='connect_advisor'),
    url(r'^get_profile_details/', views.get_profile_details, name='get_profile_details'),
    url(r'^view_all_answers/', views.GiveAdviceClass.as_view(
        {'post': 'view_all_answers'})),
    url(r'^submit_advice', views.GiveAdviceClass.as_view({'post': 'submit_advice'})),
    url(r'^download_docs', views.GiveAdviceClass.as_view({'post': 'download_docs'})),
    url(r'^download_advisors_docs',
        views.GiveAdviceClass.as_view({'post': 'download_advisors_docs'})),
]
