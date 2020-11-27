from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from users.models import User
from django.views.generic import ListView
from common.utils import get_small_template


class AuthView(TemplateView, CategoryListMixin):
	template_name = None

	def get(self,request,*args,**kwargs):
		if request.user.is_authenticated:
			self.template_name = "profile/draft_news.html"
		else:
			self.template_name = "account/auth.html"
		return super(AuthView,self).get(request,*args,**kwargs)


class UserNewsView(ListView, CategoryListMixin):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.user = request.user
		self.template_name = get_small_template("profile/user_news.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserNewsView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(UserNewsView,self).get_context_data(**kwargs)
		context["user"] = self.user
		return context

	def get_queryset(self):
		user_news = self.user.get_news()
		return user_news


class SubscribeElectsView(ListView, CategoryListMixin):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.user = request.user
		self.template_name = get_small_template("profile/subscribes_elect.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(SubscribeElectsView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(SubscribeElectsView,self).get_context_data(**kwargs)
		context["user"] = self.user
		return context

	def get_queryset(self):
		elect_subscribers = self.user.get_elect_subscribers()
		return elect_subscribers


class LikeNewsView(ListView, CategoryListMixin):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.user = request.user
		self.template_name = get_small_template("profile/like_news.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(LikeNewsView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(LikeNewsView,self).get_context_data(**kwargs)
		context["user"] = self.user
		return context

	def get_queryset(self):
		like_news = self.user.get_like_news()
		return like_news


class DislikeNewsView(ListView, CategoryListMixin):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.user = request.user
		self.template_name = get_small_template("profile/dislike_news.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(DislikeNewsView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(DislikeNewsView,self).get_context_data(**kwargs)
		context["user"] = self.user
		return context

	def get_queryset(self):
		dislike_news = self.user.get_dislike_news()
		return dislike_news
