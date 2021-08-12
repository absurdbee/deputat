from organizations.views import *
from django.conf.urls import url


urlpatterns=[
	url(r'^$', AllOrganizationsList.as_view(), name="all_organizations"),
	url(r'^suggest_organization/$', SuggestOrganizationView.as_view()),
]
