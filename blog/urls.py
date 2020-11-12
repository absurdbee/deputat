from django.conf.urls import url
from blog.views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^(?P<pk>\d+)/$', BlogDetailView.as_view(), name="blog_detail"),
    url(r'^all_elect_news/$', AllElectNewsView.as_view(), name="all_elect_news"),
    url(r'^news/$', ProectNewsView.as_view(), name="proect_news"),

    url(r'^like/(?P<pk>\d+)/$',login_required(BlogLikeCreate.as_view())),
    url(r'^dislike/(?P<pk>\d+)/$',login_required(BlogDislikeCreate.as_view())),
    url(r'^comment_like/(?P<comment_pk>\d+)/$',login_required(BlogCommentLikeCreate.as_view())),
    url(r'^comment_dislike/(?P<comment_pk>\d+)/$',login_required(BlogCommentDislikeCreate.as_view())),

    url(r'^post-comment/$', login_required(BlogCommentCreate.as_view())),
    url(r'^reply-comment/$', login_required(BlogReplyCreate.as_view())),
    url(r'^delete_comment/(?P<pk>\d+)/$', login_required(BlogCommentDelete.as_view())),
    url(r'^abort_delete_comment/(?P<pk>\d+)/$', login_required(BlogCommentAbortDelete.as_view())),
    url(r'^comment/(?P<pk>\d+)/$', BlogCommentList.as_view()),
]
