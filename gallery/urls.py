from django.conf.urls import url, include
from gallery.views import *


urlpatterns=[
	url(r'^(?P<pk>\d+)/$', UserGallery.as_view(), name="user_gallery"),
	url(r'^list/(?P<uuid>[0-9a-f-]+)/$', UserPhotoList.as_view(), name="user_list"),
	url(r'^load_list/(?P<pk>\d+)/$', UserLoadList.as_view()),
    url(r'^photo/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserListPhoto.as_view(), name="u_photo"),
	url(r'^elect_new_photo/(?P<pk>\d+)/(?P<photo_pk>\d+)/$', UserElectNewPhoto.as_view(), name="u_elect_new_photo"),
	url(r'^blog_comment_photo/(?P<pk>\d+)/(?P<photo_pk>\d+)/$', UserBlogCommentPhoto.as_view(), name="u_blog_comment_photo"),
	url(r'^elect_new_comment_photo/(?P<pk>\d+)/(?P<photo_pk>\d+)/$', UserElectNewCommentPhoto.as_view(), name="u_elect_new_comment_photo"),
	url(r'^preview_photo/(?P<pk>\d+)/$', GetUserPhoto.as_view()),

	url(r'^user_progs/', include('gallery.url.user_progs')),
]
