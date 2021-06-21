from django.conf.urls import url
from managers.view.elect_new import *


urlpatterns = [
    url(r'^add_admin/(?P<pk>\d+)/$', ElectNewAdminCreate.as_view()),
    url(r'^delete_admin/(?P<pk>\d+)/$', ElectNewAdminDelete.as_view()),
    url(r'^add_moderator/(?P<pk>\d+)/$', ElectNewModerCreate.as_view()),
    url(r'^delete_moderator/(?P<pk>\d+)/$', ElectNewModerDelete.as_view()),
    url(r'^add_editor/(?P<pk>\d+)/$', ElectNewEditorCreate.as_view()),
    url(r'^delete_editor/(?P<pk>\d+)/$', ElectNewEditorDelete.as_view()),

    url(r'^add_worker_admin/(?P<pk>\d+)/$', ElectNewWorkerAdminCreate.as_view()),
    url(r'^delete_worker_admin/(?P<pk>\d+)/$', ElectNewWorkerAdminDelete.as_view()),
    url(r'^add_worker_moderator/(?P<pk>\d+)/$', ElectNewWorkerModerCreate.as_view()),
    url(r'^delete_worker_moderator/(?P<pk>\d+)/$', ElectNewWorkerModerDelete.as_view()),
    url(r'^add_worker_editor/(?P<pk>\d+)/$', ElectNewWorkerEditorCreate.as_view()),
    url(r'^delete_worker_editor/(?P<pk>\d+)/$', ElectNewWorkerEditorDelete.as_view()),

    url(r'^create_publish/(?P<pk>\d+)/$', PublishElectNew.as_view()),
    url(r'^suggest_rejected/(?P<pk>\d+)/$', RejectElectNew.as_view()),

    url(r'^create_close/(?P<uuid>[0-9a-f-]+)/$', ElectNewCloseCreate.as_view()),
    url(r'^delete_close/(?P<uuid>[0-9a-f-]+)/$', ElectNewCloseDelete.as_view()),
    url(r'^create_rejected/(?P<uuid>[0-9a-f-]+)/$', ElectNewRejectedCreate.as_view()),
    url(r'^create_claim/(?P<pk>\d+)/$', ElectNewClaimCreate.as_view()),
    url(r'^unverify/(?P<post_uuid>[0-9a-f-]+)/$', ElectNewUnverify.as_view()),

    url(r'^comment_create_close/(?P<pk>\d+)/$', CommentElectNewCloseCreate.as_view()),
    url(r'^comment_delete_close/(?P<pk>\d+)/$', CommentElectNewCloseDelete.as_view()),
    url(r'^comment_create_rejected/(?P<pk>\d+)/$', CommentElectNewRejectedCreate.as_view()),
    url(r'^comment_create_claim/(?P<pk>\d+)/$', CommentElectNewClaimCreate.as_view()),
    url(r'^comment_unverify/(?P<pk>\d+)/$', CommentElectNewUnverify.as_view()),
]
