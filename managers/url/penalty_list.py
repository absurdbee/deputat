from django.conf.urls import url
from managers.view.penalty_list import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^user/$', login_required(PenaltyUserList.as_view())),
    url(r'^community/$', login_required(PenaltyCommunityList.as_view())),
    url(r'^elect_new/$', login_required(PenaltyElectNewList.as_view())),
    url(r'^photo/$', login_required(PenaltyPhotoList.as_view())),
    url(r'^audio/$', login_required(PenaltyAudioList.as_view())),
    url(r'^video/$', login_required(PenaltyVideoList.as_view())),
    url(r'^survey/$', login_required(PenaltySurveyList.as_view())),

    url(r'^elect_new_comment/$', login_required(PenaltyElectNewCommentList.as_view())),
    url(r'^blog_comment/$', login_required(PenaltyBlogCommentList.as_view())),

    url(r'^user_advertiser/$', login_required(PenaltyUserAdvertiserList.as_view())),
    url(r'^community_advertiser/$', login_required(PenaltyCommunityAdvertiserList.as_view())),
]
