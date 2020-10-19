from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from django.views.generic import ListView
from lists.models import ElectList
from elect.models import Elect


class ElectLists(ListView, CategoryListMixin):
	template_name = "elect_index.html"
	paginate_by = 20

	def get(self,request,*args,**kwargs):
		if self.kwargs["slug"] == None:
			self.cat = ElectList.objects.first()
		else:
			self.cat = ElectList.objects.get(slug=self.kwargs["slug"])
		return super(ElectLists,self).get(request,*args,**kwargs)

	def get_queryset(self):
		elects = Elect.objects.filter(category=self.cat)
		return elects

	def get_context_data(self,**kwargs):
		context = super(ElectLists,self).get_context_data(**kwargs)
		context["category"] = self.cat
		return context

class ElectListView(TemplateView, CategoryListMixin):
    template_name = "elect_list.html"
