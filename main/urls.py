from django.conf.urls import url
from main.views import *


urlpatterns = [
	url(r'^$', MainPageView.as_view(), name="main"),
	url(r'^phone_verify/$', MainPhoneSend.as_view(), name="phone_send"),
	url(r'^phone_send/(?P<phone>\d+)/$', PhoneSend.as_view()),
    url(r'^phone_verify/(?P<phone>\d+)/(?P<code>\d+)/$', PhoneVerify.as_view()),
]
