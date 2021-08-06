from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from organizations.models import Organization
from django.views.generic import ListView
from common.templates import get_full_template


class AllOrganizationsList(ListView, CategoryListMixin):
	template_name, paginate_by = None, 12

	def get(self,request,*args,**kwargs):
		self.template_name = get_full_template("organizations/", "all.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(CityListView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		return Organization.objects.only("pk")
