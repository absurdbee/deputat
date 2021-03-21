from django.conf.urls import url
from city.views import *


urlpatterns = [
    url(r'^list/(?P<slug>[\w\-]+)/$', CitylistView.as_view(), name="city_list"),
    url(r'^(?P<slug>[\w\-]+)/$', CityDetailView.as_view(), name="city")
]
