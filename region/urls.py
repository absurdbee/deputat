from django.conf.urls import url
from region.views import *


urlpatterns = [
    url(r'^(?P<slug>[\w\-]+)/$', RegionDetailView.as_view(), name='region_detail'),
    url(r'^(?P<slug>[\w\-]+)/$', RegionElectView.as_view(), name='region_index'),
    url(r'^elects/(?P<slug>[\w\-]+)/$', RegionElectDetailView.as_view(), name="region_elects"),
    url(r'^communities/(?P<slug>[\w\-]+)/$', RegionCommunitiesDetailView.as_view(), name="region_communities"),
    url(r'^organizations/(?P<slug>[\w\-]+)/$', RegionOrganizationsDetailView.as_view(), name="region_organizations"),

    url(r'^cities/(?P<pk>\d+)/$', LoadCitiesView.as_view()),
    url(r'^settings_cities/(?P<pk>\d+)/$', LoadSettingsDistrictsView.as_view()),
    url(r'^load_left_menu_regions/$', LoadLeftMenuRegions.as_view()),
    url(r'^load_left_menu_regions_select/$', LoadLeftMenuRegionsSelect.as_view()),
    url(r'^load_left_menu_region_get_districts/(?P<slug>[\w\-]+)/$', LoadLeftMenuRegionDistricts.as_view()),
    url(r'^load_districts_for_multiple_form/(?P<pk>\d+)/$', LoadDistrictsMultipleForm.as_view()),
    url(r'^load_region_for_select_regional_elects/$', LoadRegionForSelectRegionalElects.as_view()),
    url(r'^load_region_for_select_regional_elects/$', LoadRegionForSelectRegionalElects.as_view()),
]
