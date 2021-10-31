from django.conf.urls import url, include
from video.views import *


urlpatterns = [
    url(r'^$', AllVideoView.as_view(), name='all_video'),
    url(r'^user_load/(?P<pk>\d+)/$', UserLoadVideoList.as_view()),
    url(r'^penalty_load/(?P<pk>\d+)/$', UserLoadPenaltyVideoList.as_view()),
    url(r'^moderated_load/(?P<pk>\d+)/$', UserLoadModeratedVideoList.as_view()),
    url(r'^user_video/(?P<pk>\d+)/$', UserVideo.as_view(), name='user_video'),
    url(r'^user_detail/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserVideoDetail_2.as_view(), name='u_video'),
    url(r'^user_list/(?P<uuid>[0-9a-f-]+)/$', UserVideoList.as_view(), name='user_video_list'),
    url(r'^video_detail/(?P<pk>\d+)/$', UserVideoDetail.as_view()),
    url(r'^media_video_detail/(?P<pk>\d+)/$', ManagerVideoDetail.as_view()),

    url(r'^user_progs/', include('video.url.user_progs')),
]
