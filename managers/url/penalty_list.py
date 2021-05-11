from django.conf.urls import url
from managers.view.penalty_list import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^user/$', login_required(PenaltyUser.as_view())),
    url(r'^community/$', login_required(PenaltyCommunity.as_view())),
    url(r'^elect_new/$', login_required(PenaltyElectNew.as_view())),
    url(r'^photo/$', login_required(PenaltyPhoto.as_view())),
    url(r'^audio/$', login_required(PenaltyAudio.as_view())),
    url(r'^video/$', login_required(PenaltyVideo.as_view())),
    url(r'^survey/$', login_required(PenaltySurvey.as_view())),

    url(r'^elect_new_comment/$', login_required(PenaltyElectNewComment.as_view())),

    url(r'^user_advertiser/$', login_required(PenaltyUserAdvertiser.as_view())),
    url(r'^community_advertiser/$', login_required(PenaltyCommunityAdvertiser.as_view())),
]
