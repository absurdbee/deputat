from django.conf.urls import url
from lists.views import *


urlpatterns = [
    url(r'^elect_list/$', ElectListsView.as_view(), name='elect_list'),
    url(r'^(?P<slug>[\w\-]+)/$', ElectsList.as_view(), name='elect_index'),
]
