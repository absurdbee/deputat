from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from elect.models import Elect
from blog.models import ElectNew
from django.views.generic import ListView


class ElectDetailView(TemplateView, CategoryListMixin):
	template_name = "elect/elect.html"

	def get(self,request,*args,**kwargs):
		self.elect = Elect.objects.get(pk=self.kwargs["pk"])
		return super(ElectDetailView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(ElectDetailView,self).get_context_data(**kwargs)
		context["object"] = self.elect
		return context



class ElectNewsView(ListView, CategoryListMixin):
	template_name = "elect/news.html"
	paginate_by = 12

	def get(self,request,*args,**kwargs):
		self.elect = Elect.objects.get(pk=self.kwargs["pk"])
		return super(ElectNewsView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(ElectNewsView,self).get_context_data(**kwargs)
		context["object"] = self.object
		context["elect"] = self.elect
		return context

	def get_queryset(self):
		blog = ElectNew.objects.filter(elect=self.elect)
		return blog


class ElectNewDetailView(TemplateView, CategoryListMixin):
	template_name = "elect/elect_new.html"

	def get(self,request,*args,**kwargs):
		self.new = ElectNew.objects.get(pk=self.kwargs["pk"])
		return super(ElectNewDetailView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(ElectNewDetailView,self).get_context_data(**kwargs)
		context["object"] = self.new
		return context
