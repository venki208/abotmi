from django.conf.urls import url
from reputation_index import views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^advisor-scoring-fb/', views.advisor_scoring_fb_api, name='advisor-scoring-fb'),
    url(r'^advisor-scoring-linkedin/', 
        views.advisor_scoring_linkedin_api, name='advisor-scoring-linkedin'),
    url(r'^check_social_email/', 
        views.check_social_email, name='check_social_email'),
    url(r'^get_reputation_index_data/', 
        views.get_reputation_index_data, name='get_reputation_index_data'),
    url(r'^advisor_reputation_for_hyperlocal/', 
        views.advisor_reputation_for_hyperlocal, 
        name='advisor_reputation_for_hyperlocal'
    ),
    url(r'^create_insurance_meta_if_not_existed/', 
        views.create_insurance_meta_if_not_existed,
        name='create_insurance_meta_if_not_existed'
    ),
    url(r'^get_geo_pincode/', views.get_geo_pincode, name='get_geo_pincode'),
    url(r'^get_advisors_rank/', views.get_advisors_rank, name='get_advisors_rank'),
    url(r'^call_native/', views.call_native, name='call_native'),
    url(r'^update_pincode/', views.update_pincode, name='update_pincode'),
    url(r'^edit_pincode/',
        TemplateView.as_view(
            template_name="my_repute/edit_pincode.html"
        )
    ),

]
