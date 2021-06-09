from django.conf.urls import url
from managers.view.blog import *


urlpatterns = [
    url(r'^add_admin/(?P<pk>\d+)/$', BlogAdminCreate.as_view()),
    url(r'^delete_admin/(?P<pk>\d+)/$', BlogAdminDelete.as_view()),
    url(r'^add_moderator/(?P<pk>\d+)/$', BlogModerCreate.as_view()),
    url(r'^delete_moderator/(?P<pk>\d+)/$', BlogModerDelete.as_view()),
    url(r'^add_editor/(?P<pk>\d+)/$', BlogEditorCreate.as_view()),
    url(r'^delete_editor/(?P<pk>\d+)/$', BlogEditorDelete.as_view()),

    url(r'^add_worker_admin/(?P<pk>\d+)/$', BlogWorkerAdminCreate.as_view()),
    url(r'^delete_worker_admin/(?P<pk>\d+)/$', BlogWorkerAdminDelete.as_view()),
    url(r'^add_worker_moderator/(?P<pk>\d+)/$', BlogWorkerModerCreate.as_view()),
    url(r'^delete_worker_moderator/(?P<pk>\d+)/$', BlogWorkerModerDelete.as_view()),
    url(r'^add_worker_editor/(?P<pk>\d+)/$', BlogWorkerEditorCreate.as_view()),
    url(r'^delete_worker_editor/(?P<pk>\d+)/$', BlogWorkerEditorDelete.as_view()),

    url(r'^create_close/(?P<uuid>[0-9a-f-]+)/$', BlogCloseCreate.as_view()),
    url(r'^delete_close/(?P<uuid>[0-9a-f-]+)/$', BlogCloseDelete.as_view()),
    url(r'^create_rejected/(?P<uuid>[0-9a-f-]+)/$', BlogRejectedCreate.as_view()),
    url(r'^create_claim/(?P<pk>\d+)/$', BlogClaimCreate.as_view()),
    url(r'^unverify/(?P<post_uuid>[0-9a-f-]+)/$', BlogUnverify.as_view()),

    url(r'^comment_create_close/(?P<pk>\d+)/$', CommentBlogCloseCreate.as_view()),
    url(r'^comment_delete_close/(?P<pk>\d+)/$', CommentBlogCloseDelete.as_view()),
    url(r'^comment_create_rejected/(?P<pk>\d+)/$', CommentBlogRejectedCreate.as_view()),
    url(r'^comment_create_claim/(?P<pk>\d+)/$', CommentBlogClaimCreate.as_view()),
    url(r'^comment_unverify/(?P<pk>\d+)/$', CommentBlogUnverify.as_view()),
]
