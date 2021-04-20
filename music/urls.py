from django.conf.urls import url, include
from music.views import *


urlpatterns = [
    url(r'^$', AllMusicView.as_view(), name='all_music'),
    url(r'^load/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserLoadPlaylist.as_view(), name='u_playlist_load'),
    url(r'^user_music/(?P<pk>\d+)/$', UserMusic.as_view(), name='user_music'),
    url(r'^user_playlist/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserMusicList.as_view(), name='user_playlist'),

    url(r'^user_progs/', include('music.url.user_progs')),
]
