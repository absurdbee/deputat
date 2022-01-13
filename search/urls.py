from django.conf.urls import url
from search.views import *


urlpatterns = [
    url(r'^$', SearchView.as_view(), name='search'),
    url(r'^elect_filter/', AllElectSearch.as_view()),
    url(r'^elect_add_elect_new_filter/', ElectAddElectNewSearch.as_view()),
    url(r'^elect_add_blog_filter/', ElectAddBlogSearch.as_view()),
    url(r'^tags_filter/(?P<pk>\d+)/', TagsSearch.as_view()),
]
