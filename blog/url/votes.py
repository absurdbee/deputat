from django.conf.urls import url
from blog.view.votes import *


urlpatterns = [
    url(r'^elect_new_like/(?P<pk>\d+)/$', ElectNewLikeCreate.as_view()),
    url(r'^elect_new_dislike/(?P<pk>\d+)/$', ElectNewDislikeCreate.as_view()),

    url(r'^elect_new_comment_like/(?P<pk>\d+)/$', ElectNewCommentLikeCreate.as_view()),
    url(r'^elect_new_comment_dislike/(?P<pk>\d+)/$', ElectNewCommentDislikeCreate.as_view()),
    url(r'^elect_comment_like/(?P<pk>\d+)/$', ElectCommentLikeCreate.as_view()),
    url(r'^elect_comment_dislike/(?P<pk>\d+)/$', ElectCommentDislikeCreate.as_view()),
]
