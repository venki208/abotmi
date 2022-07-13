from django.conf.urls import include, url
from . import views
urlpatterns = [
    url(r'^$', views.index, name="revenue_view"),
    url(r'^create-revenue-type/', views.create_revenue_type),
    url(r'^create-client-platform/', views.create_client_platform),
    url(r'^create-client/', views.create_client),
    url(r'^map-revenuetype-platform/', views.map_revenuetype_platform),
    url(r'^make-transaction/', views.revenue_transactions),
    url(r'^revenue-details/', views.total_revenue),
    url(r'^get-advisor-transactions/', views.get_advisor_transactions),
    url(r'^get-all-revenue-type/', views.get_all_revenue_type),
    url(r'^get-all-platform/', views.get_all_platform),
    url(r'^get-all-client/', views.get_all_client),
    url(r'^get-certified-revenue/', views.get_certified_revenue),
    url(r'^get-qualified-revenue/', views.get_qualified_revenue),
    url(r'^get-connected-revenue-fee/', views.get_connected_revenue_fee),
    url(r'^get-listing-revenue-fee/', views.get_listing_revenue_fee),
    url(r'^get-facilitation-revenue-fee/', views.get_facilitation_revenue_fee),
    url(r'^get-product-education-fee/', views.get_product_education_fee),
    url(r'^get-advisor-transactions/', views.get_advisor_transactions),
    url(r'^add-client/', views.add_client),
    url(r'^list-client/', views.list_client),    
    url(r'^open-transaction/', views.open_transaction),
    url(r'^create-transaction/', views.create_transaction),    
    url(r'^revenue-statement-by-email/', views.revenue_statement_by_email),    
    
]