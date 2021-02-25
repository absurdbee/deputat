from django.conf.urls import url, include
from blog.views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^(?P<pk>\d+)/$', BlogDetailView.as_view(), name="blog_detail"),
    url(r'^news/$', ProectNewsView.as_view(), name="proect_news"),
    url(r'^all_elects_news/(?P<name>[\w\-]+)/$', AllElectsNewsView.as_view(), name="all_elect_news"),

    url(r'^post-comment/$', login_required(BlogCommentCreate.as_view())),
    url(r'^reply-comment/$', login_required(BlogReplyCreate.as_view())),
    url(r'^delete_comment/(?P<pk>\d+)/$', login_required(BlogCommentDelete.as_view())),
    url(r'^abort_delete_comment/(?P<pk>\d+)/$', login_required(BlogCommentAbortDelete.as_view())),
    url(r'^comments/(?P<pk>\d+)/$', BlogCommentList.as_view()),

    url(r'^progs/', include('blog.url.progs')),
    url(r'^votes/', include('votes.url.progs')),
    url(r'^comments/', include('blog.url.comments')),
]
