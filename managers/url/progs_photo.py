from django.conf.urls import url
from managers.view.photo import *


urlpatterns = [
    url(r'^add_admin/(?P<pk>\d+)/$', PhotoAdminCreate.as_view()),
    url(r'^delete_admin/(?P<pk>\d+)/$', PhotoAdminDelete.as_view()),
    url(r'^add_moderator/(?P<pk>\d+)/$', PhotoModerCreate.as_view()),
    url(r'^delete_moderator/(?P<pk>\d+)/$', PhotoModerDelete.as_view()),
    url(r'^add_editor/(?P<pk>\d+)/$', PhotoEditorCreate.as_view()),
    url(r'^delete_editor/(?P<pk>\d+)/$', PhotoEditorDelete.as_view()),

    url(r'^add_worker_admin/(?P<pk>\d+)/$', PhotoWorkerAdminCreate.as_view()),
    url(r'^delete_worker_admin/(?P<pk>\d+)/$', PhotoWorkerAdminDelete.as_view()),
    url(r'^add_worker_moderator/(?P<pk>\d+)/$', PhotoWorkerModerCreate.as_view()),
    url(r'^delete_worker_moderator/(?P<pk>\d+)/$', PhotoWorkerModerDelete.as_view()),
    url(r'^add_worker_editor/(?P<pk>\d+)/$', PhotoWorkerEditorCreate.as_view()),
    url(r'^delete_worker_editor/(?P<pk>\d+)/$', PhotoWorkerEditorDelete.as_view()),

    url(r'^create_close/(?P<uuid>[0-9a-f-]+)/$', PhotoCloseCreate.as_view()),
    url(r'^delete_close/(?P<uuid>[0-9a-f-]+)/$', PhotoCloseDelete.as_view()),
    url(r'^create_rejected/(?P<uuid>[0-9a-f-]+)/$', PhotoRejectedCreate.as_view()),
    url(r'^create_claim/(?P<uuid>[0-9a-f-]+)/$', PhotoClaimCreate.as_view()),
    url(r'^unverify/(?P<photo_uuid>[0-9a-f-]+)/(?P<obj_pk>\d+)/$', PhotoUnverify.as_view()),

    url(r'^list_create_close/(?P<pk>\d+)/$', ListPhotoCloseCreate.as_view()),
    url(r'^list_delete_close/(?P<pk>\d+)/$', ListPhotoCloseDelete.as_view()),
    url(r'^list_create_rejected/(?P<pk>\d+)/$', ListPhotoRejectedCreate.as_view()),
    url(r'^list_create_claim/(?P<pk>\d+)/$', ListPhotoClaimCreate.as_view()),
    url(r'^list_unverify/(?P<pk>\d+)/(?P<obj_pk>\d+)/$', ListPhotoUnverify.as_view()),
]
