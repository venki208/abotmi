from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^$', views.index, name='dashboard'),
    url(r'^view_member/', views.view_member, name='view_member'),
    url(r'^view_members/', views.view_member, name='view_members'),
    url(r'^add_member/', views.add_member, name='add_member'),
    url(r'^save_new_members/', views.save_new_member, name='save_new_members'),
    url(r'^refer_advisor/', views.refer_advisor, name='refer_advisor'),
    url(r'^save_refer_advisor/', views.save_refer_advisor, name='save_refer_advisor'),
    url(r'^invite_advisor_to_rate/',
        views.invite_advisor_to_rate, name='invite_advisor_to_rate'),
    url(r'^advisor_rating_list',
        views.advisor_rating_list, name='advisor_rating_list'),
    url(r'^rate_advisor/', views.rate_advisor, name='rate_advisor'),
    url(r'^accept_or_decline_booking/',
        views.accept_or_decline_booking, name='accept_or_decline_booking'),
    url(r'^valid_email/', views.valid_email, name='valid_email'),
    # Rating or Ranking
    url(r'^view_ranking_or_rating/', views.view_ranking_or_rating,
        name='view_ranking_or_rating'),
    url(r'^client_enquiry/', views.view_client_enquiry, name='client_enquiry'),
    url(r'^valid_email_for_rating/', views.valid_email_for_rating,
        name='valid_email_for_rating'),
    # CRISIL Application URLS
    url(r'^load_apply_now_crisil_modal/',
        TemplateView.as_view(template_name="dashboard/crisil_apply_now.html")),
    url(r'^appling_crisil/', views.appling_crisil, name='appling_crisil'),
    url(r'^view_loop/', views.view_loop, name='view_loop'),
    url(r'^submit_crisil_form/', views.submit_crisil_form, name='submit_crisil_form'),
    url(r'^check_promocode/', views.check_promocode, name='check_promocode'),
    url(r'^crisil_terms_and_conditions/',
       TemplateView.as_view(template_name="dashboard/crisil_terms_and_conditions.html"),
        name='crisil_terms_and_conditions'
    ),
    url(r'^renewal_submit_crisil_form/',
        views.renewal_submit_crisil_form, name='renewal_submit_crisil_form'),
    url(r'^check_address_proof/', views.check_address_proof, name='check_address_proof'),
    url(r'^crisil_online_payment/',
        views.submit_crisil_online_payment_form, name='submit_online_payment_form'),
    url(r'^crisil_payment_success/', views.crisil_payment_success, name='crisil_payment_success'),
    url(r'^crisil_faq/',
        TemplateView.as_view(template_name="dashboard/crisil_faq_modal.html"),
        name='crisil_faq_modal'),
    # End CRISIL URLS
    # Grouping URLS
    url(r'^add_group_name/', views.add_group_name, name='add_group_name'),
    url(r'^group_list_view/', views.group_list_view, name='group_list_view'),
    url(r'^group_members/', views.group_members, name='group_members'),
    url(r'^list_members_excluded/', views.list_members_excluded,
        name='list_members_excluded'),
    url(r'^onchange_add_member_in_group/', views.onchange_add_member_in_group,
        name='onchange_add_member_in_group'),
    url(r'^add_member_in_group/', views.add_member_in_group, name='add_member_in_group'),
    url(r'^update_group/', views.update_group, name="update_group"),
    url(r'^delete_group/', views.delete_group, name='delete_group'),
    url(r'^create_new_group/', views.create_new_group, name='create_new_group'),
    url(r'^load_send_group_email_modal/', views.load_send_group_email_modal,
        name='load_send_group_email_modal'),
    # End Grouping URLS
    # Member URLS
    url(r'^advisor_member_maping/', views.advisor_member_maping,
        name="advisor_member_maping"),
    # End Member URLS
    # Advisor UPLYF Transaction URLS
    url(r'^manage-uplyf-transaction/', views.manage_uplyf_transaction,
        name='manage_uplyf_transaction'),
    url(r'list_enquiried_clients/', views.list_enquiried_clients,
        name='list_enquiried_clients'),
    url(r'upload_transaction_documents/', views.upload_transaction_documents,
        name='upload_transaction_documents'),
    # End Advisor UPLYF Transaction URLS
    # It is a temperory url
    url(r'^project_detail/', views.project_details, name="project_detail"),
    # UPLYF URL
    url(r'^create_users_session', views.launch_uplyf, name='create_users_session'),
    url(r'^financial_tools/', views.financial_tools, name='financial_tools'),
    # Video URLS
    url(r'^video_publish_modal/',
       TemplateView.as_view(template_name="dashboard/video_publish_modal.html"),
        name='video_publish_modal'
    ),
    url(r'^video_shoot_request/', views.video_shoot_request, name='video_shoot_request'),
    url(r'^advisor_video_upload/', views.advisor_video_upload,
        name='advisor_video_upload'),
    # End Video URLS
    url(r'^check_ebs_mandatory_details/', views.check_ebs_mandatory_details,
        name='check_ebs_mandatory_details'),
    # micro learning FAQ modal
    url(r'^micro_learning_faq_modal/',
       TemplateView.as_view(template_name="dashboard/micro_learning_faq_modal.html"),
        name='micro_learning_faq_modal'
    ),
    url(r'^give_advice_how_it_works/',
       TemplateView.as_view(template_name="home/give_advice_how_it_works.html"),
        name='give_advice_how_it_works'
    ),
    url(r'^db_street_works/',
       TemplateView.as_view(template_name="home/db_street_works.html"),
        name='db_street_works'
    ),
    url(r'^wpb_works/',
       TemplateView.as_view(template_name="home/wpb_how_it_works.html"),
        name='wpb_works'
    ),
    url(r'^micro_learning_packages_model/', views.micro_learning_packages_model,
        name='micro_learning_packages_model'),
    url(r'^get_video_request_modal/', views.get_video_request_modal,
        name='get_video_request_modal'),
    # END Micro learning video URLS
    # video subscripton URLS
    url(r'^check_advisor_subscribed_to_create_video/',
        views.check_advisor_subscribed_to_create_video,
        name='check_advisor_subscribed_to_create_video'
    ),
    # END subscripton URLS
    url(r'^follow_advisors/',
        views.FollowingActivities.as_view({'post': 'follow_advisors'})),
    url(r'^follower_advisor_mapping/',
        views.FollowingActivities.as_view({'get': 'follower_advisor_mapping'})),
    url(r'^unfollow_advisors/',
        views.FollowingActivities.as_view({'post': 'unfollow_advisors'})),
    url(r'^donot_follow_advisors/',
        views.FollowingActivities.as_view({'post': 'donot_follow_advisors'})),
    url(r'^view_followers/',
        views.FollowingActivities.as_view({'post': 'view_followers'})),
    url(r'^view_followees/',
        views.FollowingActivities.as_view({'post': 'view_followees'})),
    url(r'list_profile_viewed/', views.list_profile_viewed,
        name='list_profile_viewed'),
    url(r'list_connect_profile/', views.list_connect_profile,
        name='list_connect_profile'),
    # Save Calendly link
    url(r'^save_calendly_link/', views.save_calendly_link, name='save_calendly_link'),
    url(r'^calendly-modal/',
        TemplateView.as_view(template_name="dashboard/calendly_how_it_works.html")
        ),
]
