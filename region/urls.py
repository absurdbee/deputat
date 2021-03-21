from django.conf.urls import url
from region.views import *


urlpatterns = [
    url(r'^region/(?P<slug>[\w\-]+)/$', RegionElectView.as_view(), name='region_index'),
    url(r'^area/(?P<slug>[\w\-]+)/$', RegionDetailView.as_view(), name='region_detail'),
]
