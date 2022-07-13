# python libs
import json
import logging
import os
import requests
import time
import threading
from time import gmtime, strftime

# Django Modules
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.forms import ModelForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.utils.crypto import get_random_string

# Database Models
from datacenter.models import Advisor, UserProfile, SocialMediaLikesShareCount

# Local Imports
from common.views import (
    social_media_like_count_bg_process, social_media_like_count,
    top_three_post, logme
)
from common.constants import SSL_VERIFY
from login.decorators import active_and_certified_advisor, active_and_registered_advisor

# Wordpress
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.base import *
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, comments, posts

logger = logging.getLogger(__name__)


def create_word_press_user(request):
    '''
    1. Create user in icore wordpress using api
    2. If Created, it will return json with user details
    3. Get word press user id and return
    4. If user existing, it will return already exist message
    5. Then, request one more API (our API in wordpress) to get word press user id
        and return.
    '''
    user_profile_obj = user.get_profile()  # Returns UserProfile Table object
    USERNAME = settings.ICORE_ADMIN
    PASSWORD = settings.ICORE_ADMIN_PWD
    url = settings.ICORE_API_URL+'/users/'
    headers = {'Content-Type': 'application/json'}
    WP_PASSWORD = get_random_string(length=8)
    post_data = {
        "username": user_profile_obj.email,
        "name": user_profile_obj.first_name,
        "password": WP_PASSWORD,
        "email": user_profile_obj.email,
        "role": "author"
    }
    req = requests.post(
        url,
        auth=(USERNAME, PASSWORD),
        headers=headers,
        data=post_data,
        verify=SSL_VERIFY
    )
    json_res = req.content.encode('UTF-8')
    token_obj = json.loads(json_res)
    if token_obj:
        if len(token_obj) == 1:
            message = token_obj[0]['message']
            url_wp_id = settings.ICORE_API_URL+'/users/username/'+request.user.email
            request_wp_id = requests.get(url_wp_id, headers, verify=SSL_VERIFY)
            response_wp_id = request_wp_id.content.encode('UTF-8')
            json_wp_id = json.loads(response_wp_id)
            # Already existing user id in icore
            wordpress_user_id = json_wp_id['id']
        else:
            # New User id in icore
            wordpress_user_id = token_obj['ID']
    logger.info(
        logme('created icore user successfully (wordpress)', request)
    )
    return wordpress_user_id


def icore_view(request):
    '''
    Loading Icore Posts with Pagination and Navigating to icoreview html
    '''
    title = 'Icore View'
    USERNAME = settings.ICORE_ADMIN
    PASSWORD = settings.ICORE_ADMIN_PWD
    # ================Fetching recent posts==================
    url_all = settings.ICORE_API_URL+'/posts/'
    headers_all = {'Content-Type': 'application/json'}
    req_all = requests.get(
        url_all,
        auth=(USERNAME, PASSWORD),
        headers=headers_all,
        verify=SSL_VERIFY
    )
    json_res_all = req_all.content.encode('UTF-8')
    token_obj_all = json.loads(json_res_all)

    # ============Fetching all posts with pagination==========
    url = settings.ICORE_API_URL+'/posts?filter[posts_per_page]=-1'
    headers = {'Content-Type': 'application/json'}
    req = requests.get(
        url,
        auth=(USERNAME, PASSWORD),
        headers=headers,
        verify=SSL_VERIFY
    )
    json_res = req.content.encode('UTF-8')
    token_obj = json.loads(json_res)
    paginator = Paginator(token_obj, 4)
    page = request.GET.get('page')

    # ============ Fetching top Three post ====================
    t = threading.Thread(target=social_media_like_count_bg_process, args=(), kwargs={})
    t.setDaemon(True)
    t.start()

    count = []
    if token_obj:
        post_data = token_obj
        count = top_three_post(post_data)

    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)

    PRODUCT_NAME = settings.PRODUCT_NAME
    icore_all = token_obj_all
    icore = contacts
    logger.info(
        logme('listed all icore blogs', request)
    )
    return render(request, 'blog/icoreview.html', locals())


def icore_post_view(request, pk):
    '''
    Getting Individual Icore Post and Navigating to icorepost html
    '''
    context = RequestContext(request)
    USERNAME = settings.ICORE_ADMIN
    PASSWORD = settings.ICORE_ADMIN_PWD
    url = settings.ICORE_API_URL+'/posts/'+pk
    headers = {'Content-Type': 'application/json'}
    req = requests.get(
        url,
        auth=(USERNAME, PASSWORD),
        headers=headers,
        verify=SSL_VERIFY
    )
    json_res = req.content.encode('UTF-8')
    token_obj = json.loads(json_res)
    social_media_like_count(token_obj['link'], "fb")
    # social_media_like_count(token_obj['link'], "ln")
    # ----------------------------------
    # Getting Comments for specific posts
    # -----------------------------------
    url_comment = settings.ICORE_API_URL+'/posts/'+pk+'/comments/'
    headers_comment = {'Content-Type': 'application/json'}
    req_comment = requests.get(
        url_comment,
        auth=(USERNAME, PASSWORD),
        headers=headers_comment,
        verify=SSL_VERIFY
    )
    json_res_comment = req_comment.content.encode('UTF-8')
    token_obj_comment = json.loads(json_res_comment)
    # ------------------------------------
    # Getting Ratings for specific posts
    # ------------------------------------
    url_rating = settings.ICORE_API_URL+'/posts/'+pk+'/rating/'
    headers_rating = {'Content-Type': 'application/json'}
    req_rating = requests.get(
        url_rating,
        auth=(USERNAME, PASSWORD),
        headers=headers_rating, verify=SSL_VERIFY)
    json_res_rating = req_rating.content.encode('UTF-8')
    token_obj_rating = json.loads(json_res_rating)
    # Converting Rating response data into json format
    data = {}
    data_rating = {}
    if token_obj_rating:
        data_rating['votes'] = token_obj_rating[2]['meta_value']
        data_rating['ratings'] = token_obj_rating[3]['meta_value']
        data_rating['last_update_date'] = token_obj_rating[5]['meta_value']
    # ------------------------------------
    # Fetching all posts with pagination
    # ------------------------------------
    url_all = settings.ICORE_API_URL+'/posts?filter[posts_per_page]=-1'
    headers_all = {'Content-Type': 'application/json'}
    req_all = requests.get(
        url_all,
        auth=(USERNAME, PASSWORD),
        headers=headers_all,
        verify=SSL_VERIFY
    )
    json_res_all = req_all.content.encode('UTF-8')
    token_obj_all = json.loads(json_res_all)
    # ============ Fetching top Three post ====================
    count = []
    if token_obj_all:
        post_data = token_obj_all
        count = top_three_post(post_data)

    profile_pic = ""
    if request.user.profile.picture:
        profile_pic = request.user.profile.picture.url

    title = 'Icore Post - ' + token_obj.get('title', '')

    context_dict = {
        'PRODUCT_NAME': settings.PRODUCT_NAME,
        'icore': token_obj,
        'icore_comment': token_obj_comment,
        'icore_object_main': token_obj_all,
        'rating': data_rating,
        'count': count,
        'profile_pic': profile_pic,
        'title': title
    }
    logger.info(
        logme('opened id=%s icore post' % (str(pk)), request)
    )
    return render_to_response('blog/icorepost.html', context_dict, context)


@active_and_certified_advisor
def icore_add_post(request):
    '''
    Checking Advisor is certified advisor or not for adding icore post
    GET:
        -> Getting Catrgories
        -> Navigating to icore_addpost html
    POST:
        -> Adding/Saving the Icore post in wordpress
    '''
    context = RequestContext(request)
    if request.method == 'GET':
        USERNAME = settings.ICORE_ADMIN
        PASSWORD = settings.ICORE_ADMIN_PWD
        url = settings.ICORE_API_URL+'/taxonomies/category/terms/'
        headers = {'Content-Type': 'application/json'}
        req = requests.get(
            url,
            auth=(USERNAME, PASSWORD),
            headers=headers,
            verify=SSL_VERIFY
        )
        json_res = req.content.encode('UTF-8')
        token_obj = json.loads(json_res)
        PRODUCT_NAME = settings.PRODUCT_NAME
        category_list = token_obj
        logger.info(
            logme('opened icore add post template', request)
        )
        return render(request, 'blog/icore_addpost.html', locals())

    if request.method == 'POST':
        advisor_details = Advisor.objects.get(user_profile=request.user.profile)
        wordpress_user = advisor_details.wordpress_user_id
        # creating tag list
        list_tag = []
        if request.POST['add_tag']:
            str_tag = request.POST['add_tag']
            list_tag = str_tag.split(',')
        else:
            list_tag = []
        # creating category list
        list_category = []
        str_category = request.POST.get('id_total_category_selected', None)
        if str_category:
            list_category = str_category.split(',')
        USERNAME = settings.ICORE_ADMIN
        PASSWORD = settings.ICORE_ADMIN_PWD
        url = settings.ICORE_API_URL+'/posts/'
        headers = {'Content-Type': 'application/json'}
        wp = Client(settings.ICORE_XMLRPC, USERNAME, PASSWORD)
        post = WordPressPost()
        post.title = request.POST['title']
        post.content = request.POST['content_raw']
        post.post_status = 'publish'
        post.comment_status = 'open'
        post.user = wordpress_user
        post.terms_names = {'post_tag': list_tag, 'category': list_category}
        post.thumbnail = request.POST['featured_image']
        post.id = wp.call(posts.NewPost(post))
        logger.info(
            logme('submitted icore post id =%s successfully' % (str(post.id)), request)
        )
        return redirect('/blog/icore/')


def icore_add_comment(request):
    '''
    Adding Comments to Icore post
    '''
    if request.method == 'POST':
        USERNAME = settings.ICORE_ADMIN
        PASSWORD = settings.ICORE_ADMIN_PWD
        post_id = request.POST['post_id']
        url = settings.ICORE_API_URL+'/posts/'+post_id+'/comment/'
        headers = {'Content-Type': 'application/json'}
        comment_data = {}
        comment_data['post_id'] = post_id
        comment_data['comment_author_name'] = request.user.profile.first_name
        comment_data['comment_author_email'] = request.user.profile.email
        comment_data['comment_content'] = request.POST['comment']
        comment_data['user_id'] = request.user.profile.advisor.wordpress_user_id
        comment_json_data = json.dumps(comment_data)
        req = requests.post(
            url,
            auth=(USERNAME, PASSWORD),
            headers=headers,
            data=comment_json_data,
            verify=SSL_VERIFY
        )
        logger.info(
            logme('commented icore post id=%s' % (str(post_id)), request)
        )
        return HttpResponse('comment')


def icore_add_rating(request):
    '''
    Adding Rating to Icore post
    '''
    if request.method == 'POST':
        post_id = request.POST['post_id']
        user = request.user.id
        advisor_details = Advisor.objects.get(user_profile=request.user.profile)
        wordpress_user = advisor_details.wordpress_user_id
        rating_sum = request.POST['star_sum']
        rating_latest_updated_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        USERNAME = settings.ICORE_ADMIN
        PASSWORD = settings.ICORE_ADMIN_PWD
        url = settings.ICORE_API_URL+'/posts/'+post_id+'/rating/'
        headers = {'Content-Type': 'application/json'}
        rating_data = {}
        rating_data['data'] = [
                {"id": post_id, "latest": rating_latest_updated_time},
                [
                    {"meta_key": "stars-rating_sum", "meta_value": rating_sum},
                    {"meta_key": "stars-rating_max", "meta_value": "5"},
                    {"meta_key": "stars-rating_votes", "meta_value": "1"},
                    {"meta_key": "stars-rating_rating", "meta_value": rating_sum},
                    {"meta_key": "stars-rating_distribution", "meta_value": ""},
                    {"meta_key": "stars-rating_latest",
                        "meta_value": rating_latest_updated_time}
                ],
                {"user_id": wordpress_user, "logged": rating_latest_updated_time},
                {"meta_value": rating_sum}
            ]
        rating_json_data = json.dumps(rating_data)
        req = requests.post(
            url,
            auth=(USERNAME, PASSWORD),
            headers=headers,
            data=rating_json_data,
            verify=SSL_VERIFY
        )
        logger.info(
            logme('rated icore post id=%s' % (str(post_id)), request)
        )
        return HttpResponse('success')


@login_required
def icore_search_posts(request):
    '''
    Searching the Icore post
    '''
    context = RequestContext(request)
    USERNAME = settings.ICORE_ADMIN
    PASSWORD = settings.ICORE_ADMIN_PWD
    # ================Fetching recent for posts============
    url_all = settings.ICORE_API_URL+'/posts/'
    headers_all = {'Content-Type': 'application/json'}
    req_all = requests.get(
        url_all,
        auth=(USERNAME, PASSWORD),
        headers=headers_all,
        verify=SSL_VERIFY
    )
    json_res_all = req_all.content.encode('UTF-8')
    token_obj_all = json.loads(json_res_all)
    # ================Search result posts==================
    if request.method == 'POST':
        search = request.POST.get('search_name', False)
        request.session['search'] = search
    if request.method == 'GET':
        search = request.session['search']
    url = settings.ICORE_API_URL+'/posts/?filter[s]='+search
    headers = {'Content-Type': 'application/json'}
    req = requests.get(
        url,
        auth=(USERNAME, PASSWORD),
        headers=headers,
        verify=SSL_VERIFY
    )
    json_res = req.content.encode('UTF-8')
    token_obj = json.loads(json_res)
    context_dict = {'search': token_obj}
    paginator = Paginator(token_obj, 4)
    page = request.GET.get('page')

    # =================Fetching all posts =================
    url_all = settings.ICORE_API_URL+'/posts?filter[posts_per_page]=-1'
    headers_all = {'Content-Type': 'application/json'}
    req_all = requests.get(
        url_all,
        auth=(USERNAME, PASSWORD),
        headers=headers_all,
        verify=SSL_VERIFY
    )
    json_res_all = req_all.content.encode('UTF-8')
    token_obj_count = json.loads(json_res_all)

    # ============ Fetching top Three post ====================
    count = []
    if token_obj_count:
        post_data = token_obj_count
        count = top_three_post(post_data)

    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    context_dict = {
        'PRODUCT_NAME': settings.PRODUCT_NAME,
        'icore_all': token_obj_all,
        'icore': contacts,
        'count': count,
    }
    logger.info(
        logme('listed all icore post with keyword=%s' % (str(search)), request)
    )
    return render_to_response('blog/icoreview.html', context_dict, context)


@login_required
def icore_search_posts_by_category(request):
    '''
    Searching Icore post by Catagory
    '''
    context = RequestContext(request)
    if request.method == 'GET':
        USERNAME = settings.ICORE_ADMIN
        PASSWORD = settings.ICORE_ADMIN_PWD
        # ================Fetching recent for posts==================
        url_all = settings.ICORE_API_URL+'/posts/'
        headers_all = {'Content-Type': 'application/json'}
        req_all = requests.get(
            url_all,
            auth=(USERNAME, PASSWORD),
            headers=headers_all,
            verify=SSL_VERIFY
        )
        json_res_all = req_all.content.encode('UTF-8')
        token_obj_all = json.loads(json_res_all)
        # ================Search result posts==================
        category = request.GET.get('cat', False)
        if category:
            request.session['category'] = category
        else:
            category = request.session['category']
        url = settings.ICORE_API_URL+'/posts/?filter[category_name]='+category
        headers = {'Content-Type': 'application/json'}
        req = requests.get(
            url,
            auth=(USERNAME, PASSWORD),
            headers=headers,
            verify=SSL_VERIFY
        )
        json_res = req.content.encode('UTF-8')
        token_obj = json.loads(json_res)
        context_dict = {'search': token_obj}
        paginator = Paginator(token_obj, 4)
        page = request.GET.get('page')

        # =================Fetching all posts =================
        url_all = settings.ICORE_API_URL+'/posts?filter[posts_per_page]=-1'
        headers_all = {'Content-Type': 'application/json'}
        req_all = requests.get(
            url_all,
            auth=(USERNAME, PASSWORD),
            headers=headers_all,
            verify=SSL_VERIFY
        )
        json_res_all = req_all.content.encode('UTF-8')
        token_obj_count = json.loads(json_res_all)

        # ============ Fetching top Three post ====================
        count = []
        if token_obj_count:
            post_data = token_obj_count
            count = top_three_post(post_data)

        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        context_dict = {
            'PRODUCT_NAME': settings.PRODUCT_NAME,
            'icore_all': token_obj_all,
            'icore': contacts,
            'count': count,
        }
        logger.info(
            logme('listed all icore post based on category=%s' % (str(category)), request)
        )
        return render_to_response('blog/icoreview.html', context_dict, context)


def icore_add_media(request):
    '''
    Adding Media to Icore post
    GET:
        -> Navigating to icore_addpost html
    POST:
        -> Uploading Image into Wordpress and getting the attachment url
    '''
    context = RequestContext(request)
    if request.method == 'GET':
        context_dict = {'PRODUCT_NAME': settings.PRODUCT_NAME}
        return render_to_response('blog/icore_addpost.html', context_dict, context)
    if request.method == 'POST':
        USERNAME = settings.ICORE_ADMIN
        PASSWORD = settings.ICORE_ADMIN_PWD
        wp = Client(settings.ICORE_XMLRPC, USERNAME, PASSWORD)
        filename = request.FILES['up']
        data = {
            'name': filename.name,
            'type':  filename.content_type,
        }
        data1 = None
        for chunk in filename.chunks():
            data1 = xmlrpc_client.Binary(chunk)
        data['bits'] = data1
        response = wp.call(media.UploadFile(data))
        attachment_id = response['attachment_id']
        attachment_url = response['url']
        context_dict = attachment_id+"::"+attachment_url
        logger.info(
            logme('added media = %s to icore' % (filename.name), request)
        )
        return HttpResponse(context_dict)


@login_required
def icore_search_posts_by_author(request):
    '''
    Searching Icore post by Author
    '''
    context = RequestContext(request)
    if request.method == 'GET':
        USERNAME = settings.ICORE_ADMIN
        PASSWORD = settings.ICORE_ADMIN_PWD
        # ================Fetching recent for posts==================
        url_all = settings.ICORE_API_URL+'/posts/'
        headers_all = {'Content-Type': 'application/json'}
        req_all = requests.get(
            url_all,
            auth=(USERNAME, PASSWORD),
            headers=headers_all,
            verify=SSL_VERIFY
        )
        json_res_all = req_all.content.encode('UTF-8')
        token_obj_all = json.loads(json_res_all)
        # ================Search result posts==================
        author = request.GET.get('author', False)
        if author:
            request.session['author'] = author
        else:
            author = request.session['author']
        url = settings.ICORE_API_URL+'/posts/author/'+author
        headers = {'Content-Type': 'application/json'}
        req = requests.get(
            url,
            auth=(USERNAME, PASSWORD),
            headers=headers,
            verify=SSL_VERIFY
        )
        json_res = req.content.encode('UTF-8')
        token_obj = json.loads(json_res)
        context_dict = {'search': token_obj}
        post_data = []
        if token_obj:
            for post_author in token_obj:
                post_url = settings.ICORE_API_URL+'/posts/'+post_author['ID']
                headers = {'Content-Type': 'application/json'}
                post_req = requests.get(
                    post_url,
                    auth=(USERNAME, PASSWORD),
                    headers=headers,
                    verify=SSL_VERIFY
                )
                post_json_res = post_req.content.encode('UTF-8')
                post_data.append(json.loads(post_json_res))
        paginator = Paginator(post_data, 4)
        page = request.GET.get('page')

        # =================Fetching all posts =================
        url_all = settings.ICORE_API_URL+'/posts?filter[posts_per_page]=-1'
        headers_all = {'Content-Type': 'application/json'}
        req_all = requests.get(
            url_all,
            auth=(USERNAME, PASSWORD),
            headers=headers_all,
            verify=SSL_VERIFY
        )
        json_res_all = req_all.content.encode('UTF-8')
        token_obj_count = json.loads(json_res_all)

        # ============ Fetching top Three post ====================
        count = []
        if token_obj_count:
            post_data = token_obj_count
            count = top_three_post(post_data)

        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        context_dict = {
            'PRODUCT_NAME': settings.PRODUCT_NAME,
            'icore_all': token_obj_all,
            'icore': contacts,
            'count': count
        }
        logger.info(
            logme('listed all icore post for author=%s' % (str(author)), request)
        )
        return render_to_response('blog/icoreview.html', context_dict, context)


def social_likes_shares_count(request):
    '''
    Getting Social media likes count
    '''
    if request.method == "POST":
        blog_url = request.POST['url']
        type_social_media = request.POST['type']
        social_media_like_count(blog_url, type_social_media)
        logger.info(
            logme('fetched social media counts for blog url=%s' % (
                str(blog_url)), request)
        )
        return HttpResponse('success')
    if request.method == 'GET':
        return HttpResponse('Access forbidden')
