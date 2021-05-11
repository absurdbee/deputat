from django.conf.urls import url
from managers.view.elect_new import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^add_admin/(?P<pk>\d+)/$', login_required(ElectNewAdminCreate.as_view())),
    url(r'^delete_admin/(?P<pk>\d+)/$', login_required(ElectNewAdminDelete.as_view())),
    url(r'^add_moderator/(?P<pk>\d+)/$', login_required(ElectNewModerCreate.as_view())),
    url(r'^delete_moderator/(?P<pk>\d+)/$', login_required(ElectNewModerDelete.as_view())),
    url(r'^add_editor/(?P<pk>\d+)/$', login_required(ElectNewEditorCreate.as_view())),
    url(r'^delete_editor/(?P<pk>\d+)/$', login_required(ElectNewEditorDelete.as_view())),

    url(r'^add_worker_admin/(?P<pk>\d+)/$', login_required(ElectNewWorkerAdminCreate.as_view())),
    url(r'^delete_worker_admin/(?P<pk>\d+)/$', login_required(ElectNewWorkerAdminDelete.as_view())),
    url(r'^add_worker_moderator/(?P<pk>\d+)/$', login_required(ElectNewWorkerModerCreate.as_view())),
    url(r'^delete_worker_moderator/(?P<pk>\d+)/$', login_required(ElectNewWorkerModerDelete.as_view())),
    url(r'^add_worker_editor/(?P<pk>\d+)/$', login_required(ElectNewWorkerEditorCreate.as_view())),
    url(r'^delete_worker_editor/(?P<pk>\d+)/$', login_required(ElectNewWorkerEditorDelete.as_view())),

    url(r'^create_close/(?P<uuid>[0-9a-f-]+)/$', login_required(ElectNewCloseCreate.as_view())),
    url(r'^delete_close/(?P<uuid>[0-9a-f-]+)/$', login_required(ElectNewCloseDelete.as_view())),
    url(r'^create_rejected/(?P<uuid>[0-9a-f-]+)/$', login_required(ElectNewRejectedCreate.as_view())),
    url(r'^create_claim/(?P<pk>\d+)/$', login_required(ElectNewClaimCreate.as_view())),
    url(r'^unverify/(?P<post_uuid>[0-9a-f-]+)/(?P<obj_pk>\d+)/$', login_required(ElectNewUnverify.as_view())),

    url(r'^comment_create_close/(?P<pk>\d+)/$', login_required(CommentElectNewCloseCreate.as_view())),
    url(r'^comment_delete_close/(?P<pk>\d+)/$', login_required(CommentElectNewCloseDelete.as_view())),
    url(r'^comment_create_rejected/(?P<pk>\d+)/$', login_required(CommentElectNewRejectedCreate.as_view())),
    url(r'^comment_create_claim/(?P<pk>\d+)/$', login_required(CommentElectNewClaimCreate.as_view())),
    url(r'^comment_unverify/(?P<pk>\d+)/(?P<obj_pk>\d+)/$', login_required(CommentElectNewUnverify.as_view())),
]
