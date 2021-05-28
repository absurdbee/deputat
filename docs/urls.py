from django.conf.urls import url, include
from docs.views import *


urlpatterns = [
    url(r'^$', DocsView.as_view(), name='docs'),
    url(r'^user_load/(?P<pk>\d+)/$', UserLoadDoclist.as_view()),
    url(r'^penalty_load/(?P<pk>\d+)/$', UserLoadPenaltyDoclist.as_view()),
    url(r'^moderated_load/(?P<pk>\d+)/$', UserLoadModeratedDoclist.as_view()),
    url(r'^user_docs/(?P<pk>\d+)/$', UserDocs.as_view(), name='user_docs'),
    url(r'^user_list/(?P<uuid>[0-9a-f-]+)/$', UserDocsList.as_view(), name='user_docs_list'),

    url(r'^user_progs/', include('docs.url.user_progs')),
]
