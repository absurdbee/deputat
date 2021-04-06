from django.conf.urls import url, include
from video.views import *


urlpatterns = [
    url(r'^$', AllVideoView.as_view(), name='all_video'),
    url(r'^load/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserLoadVideoAlbum.as_view()),
    url(r'^user_video/(?P<pk>\d+)/$', UserVideo.as_view(), name='user_video'),
    url(r'^user_videolist/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserVideoList.as_view(), name='user_videolist'),
    url(r'^create_video_attach/(?P<pk>\d+)/$', UserVideoAttachCreate.as_view()),
    url(r'^create_video/(?P<pk>\d+)/$', UserVideoCreate.as_view()),
    url(r'^get_album_preview/(?P<pk>\d+)/$', UserVideoAlbumPreview.as_view()),
    url(r'^create_list/(?P<pk>\d+)/$', UserVideoListCreate.as_view()),
    url(r'^edit_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserVideolistEdit.as_view()),

    url(r'^user_progs/', include('video.url.user_progs')),
]
