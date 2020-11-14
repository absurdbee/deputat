from django.conf.urls import url
from elect.view.progs import *


urlpatterns = [
    url(r'^subscribe/(?P<pk>\d+)/$', ElectSubscribe.as_view()),
    url(r'^unsubscribe/(?P<pk>\d+)/$', ElectUnSubscribe.as_view()),
]
