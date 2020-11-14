from django.conf.urls import url
from blog.view.progs import *


urlpatterns = [
    url(r'^add_elect_new/(?P<pk>\d+)/$', ElectNewCreate.as_view()),
]
