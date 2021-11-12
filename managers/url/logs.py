from django.conf.urls import url
from managers.view.logs import *


urlpatterns = [
    url(r'^elect_new/(?P<pk>\d+)/$', ElectNewLogs.as_view()),
    url(r'^user/(?P<pk>\d+)/$', UserLogs.as_view()),
    url(r'^community/$', CommunityLogs.as_view()),
    #url(r'^elect_new/$', ModerationElectNew.as_view()),
    #url(r'^blog/$', ModerationBlog.as_view()),
    #url(r'^photo/$', ModerationPhoto.as_view()),
    #url(r'^audio/$', ModerationAudio.as_view()),
    #url(r'^video/$', ModerationVideo.as_view()),
    #url(r'^survey/$', ModerationSurvey.as_view()),
    #url(r'^doc/$', ModerationDoc.as_view()),
]
