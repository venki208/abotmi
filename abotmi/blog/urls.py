from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    url(r'^icore/$', views.icore_view, name="icore_view"),
    url(r'^icore/([0-9]+)/post/$', views.icore_post_view, name="icore_post_view"),
    url(r'^icore/add-post/$', views.icore_add_post, name="icore_add_post"),
    url(r'^icore/add-comment/$', views.icore_add_comment, name="icore_add_comment"),
    url(r'^icore/add-rating/$', views.icore_add_rating, name="icore_add_rating"),
    url(r'^icore/search_posts/$', views.icore_search_posts, name="icore_search_posts"),
    url(r'^icore/add_media/$', views.icore_add_media, name="icore_add_media"),
    url(r'^icore/category_posts/',
        views.icore_search_posts_by_category, name="icore_search_posts_by_category"),
    url(r'^icore/author_posts/',
        views.icore_search_posts_by_author, name="icore_search_posts_by_author"),
    url(r'^icore/sm_count/',
        views.social_likes_shares_count, name="social_likes_shares_count")
]
