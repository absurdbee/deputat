from region.models import Region
from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from common.templates import get_full_template


class RegionElectView(TemplateView, CategoryListMixin):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.region = Region.objects.get(slug=self.kwargs["slug"])
		self.template_name = get_full_template("elect_list/", "region_list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(RegionElectView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(RegionElectView,self).get_context_data(**kwargs)
		context["region"] = self.region
		return context

class LoadCitiesView(TemplateView):
	template_name = "city/get_region_cities.html"

	def get(self,request,*args,**kwargs):
		from city.models import City
		from district.models import District

		self.cities = City.objects.filter(region__pk=self.kwargs["pk"])
		self.districts = District.objects.filter(region__pk=self.kwargs["pk"])
		return super(LoadCitiesView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(LoadCitiesView,self).get_context_data(**kwargs)
		context["cities"] = self.cities
		context["districts"] = self.districts
		return context

class LoadLeftMenuRegions(TemplateView):
	template_name = "region/load_left_menu_regions.html"

	def get(self,request,*args,**kwargs):
		from region.models import Region

		self.regions = Region.objects.only("pk")
		return super(LoadLeftMenuRegions,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(LoadLeftMenuRegions,self).get_context_data(**kwargs)
		context["regions"] = self.regions
		return context

class LoadLeftMenuRegionsSelect(TemplateView):
	template_name = "region/load_left_menu_regions_select.html"

	def get(self,request,*args,**kwargs):
		from region.models import Region

		self.regions = Region.objects.only("pk")
		return super(LoadLeftMenuRegionsSelect,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(LoadLeftMenuRegionsSelect,self).get_context_data(**kwargs)
		context["regions"] = self.regions
		return context

class LoadLeftMenuRegionCities(TemplateView):
	template_name = "region/load_left_menu_region_cities.html"

	def get(self,request,*args,**kwargs):
		from region.models import Region

		self.region = Region.objects.get(slug=self.kwargs["slug"])
		return super(LoadLeftMenuRegionCities,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(LoadLeftMenuRegionCities,self).get_context_data(**kwargs)
		context["cities"] = self.region.get_cities()
		context["districts"] = self.region.get_districts()
		return context

class LoadCitiesMultipleForm(TemplateView):
	template_name = "region/load_cities_for_multiple_form.html"

	def get(self,request,*args,**kwargs):
		from region.models import Region

		self.region = Region.objects.get(pk=self.kwargs["pk"])
		return super(LoadCitiesMultipleForm,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(LoadCitiesMultipleForm,self).get_context_data(**kwargs)
		context["cities"] = self.region.get_cities()
		context["districts"] = self.region.get_districts()
		return context


class RegionDetailView(TemplateView, CategoryListMixin):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.region = Region.objects.get(slug=self.kwargs["slug"])
		self.template_name = get_full_template("region/",  "region.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(RegionDetailView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(RegionDetailView,self).get_context_data(**kwargs)
		context["region"] = self.region
		return context

class RegionElectDetailView(TemplateView, CategoryListMixin):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.region = Region.objects.get(slug=self.kwargs["slug"])
		self.template_name = get_full_template("region/",  "region_elects.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(RegionElectDetailView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(RegionElectDetailView,self).get_context_data(**kwargs)
		context["region"] = self.region
		return context

class RegionCommunitiesDetailView(TemplateView, CategoryListMixin):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.region = Region.objects.get(slug=self.kwargs["slug"])
		self.template_name = get_full_template("region/",  "region_communities.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(RegionCommunitiesDetailView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(RegionCommunitiesDetailView,self).get_context_data(**kwargs)
		context["region"] = self.region
		return context


class RegionOrganizationsDetailView(TemplateView, CategoryListMixin):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.region = Region.objects.get(slug=self.kwargs["slug"])
		self.template_name = get_full_template("region/",  "region_organizations.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(RegionOrganizationsDetailView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(RegionOrganizationsDetailView,self).get_context_data(**kwargs)
		context["region"] = self.region
		return context
