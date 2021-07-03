from django.conf.urls import url, include
from gallery.views import *


urlpatterns=[
	url(r'^user/(?P<pk>\d+)/$', UserGallery.as_view(), name="user_gallery"),
	url(r'^user_list/(?P<uuid>[0-9a-f-]+)/$', UserPhotoList.as_view(), name="user_list"),
	url(r'^user_load/(?P<pk>\d+)/$', UserLoadPhotoList.as_view()),
	url(r'^penalty_load/(?P<pk>\d+)/$', UserLoadPenaltyPhotolist.as_view()),
    url(r'^moderated_load/(?P<pk>\d+)/$', UserLoadModeratedPhotolist.as_view()),

    url(r'^photo/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserListPhoto.as_view(), name="u_photo"),
	url(r'^photo_detail/(?P<uuid>[0-9a-f-]+)/$', UserPhotoDetail.as_view(), name="u_photo_detail"),
	url(r'^blog_photo/(?P<pk>\d+)/(?P<photo_pk>\d+)/$', UserBlogPhoto.as_view(), name="u_blog_photo"),
	url(r'^elect_new_photo/(?P<pk>\d+)/(?P<photo_pk>\d+)/$', UserElectNewPhoto.as_view(), name="u_elect_new_photo"),
	url(r'^blog_comment_photo/(?P<pk>\d+)/(?P<photo_pk>\d+)/$', UserBlogCommentPhoto.as_view(), name="u_blog_comment_photo"),
	url(r'^elect_new_comment_photo/(?P<pk>\d+)/(?P<photo_pk>\d+)/$', UserElectNewCommentPhoto.as_view(), name="u_elect_new_comment_photo"),
	url(r'^preview_photo/(?P<pk>\d+)/$', GetUserPhoto.as_view()),
	url(r'^penalty_photo/(?P<pk>\d+)/$', GetUserPenaltyPhoto.as_view()),
	url(r'^moderated_photo/(?P<pk>\d+)/$', GetUserModeratedPhoto.as_view()),

	url(r'^user_progs/', include('gallery.url.user_progs')),
]
