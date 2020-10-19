from django.conf.urls import url
from blog_cat.views import BlogListView, BlogLists


urlpatterns = [
    url(r'^$', BlogLists.as_view(), name='blog_list'),
    url(r'^(?P<slug>[\w\-]+)/$', BlogListView.as_view(), name='blog_index'),
]
