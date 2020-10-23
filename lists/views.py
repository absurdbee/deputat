from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from django.views.generic import ListView
from lists.models import AuthorityList
from elect.models import Elect


class AuthorityListView(ListView, CategoryListMixin):
	template_name = "elect_list/authority_list.html"
	paginate_by = 20

	def get(self,request,*args,**kwargs):
		if self.kwargs["slug"] == None:
			self.list = AuthorityList.objects.first()
		else:
			self.list = AuthorityList.objects.get(slug=self.kwargs["slug"])
		return super(AuthorityListView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		elects = Elect.objects.filter(list=self.list)
		return elects

	def get_context_data(self,**kwargs):
		context = super(AuthorityListView,self).get_context_data(**kwargs)
		context["list"] = self.list
		return context


class FractionList(ListView, CategoryListMixin):
	template_name = "elect_list/fraction_list.html"
	paginate_by = 20

	def get_queryset(self):
		elects = Elect.objects.filter(fraction__slug=self.kwargs["slug"])
		return elects

	def get_context_data(self,**kwargs):
		context = super(FractionList,self).get_context_data(**kwargs)
		context["list"] = self.list
		return context

class ElectListsView(TemplateView, CategoryListMixin):
	template_name = "elect_list/all_list.html"

	def get_context_data(self,**kwargs):
		context = super(ElectListsView,self).get_context_data(**kwargs)
		context["lists"] = AuthorityList.objects.only("pk")
		return context
