from django.conf.urls import url, include
from survey.views import *


urlpatterns = [
    url(r'^$', SurveyView.as_view(), name='survey'),
    url(r'^load/(?P<pk>\d+)/$', UserLoadSurveylist.as_view()),
    url(r'^user_survey/(?P<pk>\d+)/$', UserSurvey.as_view(), name='user_survey'),
    url(r'^list/(?P<uuid>[0-9a-f-]+)/$', UserSurveysList.as_view(), name='user_survey_list'),
    url(r'^user_progs/', include('survey.url.user_progs')),
]
