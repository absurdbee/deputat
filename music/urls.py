from django.conf.urls import url, include
from music.views import AllMusicView, UserLoadPlaylist, MusicPlaylistPreview


urlpatterns = [
    url(r'^$', AllMusicView.as_view(), name='all_music'),
    url(r'^load/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserLoadPlaylist.as_view()),
    url(r'^playlist_preview/(?P<pk>\d+)/$', MusicPlaylistPreview.as_view()),

    url(r'^user_progs/', include('music.url.user_progs')),
]
