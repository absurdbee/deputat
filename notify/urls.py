from django.conf.urls import url, include
from notify.views import *

urlpatterns=[
	url(r'^$', AllNotifyView.as_view(), name='all_notify'),
	url(r'^recent/$', RecentNotifyView.as_view()),
	url(r'^all_read/$', AllReadNotifyView.as_view()),
	url(r'^new_wall/(?P<pk>\d+)/$', NewWall.as_view()),
]
