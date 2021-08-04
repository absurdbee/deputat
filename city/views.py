from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from city.models import City
from django.views.generic import ListView
from common.templates import get_small_template


class CityDetailView(TemplateView, CategoryListMixin):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.city = City.objects.get(slug=self.kwargs["slug"])
		self.template_name = get_small_template("city/city.html", request.META['HTTP_USER_AGENT'])
		return super(CityDetailView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(CityDetailView,self).get_context_data(**kwargs)
		context["object"] = self.city
		return context


class CityListView(ListView, CategoryListMixin):
	template_name, paginate_by = None, 12

	def get(self,request,*args,**kwargs):
		from region.models import Region

		self.region = Region.objects.get(slug=self.kwargs["slug"])
		self.template_name = get_small_template("city/city_list.html", request.META['HTTP_USER_AGENT'])
		return super(CityListView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		return Blog.objects.filter(category=self.cat)

	def get_context_data(self, **kwargs):
		context = super(CityListView, self).get_context_data(**kwargs)
		context['region'] = self.region
		return context
