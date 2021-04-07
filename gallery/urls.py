from django.conf.urls import url, include
from gallery.views import *


urlpatterns=[
	url(r'^(?P<pk>\d+)/$', UserGallery.as_view(), name="user_gallery"),
	url(r'^album/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserAlbum.as_view(), name="user_album"),
	url(r'^load/(?P<pk>\d+)/$', UserLoadAlbum.as_view()),
    url(r'^photo/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserAlbumPhoto.as_view(), name="u_photo"),
	url(r'^post_photo/(?P<pk>\d+)/(?P<photo_pk>\d+)/$', UserElectNewPhoto.as_view(), name="u_elect_new_photo"),
	url(r'^comment_photo/(?P<pk>\d+)/(?P<photo_pk>\d+)/$', UserCommentPhoto.as_view(), name="u_elect_new_comment_photo"),
	url(r'^preview_photo/(?P<pk>\d+)/$', GetUserPhoto.as_view()),

	url(r'^user_progs/', include('gallery.url.user_progs')),
]
