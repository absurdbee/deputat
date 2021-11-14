from django.conf.urls import url
from video.view.user_progs import *


urlpatterns = [
    url(r'^add_list/$', UserVideolistCreate.as_view()),
    url(r'^edit_list/(?P<uuid>[0-9a-f-]+)/$', UserVideolistEdit.as_view()),
    url(r'^delete_list/(?P<uuid>[0-9a-f-]+)/$', UserVideolistDelete.as_view()),
    url(r'^abort_delete_list/(?P<uuid>[0-9a-f-]+)/$', UserVideolistAbortDelete.as_view()),
    url(r'^add_list_in_collections/(?P<uuid>[0-9a-f-]+)/$', AddVideoListInUserCollections.as_view()),
    url(r'^remove_list_from_collections/(?P<uuid>[0-9a-f-]+)/$', RemoveVideoListFromUserCollections.as_view()),

    url(r'^create_video/$', UserVideoCreate.as_view()),
    url(r'^edit_video/(?P<pk>\d+)/$', UserVideoEdit.as_view()),
    url(r'^delete_video/(?P<pk>\d+)/$', UserVideoRemove.as_view()),
    url(r'^abort_delete_video/(?P<pk>\d+)/$', UserVideoAbortRemove.as_view()),
    url(r'^on_private/(?P<pk>\d+)/$', UserOnPrivateVideo.as_view()),
    url(r'^off_private/(?P<pk>\d+)/$', UserOffPrivateVideo.as_view()),

    url(r'^add_video_in_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', AddVideoInUserVideoList.as_view()),
    url(r'^remove_video_from_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', RemoveVideoInUserVideoList.as_view()),
    url(r'^add_video_in_media_list/(?P<pk>\d+)/$', AddVideoInUserMediaList.as_view()),
    url(r'^remove_video_from_media_list/(?P<pk>\d+)/$', RemoveVideoInUserMediaList.as_view()),
]
