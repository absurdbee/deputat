from django.conf.urls import url
from communities.view.votes import *


urlpatterns = [
    url(r'^like/(?P<pk>\d+)/$', CommunityLike.as_view()),
    url(r'^dislike/(?P<pk>\d+)/$', CommunityDislike.as_view()),
    url(r'^inert/(?P<pk>\d+)/$', CommunityInert.as_view()),
]
