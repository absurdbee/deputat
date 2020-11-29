from django.conf.urls import url
from blog.view.progs import *


urlpatterns = [
    url(r'^add_elect_new/(?P<pk>\d+)/$', ElectNewCreate.as_view()),
    url(r'^elect_like/(?P<pk>\d+)/$', ElectLikeCreate.as_view()),
    url(r'^elect_dislike/(?P<pk>\d+)/$', ElectDislikeCreate.as_view()),
    url(r'^blog_like/(?P<pk>\d+)/$', BlogLikeCreate.as_view()),
    url(r'^blog_dislike/(?P<pk>\d+)/$', BlogDislikeCreate.as_view()),
]
