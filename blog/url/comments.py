from django.conf.urls import url
from blog.comments.views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^add_blog_comment/$', login_required(BlogCommentCreate.as_view())),
    url(r'^reply_blog_comment/$', login_required(BlogReplyCreate.as_view())),
    url(r'^delete_blog_comment/(?P<pk>\d+)/$', login_required(BlogCommentDelete.as_view())),
    url(r'^abort_delete_blog_comment/(?P<pk>\d+)/$', login_required(BlogCommentAbortDelete.as_view())),

    url(r'^add_new_comment/$', login_required(ElectNewCommentCreate.as_view())),
    url(r'^reply_new_comment/$', login_required(ElectNewReplyCreate.as_view())),
    url(r'^delete_new_comment/(?P<pk>\d+)/$', login_required(ElectNewCommentDelete.as_view())),
    url(r'^abort_delete_new_comment/(?P<pk>\d+)/$', login_required(ElectNewCommentAbortDelete.as_view())),
]
