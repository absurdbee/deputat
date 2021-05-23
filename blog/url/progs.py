from django.conf.urls import url
from blog.view.progs import *


urlpatterns = [
    url(r'^suggest_elect_new/$', SuggestElectNew.as_view()),
    url(r'^publish_elect_new/(?P<pk>\d+)/$', PublishElectNew.as_view()),
]
