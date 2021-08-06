from django.conf.urls import url
from city.views import *


urlpatterns = [
    url(r'^list/(?P<slug>[\w\-]+)/$', CityListView.as_view(), name="city_list"),
    url(r'^elects/(?P<slug>[\w\-]+)/$', CityElectDetailView.as_view(), name="city_elects"),
    url(r'^communities/(?P<slug>[\w\-]+)/$', CityCommunitiesDetailView.as_view(), name="city_communities"),
    url(r'^organizations/(?P<slug>[\w\-]+)/$', CityOrganizationsDetailView.as_view(), name="city_organizations"),
    url(r'^(?P<slug>[\w\-]+)/$', CityDetailView.as_view(), name="city"),
]
