from django.conf.urls import url
from users.view.progs import *


urlpatterns = [
    url(r'^phone_send/(?P<phone>\d+)/$', PhoneSend.as_view()),
    url(r'^phone_verify/(?P<phone>\d+)/(?P<code>\d+)/$', PhoneVerify.as_view()),
    url(r'^change_phone_send/(?P<phone>\d+)/$', ChangePhoneSend.as_view()),
    url(r'^change_phone_verify/(?P<phone>\d+)/(?P<code>\d+)/$', ChangePhoneVerify.as_view()),

    url(r'^recovery_phone_send/(?P<phone>\d+)/$', RecoveryPhoneSend.as_view()),
    url(r'^secret_key_verify/(?P<pk>\d+)/$', SecretKeyVerify.as_view()),
]
