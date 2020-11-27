from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from django.views.generic import ListView
from lists.models import *
from elect.models import Elect
from common.utils import get_small_template, get_full_template


class AuthorityListView(ListView, CategoryListMixin):
	""" Чиновники выбранного списка: госдумы, совфеда и т.д. """

	template_name = None
	paginate_by = 20

	def get(self,request,*args,**kwargs):
		if self.kwargs["slug"] == None:
			self.list = AuthorityList.objects.first()
		else:
			self.list = AuthorityList.objects.get(slug=self.kwargs["slug"])
		self.template_name = get_full_template("elect_list/authority_list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(AuthorityListView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		elects = Elect.objects.filter(list=self.list)
		return elects

	def get_context_data(self,**kwargs):
		context = super(AuthorityListView,self).get_context_data(**kwargs)
		context["list"] = self.list
		return context


class FractionList(ListView, CategoryListMixin):
	""" Чиновники выбранной фракции госдумы """

	template_name = None
	paginate_by = 20

	def get(self,request,*args,**kwargs):
		self.template_name = get_small_template("elect_list/fraction_list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(FractionList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(FractionList,self).get_context_data(**kwargs)
		context["list"] = self.list
		return context

	def get_queryset(self):
		elects = Elect.objects.filter(fraction__slug=self.kwargs["slug"])
		return elects

class ElectListsView(TemplateView, CategoryListMixin):
	""" Списки чиновников: госдума, совфед и подобное """

	template_name = None

	def get(self,request,*args,**kwargs):
		self.template_name = get_small_template("elect_list/all_list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(ElectListsView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(ElectListsView,self).get_context_data(**kwargs)
		context["lists"] = AuthorityList.objects.only("pk")
		return context


class RegionElectView(TemplateView, CategoryListMixin):
	""" Чиновники (госдумы, совфеда и т.д.) выбранного региона """

	template_name = None

	def get(self,request,*args,**kwargs):
		self.region = Region.objects.get(slug=self.kwargs["slug"])
		self.template_name = get_small_template("elect_list/region_list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(RegionElectView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(RegionElectView,self).get_context_data(**kwargs)
		context["region"] = self.region
		return context


class RegionDetailView(TemplateView, CategoryListMixin):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.region = Region.objects.get(slug=self.kwargs["slug"])
		self.template_name = get_full_template("elect_list/region.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(RegionDetailView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(RegionDetailView,self).get_context_data(**kwargs)
		context["region"] = self.region
		return context
