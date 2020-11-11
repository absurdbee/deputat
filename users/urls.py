from django.conf.urls import url
from users.views import *


urlpatterns = [
    url(r'^user_news/$', UserNewsView.as_view(), name='user_news'),
    url(r'^subscribe_elects/$', SubscribeElectsView.as_view(), name='subscribe_elects'),
    url(r'^like_news/$', LikeNewsView.as_view(), name='like_news'),
    url(r'^dislike_news/$', DislikeNewsView.as_view(), name='dislike_news'),
]
