from django.conf.urls import url
from managers.view.moderation_list import *


urlpatterns = [
    url(r'^user/$', ModerationUser.as_view()),
    url(r'^community/$', ModerationCommunity.as_view()),
    url(r'^elect_new/$', ModerationElectNew.as_view()),
    url(r'^photo/$', ModerationPhoto.as_view()),
    url(r'^audio/$', ModerationAudio.as_view()),
    url(r'^video/$', ModerationVideo.as_view()),
    url(r'^survey/$', ModerationSurvey.as_view()),
]
