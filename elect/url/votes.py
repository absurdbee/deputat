from django.conf.urls import url
from elect.view.votes import *


urlpatterns = [
    url(r'^blog_like/(?P<pk>\d+)/$', BlogLikeCreate.as_view()),
    url(r'^blog_dislike/(?P<pk>\d+)/$', BlogDislikeCreate.as_view()),

    url(r'^blog_comment_like/(?P<pk>\d+)/$', BlogCommentLikeCreate.as_view()),
    url(r'^blog_comment_dislike/(?P<pk>\d+)/$', BlogCommentDislikeCreate.as_view()),
]
