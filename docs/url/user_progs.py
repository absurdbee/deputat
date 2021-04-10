from django.conf.urls import url
from docs.view.user_progs import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^add_list/$', UserDoclistCreate.as_view()),
    url(r'^edit_list/(?P<uuid>[0-9a-f-]+)/$', UserDoclistEdit.as_view()),
    url(r'^delete_list/(?P<uuid>[0-9a-f-]+)/$', UserDoclistDelete.as_view()),
    url(r'^abort_delete_list/(?P<uuid>[0-9a-f-]+)/$', UserDoclistAbortDelete.as_view()),
    url(r'^add_list/(?P<uuid>[0-9a-f-]+)/$', UserDoclistAdd.as_view()),
    url(r'^remove_list/(?P<uuid>[0-9a-f-]+)/$', UserDoclistRemove.as_view()),

    url(r'^create_doc/$', UserDocCreate.as_view()),
    url(r'^edit_doc/(?P<pk>\d+)/$', UserDocEdit.as_view()),

    url(r'^u_add_doc/(?P<uuid>[0-9a-f-]+)/$', login_required(UserDocAdd.as_view())),
    url(r'^u_remove_doc/(?P<pk>\d+)/$', login_required(UserDocRemove.as_view())),
    url(r'^add_doc_in_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', login_required(UserDocListAdd.as_view())),
    url(r'^remove_doc_in_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', login_required(UserDocListRemove.as_view())),
]
