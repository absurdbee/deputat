from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from users.models import User
from django.http import Http404
from users.forms import UserForm
from django.shortcuts import redirect


class UserView(TemplateView, CategoryListMixin):
	template_name = "user.html"

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		return super(UserView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(UserView,self).get_context_data(**kwargs)
		context["user"] = self.user
		return context


class UserSettings(TemplateView):
	template_name = "user_settings.html"
	form = None

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		return super(UserSettings,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserSettings,self).get_context_data(**kwargs)
		context["form"] = UserForm()
		return context

	def post(self,request,*args,**kwargs):
		self.form = UserForm(request.POST, request.FILES)
		if self.form.is_valid():
			avatar = self.form.cleaned_data['avatar']
			request.user.avatar = avatar
			request.user.save()
		return redirect('user', pk=request.user.pk)
