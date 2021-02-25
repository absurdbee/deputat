from django.conf.urls import url
from blog.view.progs import *


urlpatterns = [
    url(r'^add_elect_new/(?P<pk>\d+)/$', ElectNewCreate.as_view()),
    url(r'^elect_new_like/(?P<pk>\d+)/$', ElectNewLikeCreate.as_view()),
    url(r'^elect_new_dislike/(?P<pk>\d+)/$', ElectNewDislikeCreate.as_view()),
    url(r'^blog_like/(?P<pk>\d+)/$', BlogLikeCreate.as_view()),
    url(r'^blog_dislike/(?P<pk>\d+)/$', BlogDislikeCreate.as_view()),

    url(r'^elect_new_comment_like/(?P<pk>\d+)/$', ElectNewCommentLikeCreate.as_view()),
    url(r'^elect_new_comment_dislike/(?P<pk>\d+)/$', ElectNewCommentDislikeCreate.as_view()),
    url(r'^elect_comment_like/(?P<pk>\d+)/$', ElectCommentLikeCreate.as_view()),
    url(r'^elect_comment_dislike/(?P<pk>\d+)/$', ElectCommentDislikeCreate.as_view()),
    url(r'^blog_comment_like/(?P<pk>\d+)/$', BlogCommentLikeCreate.as_view()),
    url(r'^blog_comment_dislike/(?P<pk>\d+)/$', BlogCommentDislikeCreate.as_view()),
]
