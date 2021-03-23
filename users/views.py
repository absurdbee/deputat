from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from users.models import User
from django.views.generic import ListView
from common.utils import get_small_template
from django.http import HttpResponse


class AuthView(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		if request.user.is_authenticated:
			self.template_name = "profile/user_news.html"
		else:
			self.template_name = "account/auth.html"
		return super(AuthView,self).get(request,*args,**kwargs)

class SignupView(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		if request.user.is_authenticated:
			self.template_name = "profile/user_news.html"
		else:
			self.template_name = "account/signup.html"
		return super(SignupView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		from region.models import Region
		context=super(SignupView,self).get_context_data(**kwargs)
		context["regions"] = Region.onjects.only("pk")
		return context

class MainPhoneSend(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.template_name = get_small_template("generic/phone_verification.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(MainPhoneSend,self).get(request,*args,**kwargs)

class UserNewsView(ListView, CategoryListMixin):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
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
		self.user = User.objects.get(pk=self.kwargs["pk"])
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
		self.user = User.objects.get(pk=self.kwargs["pk"])
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
		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_small_template("profile/dislike_news.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(DislikeNewsView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(DislikeNewsView,self).get_context_data(**kwargs)
		context["user"] = self.user
		return context

	def get_queryset(self):
		dislike_news = self.user.get_dislike_news()
		return dislike_news


class UserView(TemplateView, CategoryListMixin):
	template_name = "profile/user.html"

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		return super(UserView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(UserView,self).get_context_data(**kwargs)
		context["user"] = self.user
		return context


class UserEditView(TemplateView):
	template_name, form = None, None

	def get(self,request,*args,**kwargs):
		from common.utils import get_my_template
		self.template_name = get_small_template("profile/edit.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserEditView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		from users.forms import UserForm

		context = super(UserEditView,self).get_context_data(**kwargs)
		context["form"] = UserForm()
		return context

	def post(self,request,*args,**kwargs):
		from users.forms import UserForm

		self.form = UserForm(request.POST, instance=request.user)
		if request.is_ajax() and self.form.is_valid():
			self.form.save()
			photo_input = request.FILES.get('image')
			if photo_input:
				request.user.create_s_avatar(photo_input)
				request.user.create_b_avatar(photo_input)
			return HttpResponse()
		return super(UserEditView,self).post(request,*args,**kwargs)

class UserEditPassword(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.template_name = get_small_template("profile/edit_password.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserEditPassword,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		from users.forms import UserPasswordForm
		context = super(UserEditPassword,self).get_context_data(**kwargs)
		context["form"] = UserPasswordForm()
		return context

	def post(self,request,*args,**kwargs):
		from users.forms import UserPasswordForm

		self.form = UserPasswordForm(request.POST,instance=request.user)
		if request.is_ajax() and self.form.is_valid():
			self.form.save()
			return HttpResponse()
		return super(UserEditPassword,self).post(request,*args,**kwargs)
