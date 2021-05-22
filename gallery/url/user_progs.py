from gallery.view.user_progs import *
from django.conf.urls import url


urlpatterns=[
    url(r'^delete/(?P<uuid>[0-9a-f-]+)/$', UserPhotoDelete.as_view()),
    url(r'^abort_delete/(?P<uuid>[0-9a-f-]+)/$', UserPhotoAbortDelete.as_view()),
    url(r'^on_private/(?P<uuid>[0-9a-f-]+)/$', UserOnPrivatePhoto.as_view()),
    url(r'^off_private/(?P<uuid>[0-9a-f-]+)/$', UserOffPrivatePhoto.as_view()),

    url(r'^add_photo/(?P<uuid>[0-9a-f-]+)/$', AddPhotoIntUserList.as_view()),
    url(r'^add_attach_photo/$', AttachPhotoInUserList.as_view()),

    url(r'^add_list/$', PhotoListUserCreate.as_view()),
    url(r'^edit_list/(?P<uuid>[0-9a-f-]+)/$', PhotoListUserEdit.as_view(), name="photo_list_edit_user"),
    url(r'^delete_list/(?P<uuid>[0-9a-f-]+)/$', PhotoListUserDelete.as_view()),
    url(r'^abort_delete_list/(?P<uuid>[0-9a-f-]+)/$', PhotoListUserAbortDelete.as_view()),

    url(r'^add_photo_in_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', AddPhotoInUserPhotoList.as_view()),
    url(r'^remove_photo_from_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', RemovePhotoInUserPhotoList.as_view()),

    url(r'^add_list_in_collections/(?P<uuid>[0-9a-f-]+)/$', AddPhotoListInUserCollections.as_view()),
    url(r'^remove_list_from_collections/(?P<uuid>[0-9a-f-]+)/$', RemovePhotoListFromUserCollections.as_view()),
]
