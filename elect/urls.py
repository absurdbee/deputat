from django.conf.urls import url, include
from elect.views import *


urlpatterns = [
    url(r'^(?P<pk>\d+)/$', ElectDetailView.as_view(), name="elect_detail"),
    url(r'^(?P<pk>\d+)/new/$', ElectNewDetailView.as_view(), name="elect_new_detail"),

    url(r'^(?P<pk>\d+)/all_news/$', AllElectNewsView.as_view()),
    url(r'^(?P<pk>\d+)/statements_elect_news/$', StatementsElectNewsView.as_view()),
    url(r'^(?P<pk>\d+)/work_with_voters_elect_news/$', WorkWithVotersElectNewsView.as_view()),
    url(r'^(?P<pk>\d+)/pre_election_activities_elect_news/$', PreElectionElectNewsView.as_view()),

    url(r'^progs/', include('elect.url.progs')),
]
