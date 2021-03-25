from django.conf.urls import url
from main.views import *


urlpatterns = [
	url(r'', MainPageView.as_view(), name="main"),
	url(r'^region/(?P<slug>[\w\-]+)/$', MainRegionView.as_view()),
	url(r'^main_map/$', MainMapView.as_view()),
	url(r'^main_stat/$', MainStatView.as_view()),
	url(r'^main_docs/$', MainDocsView.as_view()),
	url(r'^my_news/$', MyNewsView.as_view()),
	url(r'^draft_news/$', DraftNewsView.as_view()),
	url(r'^phone_send/(?P<phone>\d+)/$', PhoneSend.as_view()),
    url(r'^phone_verify/(?P<phone>\d+)/(?P<code>\d+)/$', PhoneVerify.as_view()),
]
