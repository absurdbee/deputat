from django.conf.urls import url
from users.view.progs import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^phone_send/(?P<phone>\d+)/$', login_required(PhoneSend.as_view())),
    url(r'^phone_verify/(?P<phone>\d+)/(?P<code>\d+)/$', login_required(PhoneVerify.as_view())),
]
