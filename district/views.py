from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from district.models import District2
from django.views.generic import ListView
from common.templates import get_full_template


class DistrictListView(ListView, CategoryListMixin):
	template_name, paginate_by = None, 12

	def get(self,request,*args,**kwargs):
		from region.models import Region

		self.region = Region.objects.get(slug=self.kwargs["slug"])
		self.template_name = get_full_template("district/", "district_list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(DistrictListView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		return Blog.objects.filter(category=self.cat)

	def get_context_data(self, **kwargs):
		context = super(DistrictListView, self).get_context_data(**kwargs)
		context['region'] = self.region
		return context


class DistrictDetailView(TemplateView, CategoryListMixin):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.district = District2.objects.get(slug=self.kwargs["slug"])
		self.template_name = get_full_template("district/", "district.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(DistrictDetailView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(DistrictDetailView,self).get_context_data(**kwargs)
		context["object"] = self.district
		return context

class DistrictElectDetailView(TemplateView, CategoryListMixin):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.district = District2.objects.get(slug=self.kwargs["slug"])
		self.template_name = get_full_template("district/", "district_elects.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(DistrictElectDetailView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(DistrictElectDetailView,self).get_context_data(**kwargs)
		context["object"] = self.district
		return context


class DistrictCommunitiesDetailView(TemplateView, CategoryListMixin):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.district = District2.objects.get(slug=self.kwargs["slug"])
		self.template_name = get_full_template("district/", "district_communities.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(DistrictCommunitiesDetailView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(DistrictCommunitiesDetailView,self).get_context_data(**kwargs)
		context["object"] = self.district
		return context


class DistrictOrganizationsDetailView(TemplateView, CategoryListMixin):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.district = District2.objects.get(slug=self.kwargs["slug"])
		self.template_name = get_full_template("district/", "district_organizations.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(DistrictOrganizationsDetailView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(DistrictOrganizationsDetailView,self).get_context_data(**kwargs)
		context["object"] = self.district
		return context
