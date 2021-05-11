from django.conf.urls import url
from managers.view.moderation_list import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^user/$', login_required(ModerationUser.as_view())),
    url(r'^community/$', login_required(ModerationCommunity.as_view())),
    url(r'^elect_new/$', login_required(ModerationElectNew.as_view())),
    url(r'^photo/$', login_required(ModerationPhoto.as_view())),
    url(r'^audio/$', login_required(ModerationAudio.as_view())),
    url(r'^video/$', login_required(ModerationVideo.as_view())),
    url(r'^survey/$', login_required(ModerationSurvey.as_view())),

    url(r'^elect_new_comment/$', login_required(ModerationElectNewComment.as_view())),

    url(r'^user_advertiser/$', login_required(ModerationUserAdvertiser.as_view())),
    url(r'^community_advertiser/$', login_required(ModerationCommunityAdvertiser.as_view())),
]
