from django.conf.urls import url, include
from video.views import *


urlpatterns = [
    url(r'^$', AllVideoView.as_view(), name='all_video'),
    url(r'^user_load/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserLoadVideoList.as_view()),
    url(r'^user_video/(?P<pk>\d+)/$', UserVideo.as_view(), name='user_video'),
    url(r'^user_detail/(?P<pk>\d+)/$', UserVideoDetail.as_view(), name='u_video'),
    url(r'^user_list/(?P<uuid>[0-9a-f-]+)/$', UserVideoList.as_view(), name='user_videolist'),

    url(r'^user_progs/', include('video.url.user_progs')),
]
