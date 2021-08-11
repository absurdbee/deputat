from django.conf.urls import url
from managers.view.audio import *


urlpatterns = [
    url(r'^add_admin/(?P<pk>\d+)/$', AudioAdminCreate.as_view()),
    url(r'^delete_admin/(?P<pk>\d+)/$', AudioAdminDelete.as_view()),
    url(r'^add_moderator/(?P<pk>\d+)/$', AudioModerCreate.as_view()),
    url(r'^delete_moderator/(?P<pk>\d+)/$', AudioModerDelete.as_view()),
    url(r'^add_editor/(?P<pk>\d+)/$', AudioEditorCreate.as_view()),
    url(r'^delete_editor/(?P<pk>\d+)/$', AudioEditorDelete.as_view()),

    url(r'^add_worker_admin/(?P<pk>\d+)/$', AudioWorkerAdminCreate.as_view()),
    url(r'^delete_worker_admin/(?P<pk>\d+)/$', AudioWorkerAdminDelete.as_view()),
    url(r'^add_worker_moderator/(?P<pk>\d+)/$', AudioWorkerModerCreate.as_view()),
    url(r'^delete_worker_moderator/(?P<pk>\d+)/$', AudioWorkerModerDelete.as_view()),
    url(r'^add_worker_editor/(?P<pk>\d+)/$', AudioWorkerEditorCreate.as_view()),
    url(r'^delete_worker_editor/(?P<pk>\d+)/$', AudioWorkerEditorDelete.as_view()),

    url(r'^create_close/(?P<pk>\d+)/$', OrganizationCloseCreate.as_view()),
    url(r'^delete_close/(?P<pk>\d+)/$', OrganizationCloseDelete.as_view()),
    url(r'^create_rejected/(?P<pk>\d+)/$', OrganizationRejectedCreate.as_view()),
    url(r'^create_claim/(?P<pk>\d+)/$', OrganizationClaimCreate.as_view()),
    url(r'^unverify/(?P<pk>\d+)/$', OrganizationUnverify.as_view()),

    url(r'^comment_create_close/(?P<pk>\d+)/$', CommentOrganizationCloseCreate.as_view()),
    url(r'^comment_delete_close/(?P<pk>\d+)/$', CommentOrganizationCloseDelete.as_view()),
    url(r'^comment_create_rejected/(?P<pk>\d+)/$', CommentOrganizationRejectedCreate.as_view()),
    url(r'^comment_create_claim/(?P<pk>\d+)/$', CommentOrganizationClaimCreate.as_view()),
    url(r'^comment_unverify/(?P<pk>\d+)/$', CommentOrganizationUnverify.as_view()),
]
