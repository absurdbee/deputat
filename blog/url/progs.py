from django.conf.urls import url
from blog.view.progs import *


urlpatterns = [
    url(r'^subscribe/(?P<pk>\d+)/$', ElectSubscribe.as_view(), name="elect_subscribe"),
    url(r'^unsubscribe(?P<pk>\d+)/$', ElectUnSubscribe.as_view(), name="elect_unsubscribe"),
    url(r'^add_elect_new/(?P<pk>\d+)/$', ElectNewCreate.as_view()),
]
