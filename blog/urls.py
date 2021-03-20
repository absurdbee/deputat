from django.conf.urls import url, include
from blog.views import *
from blog.view.comments import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^news/$', ProectNewsView.as_view(), name="proect_news"),
    url(r'^all_elects_news/(?P<name>[\w\-]+)/$', AllElectsNewsView.as_view(), name="all_elect_news"),
    url(r'^comments/(?P<pk>\d+)/$', BlogCommentList.as_view()),

    url(r'^add_blog_comment/$', login_required(BlogCommentCreate.as_view())),
    url(r'^reply_blog_comment/$', login_required(BlogReplyCreate.as_view())),
    url(r'^delete_blog_comment/(?P<pk>\d+)/$', login_required(BlogCommentDelete.as_view())),
    url(r'^abort_delete_blog_comment/(?P<pk>\d+)/$', login_required(BlogCommentAbortDelete.as_view())),

    url(r'^add_new_comment/$', login_required(ElectNewCommentCreate.as_view())),
    url(r'^reply_new_comment/$', login_required(ElectNewReplyCreate.as_view())),
    url(r'^delete_new_comment/(?P<pk>\d+)/$', login_required(ElectNewCommentDelete.as_view())),
    url(r'^abort_delete_new_comment/(?P<pk>\d+)/$', login_required(ElectNewCommentAbortDelete.as_view())),

    url(r'^progs/', include('blog.url.progs')),
    url(r'^votes/', include('blog.url.votes')),

    url(r'^(?P<pk>\d+)/$', BlogDetailView.as_view(), name="blog_detail"),
]
