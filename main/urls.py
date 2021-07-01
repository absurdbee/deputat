from django.conf.urls import url
from main.views import *


urlpatterns = [
	url(r'^$', MainPageView.as_view(), name="main"),
	url(r'^main_region/(?P<slug>[\w\-]+)/$', MainRegionView.as_view()),
	url(r'^main_map/$', MainMapView.as_view()),
	url(r'^main_stat/$', MainStatView.as_view()),
	url(r'^main_docs/$', MainDocsView.as_view()),
	url(r'^my_news/$', MyNewsView.as_view()),
	url(r'^draft_news/$', DraftNewsView.as_view()), 
]
