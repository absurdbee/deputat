from django.conf.urls import url
from lists.views import *


urlpatterns = [
    url(r'^elect_list/$', ElectListsView.as_view(), name='elect_list'),

    url(r'^(?P<slug>[\w\-]+)/$', AuthorityList.as_view(), name='authority_index'),
    url(r'^(?P<fraction>[\w\-]+)/$', FractionList.as_view(), name='fraction_index'),
]
