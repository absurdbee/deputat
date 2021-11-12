from django.conf.urls import url
from managers.view.logs import *


urlpatterns = [
    url(r'^elect_new/(?P<pk>\d+)/$', ElectNewLogs.as_view()),
    url(r'^user/(?P<pk>\d+)/$', UserLogs.as_view()),
    url(r'^community/(?P<pk>\d+)/$', CommunityLogs.as_view()),
    url(r'^blog/(?P<pk>\d+)/$', BlogLogs.as_view()),
    url(r'^photo/(?P<pk>\d+)/$', PhotoLogs.as_view()),
    url(r'^audio/(?P<pk>\d+)/$', AudioLogs.as_view()),
    url(r'^video/(?P<pk>\d+)/$', VideoLogs.as_view()),
    url(r'^survey/(?P<pk>\d+)/$', SurveyLogs.as_view()),
    url(r'^doc/(?P<pk>\d+)/$', DocLogs.as_view()),
]
