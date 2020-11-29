from django.conf.urls import url
from blog.view.progs import *


urlpatterns = [
    url(r'^add_elect_new/(?P<pk>\d+)/$', ElectNewCreate.as_view()),
    url(r'^elect_like/(?P<pk>\d+)/$',login_required(ElectLikeCreate.as_view())),
    url(r'^elect_dislike/(?P<pk>\d+)/$',login_required(ElectDislikeCreate.as_view())),
    url(r'^blog_like/(?P<pk>\d+)/$',login_required(BlogLikeCreate.as_view())),
    url(r'^blog_dislike/(?P<pk>\d+)/$',login_required(BlogDislikeCreate.as_view())),

]
