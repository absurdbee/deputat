from django.conf.urls import url
from users.view.settings import *


urlpatterns = [
    url(r'^$', UserProfileSettings.as_view()),
    url(r'^notify/$', UserNotifySettings.as_view()),
    url(r'^private/$', UserPrivateSettings.as_view()),
    url(r'^quard/$', UserQuardSettings.as_view()),
]
