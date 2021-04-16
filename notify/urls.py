from django.conf.urls import url, include
from notify.views import *

urlpatterns=[
	url(r'^$', AllNotifyView.as_view(), name='all_notify'),
	url(r'^new_notify/(?P<pk>\d+)/$', NewNotify.as_view()),
]
