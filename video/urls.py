from django.conf.urls import url, include
from video.views import AllVideoView, UserLoadVideoAlbum


urlpatterns = [
    url(r'^$', AllVideoView.as_view(), name='all_video'),
    url(r'^load/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserLoadVideoAlbum.as_view()),

    url(r'^user_progs/', include('video.url.user_progs')),
]
