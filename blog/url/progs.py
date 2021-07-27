from django.conf.urls import url
from blog.view.progs import *


urlpatterns = [
    url(r'^add_blog/$', BlogCreateView.as_view()),
    url(r'^edit_blog/(?P<pk>\d+)/$', BlogEditView.as_view()),
    url(r'^suggest_elect_new/$', SuggestElectNew.as_view()),
    url(r'^edit_elect_new/(?P<pk>\d+)/$', EditElectNew.as_view()),
    url(r'^edit_manager_elect_new/(?P<pk>\d+)/$', EditManagerElectNew.as_view()),

    url(r'^delete_elect_new/(?P<pk>\d+)/$', DeleteElectNew.as_view()),
    url(r'^restore_elect_new/(?P<pk>\d+)/$', RestoreElectNew.as_view()),
    url(r'^delete_blog/(?P<pk>\d+)/$', DeleteBlog.as_view()),
    url(r'^restore_blog/(?P<pk>\d+)/$', RestoreBlog.as_view()),

    url(r'^add_repost_count_blog_vk/(?P<pk>\d+)/$', BlogAddRepostCountVk.as_view()),
    url(r'^add_repost_count_blog_fb/(?P<pk>\d+)/$', BlogAddRepostCountFb.as_view()),
    url(r'^add_repost_count_blog_tg/(?P<pk>\d+)/$', BlogAddRepostCountTg.as_view()),
    url(r'^add_repost_count_blog_tw/(?P<pk>\d+)/$', BlogAddRepostCountTw.as_view()),

    url(r'^add_repost_count_elect_new_vk/(?P<pk>\d+)/$', ElectNewAddRepostCountVk.as_view()),
    url(r'^add_repost_count_elect_new_fb/(?P<pk>\d+)/$', ElectNewAddRepostCountFb.as_view()),
    url(r'^add_repost_count_elect_new_tg/(?P<pk>\d+)/$', ElectNewAddRepostCountTg.as_view()),
    url(r'^add_repost_count_elect_new_tw/(?P<pk>\d+)/$', ElectNewAddRepostCountTw.as_view()),
]
