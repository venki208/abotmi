from django.conf.urls import include, url
from . import views
from subscribe.views import IdentityPack

urlpatterns = [
    url(r'^$', views.index, name="subscribe"),
    url(r'^activate-package/', views.activate_package),
    url(r'^subscribe-package-order/', 
        views.subscribe_package_order, name='subscribe_package_order'),
    url(r'^subscribe-package-payment-success/', 
        views.subscribe_package_payment_success,
        name='subscribe_package_payment_success'
    ),
    url(r'^load-identity-pack/', IdentityPack.as_view()),
    url(r'^profile-viewed-details/',
        views.profile_viewed_details, name='profile_viewed_details'),
    url(r'^get-member-details/',
        views.get_member_details_by_id, name='get_member_details_by_id'),
    url(r'^payment-summary-details/',
        views.payment_summary_details, name='payment_summary_details'),
]
