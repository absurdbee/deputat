from django.conf.urls import url
from district.views import *


urlpatterns = [
    url(r'^list/(?P<slug>[\w\-]+)/$', DistrictListView.as_view(), name="district_list"),
    url(r'^elects/(?P<slug>[\w\-]+)/$', DistrictElectDetailView.as_view(), name="district_elects"),
    url(r'^communities/(?P<slug>[\w\-]+)/$', DistrictCommunitiesDetailView.as_view(), name="district_communities"),
    url(r'^organizations/(?P<slug>[\w\-]+)/$', DistrictOrganizationsDetailView.as_view(), name="district_organizations"),
    url(r'^(?P<slug>[\w\-]+)/$', DistrictDetailView.as_view(), name="district"),
]
