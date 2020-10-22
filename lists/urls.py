from django.conf.urls import url
from lists.views import ElectLists, ElectListView


urlpatterns = [
    url(r'^elect_list/$', ElectListsView.as_view(), name='elect_list'),
    url(r'^(?P<slug>[\w\-]+)/$', ElectList.as_view(), name='elect_index'),
]
