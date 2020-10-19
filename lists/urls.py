from django.conf.urls import url
from lists.views import ElectLists, ElectListView


urlpatterns = [
    url(r'^elect_list/$', ElectLists.as_view(), name='elect_list'),
    url(r'^(?P<slug>[\w\-]+)/$', ElectListView.as_view(), name='elect_index'),
]
