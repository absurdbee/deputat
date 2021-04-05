from django.conf.urls import url
from music.view.user_progs import *


urlpatterns = [
    url(r'^create_soundcloud_set/(?P<pk>\d+)/$', UserSoundcloudSetCreate.as_view()),
    url(r'^soundcloud_set/(?P<uuid>[0-9a-f-]+)/$', UserSoundcloudSet.as_view()),
    url(r'^create_list/(?P<pk>\d+)/$', UserPlaylistCreate.as_view()),
    url(r'^edit_list/(?P<uuid>[0-9a-f-]+)/$', UserPlaylistEdit.as_view()),
    url(r'^delete_list/(?P<uuid>[0-9a-f-]+)/$', UserPlaylistDelete.as_view()),
    url(r'^abort_delete_list/(?P<uuid>[0-9a-f-]+)/$', UserPlaylistAbortDelete.as_view()),
    url(r'^add_list/(?P<uuid>[0-9a-f-]+)/$', UserPlaylistAdd.as_view()),
    url(r'^remove_list/(?P<uuid>[0-9a-f-]+)/$', UserPlaylistRemove.as_view()),

    url(r'^delete_track/(?P<pk>\d+)/$', UserTrackRemove.as_view()),
    url(r'^abort_delete_track/(?P<pk>\d+)/$', UserTrackAbortRemove.as_view()),
    url(r'^add_track_in_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserTrackListAdd.as_view()),
    url(r'^remove_track_in_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserTrackListRemove.as_view()),
]
