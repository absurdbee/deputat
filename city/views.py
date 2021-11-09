from city.models import City
from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from common.templates import get_full_template


class CityDetailView(TemplateView, CategoryListMixin):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.city = City.objects.get(slug=self.kwargs["slug"])
		self.template_name = get_full_template("city/",  "city.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(CityDetailView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(CityDetailView,self).get_context_data(**kwargs)
		context["city"] = self.city
		return context
