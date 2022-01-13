from django.conf.urls import url, include
from blog.views import *
from blog.view.comments import *


urlpatterns = [
    url(r'^news/$', BlogListView.as_view(), name="blog_list"),
    url(r'^suggested/$', SuggestedElectNews.as_view(), name="suggested_elect_news"),
    url(r'^comments/(?P<pk>\d+)/$', BlogCommentList.as_view()),

    url(r'^blog_comment/$', BlogCommentCreate.as_view()),
    url(r'^blog_reply/$', BlogReplyCreate.as_view()),
    url(r'^edit_blog_comment/(?P<pk>\d+)/$', BlogCommentEdit.as_view()),
    url(r'^delete_blog_comment/(?P<pk>\d+)/$', BlogCommentDelete.as_view()),
    url(r'^restore_blog_comment/(?P<pk>\d+)/$', BlogCommentAbortDelete.as_view()),

    url(r'^add_new_comment/$', ElectNewCommentCreate.as_view()),
    url(r'^reply_new_comment/$', ElectNewReplyCreate.as_view()),
    url(r'^edit_new_comment/(?P<pk>\d+)/$', ElectNewCommentEdit.as_view()),
    url(r'^delete_new_comment/(?P<pk>\d+)/$', ElectNewCommentDelete.as_view()),
    url(r'^restore_new_comment/(?P<pk>\d+)/$', ElectNewCommentAbortDelete.as_view()),

    url(r'^progs/', include('blog.url.progs')),
    url(r'^votes/', include('blog.url.votes')),

    url(r'^window/(?P<pk>\d+)/$', BlogWindowDetailView.as_view(), name="blog_detail_window"),
    url(r'^(?P<pk>\d+)/$', BlogDetailView.as_view(), name="blog_detail"),
]
