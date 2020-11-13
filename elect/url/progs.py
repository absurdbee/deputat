from django.conf.urls import url
from elect.views import *


urlpatterns = [
    url(r'^(?P<pk>\d+)/$', ElectSubscribe.as_view(), name="elect_subscribe"),
    url(r'^(?P<pk>\d+)/$', ElectUnSubscribe.as_view(), name="elect_unsubscribe"),
    url(r'^add_elect_new/(?P<pk>\d+)/$', ElectNewCreate.as_view()),
]
