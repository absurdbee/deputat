from django.conf.urls import url
from managers.view.survey import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^add_admin/(?P<pk>\d+)/$', login_required(SurveyAdminCreate.as_view())),
    url(r'^delete_admin/(?P<pk>\d+)/$', login_required(SurveyAdminDelete.as_view())),
    url(r'^add_moderator/(?P<pk>\d+)/$', login_required(SurveyModerCreate.as_view())),
    url(r'^delete_moderator/(?P<pk>\d+)/$', login_required(SurveyModerDelete.as_view())),
    url(r'^add_editor/(?P<pk>\d+)/$', login_required(SurveyEditorCreate.as_view())),
    url(r'^delete_editor/(?P<pk>\d+)/$', login_required(SurveyEditorDelete.as_view())),

    url(r'^add_worker_admin/(?P<pk>\d+)/$', login_required(SurveyWorkerAdminCreate.as_view())),
    url(r'^delete_worker_admin/(?P<pk>\d+)/$', login_required(SurveyWorkerAdminDelete.as_view())),
    url(r'^add_worker_moderator/(?P<pk>\d+)/$', login_required(SurveyWorkerModerCreate.as_view())),
    url(r'^delete_worker_moderator/(?P<pk>\d+)/$', login_required(SurveyWorkerModerDelete.as_view())),
    url(r'^add_worker_editor/(?P<pk>\d+)/$', login_required(SurveyWorkerEditorCreate.as_view())),
    url(r'^delete_worker_editor/(?P<pk>\d+)/$', login_required(SurveyWorkerEditorDelete.as_view())),

    url(r'^create_close/(?P<uuid>[0-9a-f-]+)/$', login_required(SurveyCloseCreate.as_view())),
    url(r'^delete_close/(?P<pk>\d+)/$', login_required(SurveyCloseDelete.as_view())),
    url(r'^create_rejected/(?P<pk>\d+)/$', login_required(SurveyRejectedCreate.as_view())),
    url(r'^create_claim/(?P<pk>\d+)/$', login_required(SurveyClaimCreate.as_view())),
    url(r'^unverify/(?P<pk>\d+)/(?P<obj_pk>\d+)/$', login_required(SurveyUnverify.as_view())),
]
