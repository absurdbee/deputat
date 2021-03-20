from django.conf.urls import url
from main.views import *


urlpatterns = [
	url(r'^$', MainPageView.as_view(), name="main"),
	url(r'^my_news/$', MyNewsView.as_view(), name="my_news"),
	url(r'^draft_news/$', DraftNewsView.as_view(), name="draft_news"),
	url(r'^phone_send/(?P<phone>\d+)/$', PhoneSend.as_view()),
    url(r'^phone_verify/(?P<phone>\d+)/(?P<code>\d+)/$', PhoneVerify.as_view()),
]
