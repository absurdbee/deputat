from django.conf.urls import url
from users.views import *


urlpatterns = [
    url(r'^(?P<pk>\d+)/$', UserView.as_view(), name='user'),
    url(r'^user_news/(?P<pk>\d+)/$', UserNewsView.as_view(), name='user_news'),
    url(r'^subscribe_elects/(?P<pk>\d+)/$', SubscribeElectsView.as_view(), name='subscribe_elects'),
    url(r'^like_news/(?P<pk>\d+)/$', LikeNewsView.as_view(), name='like_news'),
    url(r'^dislike_news/(?P<pk>\d+)/$', DislikeNewsView.as_view(), name='dislike_news'),
    url(r'^edit/$', UserEditView.as_view()),
    url(r'^edit_password/$', UserEditPassword.as_view()),
    url(r'^phone_verify/$', MainPhoneSend.as_view(), name="phone_send"),
]
