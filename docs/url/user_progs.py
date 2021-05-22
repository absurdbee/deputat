from django.conf.urls import url
from docs.view.user_progs import *


urlpatterns = [
    url(r'^add_list/$', UserDoclistCreate.as_view()),
    url(r'^edit_list/(?P<uuid>[0-9a-f-]+)/$', UserDoclistEdit.as_view()),
    url(r'^delete_list/(?P<uuid>[0-9a-f-]+)/$', UserDoclistDelete.as_view()),
    url(r'^abort_delete_list/(?P<uuid>[0-9a-f-]+)/$', UserDoclistAbortDelete.as_view()),
    url(r'^add_list_in_collections/(?P<uuid>[0-9a-f-]+)/$', AddDocListInUserCollections.as_view()),
    url(r'^remove_list_from_collections/(?P<uuid>[0-9a-f-]+)/$', RemoveDocListFromUserCollections.as_view()),

    url(r'^create_doc/$', UserDocCreate.as_view()),
    url(r'^edit_doc/(?P<pk>\d+)/$', UserDocEdit.as_view()),
    url(r'^remove_doc/(?P<pk>\d+)/$', UserDocRemove.as_view()),
    url(r'^abort_remove_doc/(?P<pk>\d+)/$', UserDocAbortRemove.as_view()),

    url(r'^add_doc_in_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', AddDocInUserDocList.as_view()),
    url(r'^remove_doc_from_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', RemoveDocInUserDocList.as_view()),
]
