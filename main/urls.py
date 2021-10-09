from django.conf.urls import url
from main.views import *


urlpatterns = [
	url(r'^$', MainPageView.as_view(), name="main"),
	url(r'^main_region/(?P<uuid>[0-9a-f-]+)/$', MainRegionView.as_view()),
	url(r'^main_map/$', MainMapView.as_view()),
	url(r'^main_stat/$', MainStatView.as_view()),
	url(r'^main_media/$', MainMediaView.as_view()),
	url(r'^my_news/$', MyNewsView.as_view()),
	url(r'^draft_news/$', DraftNewsView.as_view()),
]
