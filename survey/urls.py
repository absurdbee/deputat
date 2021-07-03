from django.conf.urls import url, include
from survey.views import *


urlpatterns = [
    url(r'^$', SurveyView.as_view(), name='survey'),
    url(r'^user_load/(?P<pk>\d+)/$', UserLoadSurveylist.as_view()),
    url(r'^penalty_load/(?P<pk>\d+)/$', UserLoadPenaltySurveyList.as_view()),
    url(r'^moderated_load/(?P<pk>\d+)/$', UserLoadModeratedSurveyList.as_view()),
    url(r'^user_survey/(?P<pk>\d+)/$', UserSurvey.as_view(), name='user_survey'),
    url(r'^user_list/(?P<uuid>[0-9a-f-]+)/$', UserSurveyList.as_view(), name='user_survey_list'),
    url(r'^survey_detail/(?P<pk>\d+)/$', UserSurveyDetail.as_view()),

    url(r'^user_progs/', include('survey.url.user_progs')),
]
