from django.conf.urls import url
from search.views import SearchView, AllElectSearch


urlpatterns = [
    url(r'^$', SearchView.as_view(), name='search'),
    url(r'^elect_filter/', AllElectSearch.as_view()),
]
