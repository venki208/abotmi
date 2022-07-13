# Django Libs
from django.shortcuts import render
from django.conf import settings
from django.db.models import Q

# Database Models
from datacenter.models import AdvisorPublishedVideo

# Local imports
from common import constants as common_constants
from common.views import get_icore_posts
from my_growth.serializers import AdvisorPublishedVideoSerializer


def index(request):
    '''
    Description : This function loads my growth page, which includes micro learning,
        ICORE, top trending and Financial game.
    '''
    req_mobile = request.POST.get("req_type", None)
    title = common_constants.MY_GROWTH
    response = {}
    user = request.user
    user_profile = user.profile
    # Get all advisor video
    advisor_videos = AdvisorPublishedVideo.objects.filter(
        status=common_constants.VIDEO_PUBLISH_APPROVED
        ).select_related('user_profile').order_by('-modified_date')
    advisor = user_profile.advisor
    total_video_ids = []
    advisor_videos_data = None
    current_advisor_videos_data = None
    other_advisors_videos_data = None
    is_current_advisor_videos_present = None
    last_current_advisor_video_id = None
    current_advisor_videos_ids = None
    other_advisors_videos_data = None
    last_other_video_id = None
    is_other_advisors_videos_present = None
    other_advisors_videos_ids = None
    icore_post_titles = None
    if advisor_videos:
        advisor_videos_data = AdvisorPublishedVideoSerializer(
            advisor_videos, many=True).data
        total_video_ids = [int(videos.id) for videos in advisor_videos]
        current_advisor_videos = advisor_videos.filter(
            user_profile=user_profile).order_by('-modified_date')
        is_current_advisor_videos_present = False
        last_current_advisor_video_id = 0
        current_advisor_videos_ids = []
        if current_advisor_videos:
            current_advisor_videos_data = AdvisorPublishedVideoSerializer(
                current_advisor_videos, many=True).data
            last_current_advisor_video_id = current_advisor_videos.last().id
            is_current_advisor_videos_present = True
            current_advisor_videos_ids = [
                int(videos.id) for videos in current_advisor_videos]
        other_advisors_videos = advisor_videos.filter(
            ~Q(user_profile__id=user_profile.id)).order_by('-modified_date')
        last_other_video_id = 0
        other_advisors_videos_ids = []
        is_other_advisors_videos_present = False
        if other_advisors_videos:
            other_advisors_videos_data = AdvisorPublishedVideoSerializer(
                other_advisors_videos, many=True).data
            last_other_video_id = other_advisors_videos.last().id
            is_other_advisors_videos_present = True
            other_advisors_videos_ids = [
                int(videos.id) for videos in other_advisors_videos]
    token_obj_all, total_icore_posts = get_icore_posts()
    if req_mobile == "mobile":
        icore_post_titles = []
        for icore in token_obj_all[:3]:
            icore_post_titles.append(
                {"title": icore.get("title", None), "id": icore.get("ID", None)})
        response['advisor_videos'] = advisor_videos_data
        response['total_video_ids'] = total_video_ids
        response['current_advisor_videos'] = current_advisor_videos_data
        response['is_current_advisor_videos_present'] = is_current_advisor_videos_present
        response['last_current_advisor_video_id'] = last_current_advisor_video_id
        response['current_advisor_videos_ids'] = current_advisor_videos_ids
        response['other_advisors_videos'] = other_advisors_videos_data
        response['last_other_video_id'] = last_other_video_id
        response['is_other_advisors_videos_present'] = is_other_advisors_videos_present
        response['last_other_video_id'] = last_other_video_id
        response['other_advisors_videos_ids'] = other_advisors_videos_ids
        response['total_icore_posts'] = icore_post_titles
        response['top_trending'] = AdvisorPublishedVideoSerializer(advisor_videos, many=True).data
        return response
    return render(request, 'my_growth/my_growth.html',  locals())


def get_all_videos(request):
    title = 'List Videos'
    advisor_videos = AdvisorPublishedVideo.objects.filter(
        status=common_constants.VIDEO_PUBLISH_APPROVED
    ).select_related('user_profile').order_by('-modified_date')

    context_dict = {
        'advisor_videos': advisor_videos,
        'title': title
    }

    return render(request, 'my_growth/top_trending_video.html', context=context_dict)