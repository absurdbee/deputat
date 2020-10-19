from django.conf.urls import url
from users.views import UserView, UserSettings


urlpatterns = [
    url(r'^(?P<pk>\d+)/$', UserView.as_view(), name='user'),
    url(r'^settings/(?P<pk>\d+)/$', UserSettings.as_view(), name='user_settings'),
]
