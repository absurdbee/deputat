from django.conf.urls import url
from elect.view.votes import *


urlpatterns = [
    url(r'^elect_comment_like/(?P<pk>\d+)/$', ElectCommentLikeCreate.as_view()),
]
