from django.conf.urls import url, include
from managers.views import ManagersView, SuperManagersView, LoadClaims


urlpatterns = [
    url(r'^$', ManagersView.as_view(), name='managers'),
    url(r'^high_officer/$', SuperManagersView.as_view(), name='super_managers'),
    url(r'^load_claims/(?P<pk>\d+)/$', LoadClaims.as_view()),

    url(r'^progs_user/', include('managers.url.progs_user')),
    url(r'^progs_community/', include('managers.url.progs_community')),
    url(r'^progs_survey/', include('managers.url.progs_survey')),
    url(r'^progs_elect_new/', include('managers.url.elect_new')),
    url(r'^progs_photo/', include('managers.url.progs_photo')),
    url(r'^progs_video/', include('managers.url.progs_video')),
    url(r'^progs_audio/', include('managers.url.progs_audio')),
    url(r'^progs_doc/', include('managers.url.progs_doc')),
    url(r'^elect_new/', include('managers.url.elect_new')),
    url(r'^progs_blog/', include('managers.url.progs_blog')),
    url(r'^progs_organization/', include('managers.url.progs_organization')),

    url(r'^moderation_list/', include('managers.url.moderation_list')),
    url(r'^penalty_list/', include('managers.url.penalty_list')),
]
