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
	template_name = "region/load/get_region_citys.html"

	def get(self,request,*args,**kwargs):
		from city.models import City

		self.citys = City.objects.filter(region__pk=self.kwargs["pk"])
		return super(LoadCitiesView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(LoadCitiesView,self).get_context_data(**kwargs)
		context["citys"] = self.citys
		return context

class LoadSettingsCitiesView(TemplateView):
	template_name = "region/load/get_settings_citys.html"

	def get(self,request,*args,**kwargs):
		from city.models import City

		self.citys = City.objects.filter(region__pk=self.kwargs["pk"])
		return super(LoadSettingsCitiesView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(LoadSettingsCitiesView,self).get_context_data(**kwargs)
		context["citys"] = self.citys
		return context

class LoadLeftMenuRegions(TemplateView):
	template_name = "region/load_left_menu_regions.html"

	def get(self,request,*args,**kwargs):
		from region.models import Region

		self.regions = Region.objects.filter(is_deleted=False)
		return super(LoadLeftMenuRegions,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(LoadLeftMenuRegions,self).get_context_data(**kwargs)
		context["regions"] = self.regions
		return context

class LoadLeftMenuRegionsSelect(TemplateView):
	template_name = "region/load_left_menu_regions_select.html"

	def get(self,request,*args,**kwargs):
		from region.models import Region

		self.regions = Region.objects.filter(is_deleted=False)
		return super(LoadLeftMenuRegionsSelect,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(LoadLeftMenuRegionsSelect,self).get_context_data(**kwargs)
		context["regions"] = self.regions
		return context

class LoadLeftMenuRegionDistricts(TemplateView):
	template_name = "region/load_left_menu_region_districts.html"

	def get(self,request,*args,**kwargs):
		from region.models import Region

		self.region = Region.objects.get(slug=self.kwargs["slug"])
		return super(LoadLeftMenuRegionDistricts,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(LoadLeftMenuRegionDistricts,self).get_context_data(**kwargs)
		context["districts"] = self.region.get_districts()
		return context

class LoadDistrictsMultipleForm(TemplateView):
	template_name = "region/load_districts_for_multiple_form.html"

	def get(self,request,*args,**kwargs):
		from region.models import Region

		self.region = Region.objects.get(pk=self.kwargs["pk"])
		return super(LoadDistrictsMultipleForm,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(LoadDistrictsMultipleForm,self).get_context_data(**kwargs)
		context["districts"] = self.region.get_districts()
		return context


class LoadRegionForSelectRegionalElects(TemplateView):
	template_name = "region/load_region_for_select_regional_elects.html"

	def get(self,request,*args,**kwargs):
		from region.models import Region

		self.regions = Region.objects.filter(is_deleted=False)
		return super(LoadRegionForSelectRegionalElects,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(LoadRegionForSelectRegionalElects,self).get_context_data(**kwargs)
		context["regions"] = self.regions
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


class SearchElectsRegion(TemplateView, CategoryListMixin):
	template_name = None

	def get(self,request,*args,**kwargs):
		from elect.models import Elect

		self.region = Region.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_full_template("region/load/", "search_elects.html", request.user, request.META['HTTP_USER_AGENT'])
		self.q = request.GET.get('q')
		if self.q:
			self.list = Elect.objects.filter(region=self.region, name__icontains=self.q, type='PUB')
		else:
			self.list = []
		return super(SearchElectsRegion,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(SearchElectsRegion,self).get_context_data(**kwargs)
		context["region"] = self.region
		context["list"] = self.list
		context["q"] = self.q
		return context
