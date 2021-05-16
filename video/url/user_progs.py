from django.conf.urls import url
from video.view.user_progs import *


urlpatterns = [
    url(r'^add_list/$', UserVideolistCreate.as_view()),
    url(r'^edit_list/(?P<uuid>[0-9a-f-]+)/$', UserVideolistEdit.as_view()),
    url(r'^delete_list/(?P<uuid>[0-9a-f-]+)/$', UserVideolistDelete.as_view()),
    url(r'^abort_delete_list/(?P<uuid>[0-9a-f-]+)/$', UserVideolistAbortDelete.as_view()),
    url(r'^add_list/(?P<pk>\d+)/$', UserVideolistAdd.as_view()),
    url(r'^remove_list/(?P<pk>\d+)/$', UserVideolistRemove.as_view()),

    url(r'^create_video/$', UserVideoCreate.as_view()),
    url(r'^edit_video/(?P<pk>\d+)/$', UserVideoEdit.as_view()),
    url(r'^remove_video/(?P<pk>\d+)/$', UserVideoRemove.as_view()),
    url(r'^abort_remove_video/(?P<pk>\d+)/$', UseVideoAbortRemove.as_view()),

    url(r'^add_video_in_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserVideoListAdd.as_view()),
    url(r'^remove_video_from_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserVideoListRemove.as_view()),
]
