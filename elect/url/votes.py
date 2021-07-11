from django.conf.urls import url
from elect.view.votes import *


urlpatterns = [
    url(r'^like/(?P<pk>\d+)/$', ElectLike.as_view()),
    url(r'^dislike/(?P<pk>\d+)/$', ElectDislike.as_view()),
    url(r'^inert/(?P<pk>\d+)/$', ElectInert.as_view()),
]
