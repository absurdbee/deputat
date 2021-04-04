from django.conf.urls import url, include
from docs.views import DocsView, UserLoadDoclist, UserDocsList


urlpatterns = [
    url(r'^$', DocsView.as_view(), name='docs'),
    url(r'^load/(?P<pk>\d+)/$', UserLoadDoclist.as_view()),
    url(r'^doc_list/(?P<pk>\d+)/$', UserDocsList.as_view(), name='user_docs_list'),

    url(r'^user_progs/', include('docs.url.user_progs')),
]
