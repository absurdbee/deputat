from django.conf.urls import url
from region.views import *


urlpatterns = [
    url(r'^region/(?P<slug>[\w\-]+)/$', RegionElectView.as_view(), name='region_index'),
    url(r'^area/(?P<slug>[\w\-]+)/$', RegionDetailView.as_view(), name='region_detail'),
    url(r'^cities/(?P<pk>\d+)/$', LoadCitiesView.as_view()),
    url(r'^load_left_menu_regions/$', LoadLeftMenuRegions.as_view()),
    url(r'^load_left_menu_regions_select/$', LoadLeftMenuRegionsSelect.as_view()),
    url(r'^load_left_menu_region_get_cities/(?P<pk>\d+)/$', LoadLeftMenuRegionCities.as_view()),
]
