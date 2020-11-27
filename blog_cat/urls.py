from django.conf.urls import url
from blog_cat.views import BlogListView


urlpatterns = [
    url(r'^$', BlogListView.as_view(), name='blog_list'),
]
