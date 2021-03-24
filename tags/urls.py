from django.conf.urls import url
from tags.views import ManagerTagsView, UserTagView, TagView


urlpatterns = [
    url(r'^$', ManagerTagsView.as_view(), name='manager_tags'),
    url(r'^tag/(?P<name>[\w\-]+)/$', UserTagView.as_view(), name="user_tag"),
    url(r'^(?P<name>[\w\-]+)/$', TagView.as_view(), name="manager_tag"),
]
