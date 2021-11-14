from django.conf.urls import url
from terms.views import *


urlpatterns = [
    url(r'^(?P<pk>\d+)/$', TermsView.as_view(), name='terms'),
    url(r'^window_about/$', WindowAboutView.as_view(), name='window_about'),
]
