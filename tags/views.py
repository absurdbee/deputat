from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from tags.models import ManagerTag
from blog.models import ElectNew
from django.views.generic import ListView
from common.utils import get_small_template


class TagView(TemplateView, CategoryListMixin):
	template_name = None

	def get(self,request,*args,**kwargs):
		from urllib.parse import unquote

		self.tag = ManagerTag.objects.get(name=unquote(self.kwargs["name"]))
		self.template_name = get_small_template("tags/tag.html", request.META['HTTP_USER_AGENT'])
		return super(TagView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(TagView,self).get_context_data(**kwargs)
		context["object"] = self.tag
		return context


class ManagerTagsView(ListView, CategoryListMixin):
	template_name, paginate_by = None, 50

	def get(self,request,*args,**kwargs):
		self.template_name = get_small_template("tags/tags.html", request.META['HTTP_USER_AGENT'])
		return super(ManagerTagsView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		return ManagerTag.objects.only("pk")


class UserTagView(ListView, CategoryListMixin):
	template_name, paginate_by = None, 12

	def get(self,request,*args,**kwargs):
		from taggit.models import Tag

		self.tag = Tag.objects.get(name=self.kwargs["name"])
		self.template_name = get_small_template("tags/elect_news.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserTagView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		return ElectNew.objects.filter(tags__name=self.tag)

	def get_context_data(self, **kwargs):
		context = super(UserTagView, self).get_context_data(**kwargs)
		context['tag'] = self.tag
		return context
