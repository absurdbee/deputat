from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from users.models import User
from django.views.generic import ListView


class AuthView(TemplateView, CategoryListMixin):
	template_name = None

	def get(self,request,*args,**kwargs):
		if request.user.is_authenticated:
			self.template_name = "profile/draft_news.html"
		else:
			self.template_name = "auth.html"
		return super(AuthView,self).get(request,*args,**kwargs)


class UserNewsView(ListView, CategoryListMixin):
	template_name = "profile/user_news.html"
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.user = request.user
		return super(UserNewsView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(UserNewsView,self).get_context_data(**kwargs)
		context["user"] = self.user
		return context

	def get_queryset(self):
		user_news = self.user.get_news()
		return user_news


class SubscribeElectsView(ListView, CategoryListMixin):
	template_name = "profile/subscribes_elect.html"
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.user = request.user
		return super(SubscribeElectsView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(SubscribeElectsView,self).get_context_data(**kwargs)
		context["user"] = self.user
		return context

	def get_queryset(self):
		elect_subscribers = self.user.get_elect_subscribers()
		return elect_subscribers


class LikeNewsView(ListView, CategoryListMixin):
	template_name = "profile/like_news.html"
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.user = request.user
		return super(LikeNewsView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(LikeNewsView,self).get_context_data(**kwargs)
		context["user"] = self.user
		return context

	def get_queryset(self):
		like_news = self.user.get_like_news()
		return like_news


class DislikeNewsView(ListView, CategoryListMixin):
	template_name = "profile/dislike_news.html"
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.user = request.user
		return super(DislikeNewsView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(DislikeNewsView,self).get_context_data(**kwargs)
		context["user"] = self.user
		return context

	def get_queryset(self):
		dislike_news = self.user.get_dislike_news()
		return dislike_news
