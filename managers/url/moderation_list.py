from django.conf.urls import url
from managers.view.moderation_list import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^user/$', login_required(ModerationUserList.as_view())),
    url(r'^community/$', login_required(ModerationCommunityList.as_view())),
    url(r'^elect_new/$', login_required(ModerationElectNewList.as_view())),
    url(r'^photo/$', login_required(ModerationPhotoList.as_view())),
    url(r'^audio/$', login_required(ModerationAudioList.as_view())),
    url(r'^video/$', login_required(ModerationVideoList.as_view())),
    url(r'^survey/$', login_required(ModerationSurveyList.as_view())),

    url(r'^elect_new_comment/$', login_required(ModerationElectNewCommentList.as_view())),
    url(r'^blog_comment/$', login_required(ModerationBlogCommentList.as_view())),

    url(r'^user_advertiser/$', login_required(ModerationUserAdvertiserList.as_view())),
    url(r'^community_advertiser/$', login_required(ModerationCommunityAdvertiserList.as_view())),
]
