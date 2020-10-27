from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from elect.models import Elect


class ElectDetailView(TemplateView, CategoryListMixin):
	template_name = "elect/elect.html"

	def get(self,request,*args,**kwargs):
		self.elect = Elect.objects.get(pk=self.kwargs["pk"])
		return super(ElectDetailView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(ElectDetailView,self).get_context_data(**kwargs)
		context["object"] = self.elect
		return context
