from django.conf.urls import url
from managers.view.video import *


urlpatterns = [
    url(r'^add_admin/(?P<pk>\d+)/$', VideoAdminCreate.as_view()),
    url(r'^delete_admin/(?P<pk>\d+)/$', VideoAdminDelete.as_view()),
    url(r'^add_moderator/(?P<pk>\d+)/$', VideoModerCreate.as_view()),
    url(r'^delete_moderator/(?P<pk>\d+)/$', VideoModerDelete.as_view()),
    url(r'^add_editor/(?P<pk>\d+)/$', VideoEditorCreate.as_view()),
    url(r'^delete_editor/(?P<pk>\d+)/$', VideoEditorDelete.as_view()),

    url(r'^add_worker_admin/(?P<pk>\d+)/$', VideoWorkerAdminCreate.as_view()),
    url(r'^delete_worker_admin/(?P<pk>\d+)/$', VideoWorkerAdminDelete.as_view()),
    url(r'^add_worker_moderator/(?P<pk>\d+)/$', VideoWorkerModerCreate.as_view()),
    url(r'^delete_worker_moderator/(?P<pk>\d+)/$', VideoWorkerModerDelete.as_view()),
    url(r'^add_worker_editor/(?P<pk>\d+)/$', VideoWorkerEditorCreate.as_view()),
    url(r'^delete_worker_editor/(?P<pk>\d+)/$', VideoWorkerEditorDelete.as_view()),

    url(r'^create_close/(?P<uuid>[0-9a-f-]+)/$', VideoCloseCreate.as_view()),
    url(r'^delete_close/(?P<uuid>[0-9a-f-]+)/$', VideoCloseDelete.as_view()),
    url(r'^create_rejected/(?P<uuid>[0-9a-f-]+)/$', VideoRejectedCreate.as_view()),
    url(r'^create_claim/(?P<uuid>[0-9a-f-]+)/$', VideoClaimCreate.as_view()),
    url(r'^unverify/(?P<video_uuid>[0-9a-f-]+)/(?P<obj_pk>\d+)/$', VideoUnverify.as_view()),

    url(r'^list_create_close/(?P<pk>\d+)/$', ListVideoCloseCreate.as_view()),
    url(r'^list_delete_close/(?P<pk>\d+)/$', ListVideoCloseDelete.as_view()),
    url(r'^list_create_rejected/(?P<pk>\d+)/$', ListVideoRejectedCreate.as_view()),
    url(r'^list_create_claim/(?P<pk>\d+)/$', ListVideoClaimCreate.as_view()),
    url(r'^list_unverify/(?P<pk>\d+)/(?P<obj_pk>\d+)/$', ListVideoUnverify.as_view()),
]
