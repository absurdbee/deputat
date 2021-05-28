from django.conf.urls import url, include
from music.views import *


urlpatterns = [
    url(r'^$', AllMusicView.as_view(), name='all_music'),
    url(r'^user_load/(?P<pk>\d+)/$', UserLoadPlaylist.as_view(), name='u_playlist_load'),
    url(r'^penalty_load/(?P<pk>\d+)/$', UserLoadPenalty{Playlist.as_view()),
    url(r'^moderated_load/(?P<pk>\d+)/$', UserLoadModeratedPlaylist.as_view()),
    url(r'^user_music/(?P<pk>\d+)/$', UserMusic.as_view(), name='user_music'),
    url(r'^user_list/(?P<uuid>[0-9a-f-]+)/$', UserMusicList.as_view(), name='user_playlist'),

    url(r'^user_progs/', include('music.url.user_progs')),
]
