from django.conf.urls import url
from users.view.settings import *


urlpatterns = [
    url(r'^$', UserProfileSettings.as_view(), name="settings_profile"),
    url(r'^notify/$', UserNotifySettings.as_view(), name="settings_notify"),
    url(r'^private/$', UserPrivateSettings.as_view(), name="settings_private"),
    url(r'^quard/$', UserQuardSettings.as_view(), name="settings_quard"),
    url(r'^about/$', UserAboutSettings.as_view(), name="settings_about"),
]
