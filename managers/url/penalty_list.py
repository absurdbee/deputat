from django.conf.urls import url
from managers.view.penalty_list import *


urlpatterns = [
    url(r'^user/$', PenaltyUser.as_view()),
    url(r'^community/$', PenaltyCommunity.as_view()),
    url(r'^elect_new/$', PenaltyElectNew.as_view()),
    url(r'^photo/$', PenaltyPhoto.as_view()),
    url(r'^audio/$', PenaltyAudio.as_view()),
    url(r'^video/$', PenaltyVideo.as_view()),
    url(r'^survey/$', PenaltySurvey.as_view()),
    url(r'^doc/$', PenaltyDoc.as_view()),
]
