from django.conf.urls import url
from managers.view.logs import *


urlpatterns = [
    url(r'^elect_new/(?P<pk>\d+)/$', ElectNewLogs.as_view()),
    url(r'^user/(?P<pk>\d+)/$', UserLogs.as_view()),
    url(r'^community/(?P<pk>\d+)/$', CommunityLogs.as_view()),
    #url(r'^blog/(?P<pk>\d+)/$', ModerationBlog.as_view()),
    #url(r'^photo/(?P<pk>\d+)/$', ModerationPhoto.as_view()),
    #url(r'^audio/(?P<pk>\d+)/$', ModerationAudio.as_view()),
    #url(r'^video/(?P<pk>\d+)/$', ModerationVideo.as_view()),
    #url(r'^survey/(?P<pk>\d+)/$', ModerationSurvey.as_view()),
    #url(r'^doc/(?P<pk>\d+)/$', ModerationDoc.as_view()),
]
