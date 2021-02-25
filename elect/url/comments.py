from django.conf.urls import url
from elect.comments.views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^add_elect_comment/$', login_required(ElectCommentCreate.as_view())),
    url(r'^reply_elect_comment/$', login_required(ElectReplyCreate.as_view())),
    url(r'^delete_elect_comment/(?P<pk>\d+)/$', login_required(ElectCommentDelete.as_view())),
    url(r'^abort_delete_elect_comment/(?P<pk>\d+)/$', login_required(ElectCommentAbortDelete.as_view()))
]
