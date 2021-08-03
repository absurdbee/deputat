from django.conf.urls import url
from city.views import *


urlpatterns = [
    url(r'^list/(?P<slug>[\w\-]+)/$', CityListView.as_view(), name="city_list"),
    url(r'^load_city_flat_list/$', LoadCityFlatList.as_view()),
    url(r'^(?P<slug>[\w\-]+)/$', CityDetailView.as_view(), name="city"),
]
