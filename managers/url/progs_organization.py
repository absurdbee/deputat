from django.conf.urls import url
from managers.view.organization import *


urlpatterns = [
    url(r'^add_admin/(?P<pk>\d+)/$', OrganizationAdminCreate.as_view()),
    url(r'^delete_admin/(?P<pk>\d+)/$', OrganizationAdminDelete.as_view()),
    url(r'^add_moderator/(?P<pk>\d+)/$', OrganizationModerCreate.as_view()),
    url(r'^delete_moderator/(?P<pk>\d+)/$', OrganizationModerDelete.as_view()),
    url(r'^add_editor/(?P<pk>\d+)/$', OrganizationEditorCreate.as_view()),
    url(r'^delete_editor/(?P<pk>\d+)/$', OrganizationEditorDelete.as_view()),

    url(r'^add_worker_admin/(?P<pk>\d+)/$', OrganizationWorkerAdminCreate.as_view()),
    url(r'^delete_worker_admin/(?P<pk>\d+)/$', OrganizationWorkerAdminDelete.as_view()),
    url(r'^add_worker_moderator/(?P<pk>\d+)/$', OrganizationWorkerModerCreate.as_view()),
    url(r'^delete_worker_moderator/(?P<pk>\d+)/$', OrganizationWorkerModerDelete.as_view()),
    url(r'^add_worker_editor/(?P<pk>\d+)/$', OrganizationWorkerEditorCreate.as_view()),
    url(r'^delete_worker_editor/(?P<pk>\d+)/$', OrganizationWorkerEditorDelete.as_view()),

    url(r'^create_close/(?P<pk>\d+)/$', OrganizationCloseCreate.as_view()),
    url(r'^delete_close/(?P<pk>\d+)/$', OrganizationCloseDelete.as_view()),
    url(r'^create_rejected/(?P<pk>\d+)/$', OrganizationRejectedCreate.as_view()),
    url(r'^create_claim/(?P<pk>\d+)/$', OrganizationClaimCreate.as_view()),
    url(r'^unverify/(?P<pk>\d+)/$', OrganizationUnverify.as_view()),

    #url(r'^comment_create_close/(?P<pk>\d+)/$', CommentOrganizationCloseCreate.as_view()),
    #url(r'^comment_delete_close/(?P<pk>\d+)/$', CommentOrganizationCloseDelete.as_view()),
    #url(r'^comment_create_rejected/(?P<pk>\d+)/$', CommentOrganizationRejectedCreate.as_view()),
    #url(r'^comment_create_claim/(?P<pk>\d+)/$', CommentOrganizationClaimCreate.as_view()),
    #url(r'^comment_unverify/(?P<pk>\d+)/$', CommentOrganizationUnverify.as_view()),
]
