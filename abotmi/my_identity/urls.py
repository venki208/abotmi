from django.conf.urls import url
from my_identity import views

from django.views.generic import TemplateView
from my_identity.views import ShareProfileByEmail, BatchCode, FinancialInstruments

urlpatterns = [
    url(r'^$', views.index, name="my_identity"),
    url(
        r'^edit_languages/',
        TemplateView.as_view(
            template_name="my_identity/edit_languages.html"
        )
    ),
    url(
        r'^edit_my_belief/',
        TemplateView.as_view(
            template_name="my_identity/edit_my_belief.html"
        )
    ),
    url(
        r'^edit_my_promise/',
        TemplateView.as_view(
            template_name="my_identity/edit_my_promise.html"
        )
    ),

    # Education URLS
    url(r'^save_education/', views.save_education, name="save_education"),

    # Sales Accomplishment URLS
    url(
        r'^edit_sales_accomplishments/',
        TemplateView.as_view(
            template_name="my_identity/edit_sales_accomplishments.html"
        )
    ),
    url(r'^add_sales_acomplishments/',
        views.save_sales_acomplishments, name="save_sales_acomplishments"),

    # Self Declaration URLS
    url(
        r'^edit_self_declaration/',
        TemplateView.as_view(
            template_name="my_identity/edit_self_declaration.html"
        )
    ),
    url(
        r'^add_self_declaration/',
        views.save_self_declaration,
        name="save_self_declaration"
    ),

    # Contact Details URLS
    url(
        r'^edit_contact_details/',
        TemplateView.as_view(
            template_name="my_identity/edit_contact_details.html"
        )
    ),
    url(
        r'^update_contact_details/',
        views.update_contact_details,
        name='update_contact_details'
    ),

    # Skills URLS
    url(
        r'^edit_skills/',
        TemplateView.as_view(
            template_name="my_identity/edit_skills.html"
        )
    ),
    url(r'^add_skills/', views.save_advisor_skills, name="save_advisor_skills"),

    url(
        r'^edit_or_view_image/',
        TemplateView.as_view(
            template_name="my_identity/edit_or_view_picture.html"
        )
    ),

    # Regulatory URLS
    url(r'^edit_regulatory_registration/',
        views.edit_regulatory_registration, name='edit_regulatory_registration'),
    url(r'^save_regulatory_registration/',
        views.save_regulatory_registration, name='save_regulatory_registration'),

    # Guest Details URLS
    url(r'^guest_details', views.guest_details, name='guest_details'),
    url(r'^save_guest_details/', views.save_guest_details, name='save_guest_details'),

    # Peer and Client Connections URLS
    url(
        r'^edit_peer_connection/',
        TemplateView.as_view(
            template_name="my_identity/edit_peer_connection.html"
        )
    ),
    url(
        r'^edit_client_connection/',
        TemplateView.as_view(
            template_name="my_identity/edit_client_connection.html"
        )
    ),
    url(
        r'^save_peer_connections/', views.save_total_advisors_connected_count,
        name='save_total_advisors_connected_count'),
    url(r'^save_client_connections/',
        views.save_total_clients_served_count, name='save_peer_connection_count'),
    url(r'^share_profile_by_email/',
        ShareProfileByEmail.as_view(), name='share_profile_by_email'),

    # Batch code URLS
    url(r'^batch_code/', BatchCode.as_view(), name='batch-code'),
    url(r'^check_batch_availability/', views.check_batch_availability,
        name='check_batch_availability'),

    # Advisory Specilization
    url(r'^get_advisory_specilization/', views.get_advisory_specilization,
        name='get_advisory_specilization'),
    url(
        r'^profile_attachment/',
        TemplateView.as_view(
            template_name="my_identity/profile_attachment.html"
        )
    ),
    url(r'^advisors_archive/', views.advisors_archive,
        name='advisors_archive'),
    url(r'^attach_advisors_link/', views.attach_advisors_link,
        name='attach_advisors_link'),
    url(r'^follower_profile/', views.follower_profile,
        name='follower_profile'),

    # Experience
    url(
        r'^experience/',
        FinancialInstruments.as_view(),
        name='edit_experience'
    ),
    url(
        r'^save_experience/',
        views.save_experience,
        name='save_experience'
    ),

    # Certification
    url(r'^save_certification/', views.save_certification, name='save_certification')
]
