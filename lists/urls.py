from django.conf.urls import url
from lists.views import *


urlpatterns = [
    url(r'^elect_list/$', ElectListsView.as_view(), name='elect_list'),

    url(r'^(?P<slug>[\w\-]+)/$', AuthorityListView.as_view(), name='authority_index'),
    url(r'^fraction/(?P<slug>[\w\-]+)/$', FractionList.as_view(), name='fraction_index'),
    url(r'^region/(?P<slug>[\w\-]+)/$', RegionElectView.as_view(), name='region_index'),

    url(r'^area/(?P<slug>[\w\-]+)/$', RegionDetailView.as_view(), name='region_detail'),
]
