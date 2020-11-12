from django.conf.urls import url
from elect.views import *


urlpatterns = [
    url(r'^(?P<pk>\d+)/$', ElectDetailView.as_view(), name="elect_detail"),
    url(r'^(?P<pk>\d+)/new/$', ElectNewDetailView.as_view(), name="elect_new_detail"),
    url(r'^(?P<pk>\d+)/events/$', ElectNewsView.as_view(), name="elect_news"),
]
