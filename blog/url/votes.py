from django.conf.urls import url
from blog.view.votes import *


urlpatterns = [
    url(r'^elect_new_like/(?P<pk>\d+)/$', ElectNewLike.as_view()),
    url(r'^elect_new_dislike/(?P<pk>\d+)/$', ElectNewDislike.as_view()),
    url(r'^blog_like/(?P<pk>\d+)/$', BlogLike.as_view()),
    url(r'^blog_dislike/(?P<pk>\d+)/$', BlogDislike.as_view()),
    url(r'^blog_inert/(?P<pk>\d+)/$', BlogInert.as_view()),

    url(r'^elect_new_comment_like/(?P<pk>\d+)/$', ElectNewCommentLike.as_view()),
    url(r'^blog_comment_like/(?P<pk>\d+)/$', BlogCommentLike.as_view()),
]
