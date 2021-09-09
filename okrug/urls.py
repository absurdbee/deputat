from django.conf.urls import url
from okrug.views import *


urlpatterns = [
    url(r'^list/(?P<slug>[\w\-]+)/$', OkrugListView.as_view(), name="okrug_list"),
    url(r'^elects/(?P<slug>[\w\-]+)/$', OkrugElectDetailView.as_view(), name="okrug_elects"),
    url(r'^(?P<slug>[\w\-]+)/$', OkrugDetailView.as_view(), name="okrug"),
]
