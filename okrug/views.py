from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from okrug.models import Okrug
from django.views.generic import ListView
from common.templates import get_full_template


class OkrugListView(ListView, CategoryListMixin):
	template_name, paginate_by = None, 12

	def get(self,request,*args,**kwargs):
		from region.models import Region

		self.region = Region.objects.get(slug=self.kwargs["slug"])
		self.template_name = get_full_template("okrug/", "okrug_list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(OkrugListView,self).get(request,*args,**kwargs)

	def get_context_data(self, **kwargs):
		context = super(OkrugListView, self).get_context_data(**kwargs)
		context['region'] = self.region
		return context


class OkrugDetailView(TemplateView, CategoryListMixin):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.okrug = Okrug.objects.get(slug=self.kwargs["slug"])
		self.template_name = get_full_template("okrug/", "okrug.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(OkrugDetailView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(OkrugDetailView,self).get_context_data(**kwargs)
		context["object"] = self.okrug
		return context

class OkrugElectDetailView(TemplateView, CategoryListMixin):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.okrug = Okrug.objects.get(slug=self.kwargs["slug"])
		self.template_name = get_full_template("okrug/", "okrug_elects.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(OkrugElectDetailView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		from region.models import Region
		from lists.models import AuthorityList

		context=super(OkrugElectDetailView,self).get_context_data(**kwargs)
		context["object"] = self.okrug
		context["region"] = self.okrug.region
		context["regions"] = Region.objects.only("pk")
		context["list"] = AuthorityList.objects.get(slug="candidate_duma")
		context["okrug"] = Okrug.objects.filter(region=self.okrug.region)
		return context
