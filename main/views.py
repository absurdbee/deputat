from django.views.generic import ListView
from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from users.models import User
from django.views import View
from django.http import Http404
import json, requests
from common.templates import render_for_platform, get_small_template


class MainPageView(ListView, CategoryListMixin):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_small_template("main/mainpage.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(MainPageView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(MainPageView,self).get_context_data(**kwargs)
		return context

	def get_queryset(self):
		from common.notify.progs import get_news
		return get_news()

class MainRegionView(ListView, CategoryListMixin):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from region.models import Region

		self.template_name = get_small_template("main/region.html", request.user, request.META['HTTP_USER_AGENT'])
		self.region = Region.objects.get(slug=self.kwargs["slug"])
		return super(MainRegionView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(MainRegionView,self).get_context_data(**kwargs)
		context["region"] = self.region
		return context

	def get_queryset(self):
		from common.notify.progs import get_region_news
		return get_region_news(self.region.name)

class MainMapView(TemplateView, CategoryListMixin):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.template_name = get_small_template("main/map.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(MainMapView,self).get(request,*args,**kwargs)

class MainStatView(TemplateView, CategoryListMixin):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.template_name = get_small_template("main/stat.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(MainStatView,self).get(request,*args,**kwargs)


class MainDocsView(ListView, CategoryListMixin):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from region.models import Region

		self.template_name = get_small_template("main/docs.html", request.user, request.META['HTTP_USER_AGENT'])
		self.region = Region.objects.get(slug=self.kwargs["slug"])
		return super(MainDocsView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		return []


class MyNewsView(ListView, CategoryListMixin):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_my_template("main/my_news.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(MyNewsView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(MyNewsView,self).get_context_data(**kwargs)
		return context

	def get_queryset(self):
		from common.notify.progs import get_my_news
		if self.request.user.is_authenticated:
			return get_my_news(self.request.user)
		else:
			return []

class DraftNewsView(ListView, CategoryListMixin):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_my_template("main/draft_news.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(DraftNewsView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(DraftNewsView,self).get_context_data(**kwargs)
		return context

	def get_queryset(self):
		from common.notify.progs import get_draft_news
		if self.request.user.is_authenticated and (self.request.user.is_manager() or self.request.user.is_supermanager()):
			return get_draft_news(self.request.user)
		else:
			return []
