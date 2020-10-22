from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from django.views.generic import ListView
from lists.models import ElectList
from elect.models import Elect


class ElectsList(ListView, CategoryListMixin):
	template_name = "elect_list/list.html"
	paginate_by = 20

	def get(self,request,*args,**kwargs):
		if self.kwargs["slug"] == None:
			self.list = ElectList.objects.first()
		else:
			self.list = ElectList.objects.get(slug=self.kwargs["slug"])
		return super(ElectsList,self).get(request,*args,**kwargs)

	def get_queryset(self):
		elects = Elect.objects.filter(list=self.list)
		return elects

	def get_context_data(self,**kwargs):
		context = super(ElectsList,self).get_context_data(**kwargs)
		context["list"] = self.list
		return context

class ElectListsView(ListView, CategoryListMixin):
    template_name = "elect_list/all_list.html"

	def get_queryset(self):
		lists = ElectList.objects.only("pk")
		return lists
