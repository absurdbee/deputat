from django.conf.urls import url
from users.view.settings import *


urlpatterns = [
    url(r'^$', UserProfileSettings.as_view(), name="settings_profile"),
    url(r'^notify/$', UserNotifySettings.as_view(), name="settings_notify"),
    url(r'^private/$', UserPrivateSettings.as_view(), name="settings_private"),
    url(r'^quard/$', UserQuardSettings.as_view(), name="settings_quard"),
    url(r'^about/$', UserAboutSettings.as_view(), name="settings_about"),

    url(r'^edit_password/$', UserEditPassword.as_view()),
    url(r'^edit_phone/$', UserEditPhone.as_view()),
    url(r'^create_secret_key/$', UserCreateKey.as_view()),
    url(r'^deputat_send/$', UserDeputatSend.as_view()),

    url(r'^password_recovery/$', PasswordRecovery.as_view()),
    url(r'^get_password_recovery_secret_key/$', GetPasswordRecoverySecretKey.as_view()),
    url(r'^get_password_recovery_phone/$', GetPasswordRecoveryPhone.as_view()),

    url(r'^load_include_users/$', UserPrivateIncludeUsers.as_view()),
    url(r'^load_exclude_users/$', UserPrivateExcludeUsers.as_view()),
]
