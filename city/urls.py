from django.conf.urls import url
from city.views import *


urlpatterns = [
    url(r'^(?P<slug>[\w\-]+)/$', CityDetailView.as_view(), name='city_detail'),
]
