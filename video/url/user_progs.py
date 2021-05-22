from django.conf.urls import url
from video.view.user_progs import *


urlpatterns = [
    url(r'^add_list/$', UserVideolistCreate.as_view()),
    url(r'^edit_list/(?P<uuid>[0-9a-f-]+)/$', UserVideolistEdit.as_view()),
    url(r'^delete_list/(?P<uuid>[0-9a-f-]+)/$', UserVideolistDelete.as_view()),
    url(r'^abort_delete_list/(?P<uuid>[0-9a-f-]+)/$', UserVideolistAbortDelete.as_view()),
    url(r'^add_list_in_collections/(?P<pk>\d+)/$', AddVideoListInUserCollections.as_view()),
    url(r'^remove_list_from_collections/(?P<pk>\d+)/$', RemoveVideoListFromUserCollections.as_view()),

    url(r'^create_video/$', UserVideoCreate.as_view()),
    url(r'^edit_video/(?P<pk>\d+)/$', UserVideoEdit.as_view()),
    url(r'^delete_video/(?P<uuid>[0-9a-f-]+)/$', UserVideoRemove.as_view()),
    url(r'^abort_delete_video/(?P<uuid>[0-9a-f-]+)/$', UserVideoAbortRemove.as_view()),
    url(r'^on_private/(?P<uuid>[0-9a-f-]+)/$', UserOnPrivateVideo.as_view()),
    url(r'^off_private/(?P<uuid>[0-9a-f-]+)/$', UserOffPrivateVideo.as_view()),

    url(r'^add_video_in_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', AddVideoInUserVideoList.as_view()),
    url(r'^remove_video_from_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', RemoveVideoInUserVideoList.as_view()),
]
