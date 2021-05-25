from django.conf.urls import url
from managers.view.penalty_list import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^user/$', PenaltyUser.as_view()),
    url(r'^community/$', PenaltyCommunity.as_view()),
    url(r'^elect_new/$', PenaltyElectNew.as_view()),
    url(r'^photo/$', PenaltyPhoto.as_view()),
    url(r'^audio/$', PenaltyAudio.as_view()),
    url(r'^video/$', PenaltyVideo.as_view()),
    url(r'^survey/$', PenaltySurvey.as_view()),
]
