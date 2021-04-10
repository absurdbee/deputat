from django.conf.urls import url
from video.view.user_progs import *


urlpatterns = [
    url(r'^delete/(?P<uuid>[0-9a-f-]+)/$', UserVideoDelete.as_view()),
    url(r'^abort_delete/(?P<uuid>[0-9a-f-]+)/$', UserVideoAbortDelete.as_view()),
    url(r'^on_private/(?P<uuid>[0-9a-f-]+)/$', UserOnPrivateVideo.as_view()),
    url(r'^off_private/(?P<uuid>[0-9a-f-]+)/$', UserOffPrivateVideo.as_view()),
    url(r'^add_video_in_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserVideoListAdd.as_view()),
    url(r'^remove_video_in_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserVideoListRemove.as_view()),

    url(r'^delete_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserVideolistDelete.as_view()),
    url(r'^abort_delete_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserVideolistAbortDelete.as_view()),
    url(r'^add_list/(?P<uuid>[0-9a-f-]+)/$', UserVideoAlbumAdd.as_view()),
    url(r'^remove_list/(?P<uuid>[0-9a-f-]+)/$', UserVideoAlbumRemove.as_view()),
]
