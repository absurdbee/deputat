from django.views.generic.base import TemplateView
from users.model.settings import *
from django.http import HttpResponse, HttpResponseBadRequest
from common.utils import get_my_template


class UserProfileSettings(TemplateView):
	template_name, form = None, None

	def get(self,request,*args,**kwargs):
		self.template_name = get_my_template("profile/settings_profile.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserProfileSettings,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		from users.forms import UserForm

		context = super(UserProfileSettings,self).get_context_data(**kwargs)
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
		return super(UserProfileSettings,self).post(request,*args,**kwargs)


class UserNotifySettings(TemplateView):
    template_name, form = None, None

    def get(self,request,*args,**kwargs):
        from users.forms import UserNotifyForm

        self.template_name = get_my_template("profile/settings_notify.html", request.user, request.META['HTTP_USER_AGENT'])
        try:
            self.notify = UserNotifications.objects.get(user=request.user)
        except:
            self.notify = UserNotifications.objects.create(user=request.user)
        self.form = UserNotifyForm(instance=self.notify)
        return super(UserNotifySettings,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserNotifySettings,self).get_context_data(**kwargs)
        context["form"] = self.form
        context["notify"] = self.notify
        context["user"] = self.request.user
        return context

    def post(self,request,*args,**kwargs):
        from users.forms import UserNotifyFory

        self.notify = UserNotifications.objects.get(user=request.user)
        self.form = UserNotifyForm(request.POST, instance=self.notify)
        if request.is_ajax() and self.form.is_valid():
            self.form.save()
        return HttpResponse()


class UserPrivateSettings(TemplateView):
	template_name, form = None, None

	def get(self,request,*args,**kwargs):
		from users.forms import UserPrivateForm
		try:
			self.private = UserPrivate.objects.get(user=request.user)
		except:
			self.private = UserPrivate.objects.create(user=request.user)
		self.form = UserPrivateForm(instance=self.private)
		self.template_name = get_my_template("profile/settings_private.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserPrivateSettings,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserPrivateSettings,self).get_context_data(**kwargs)
		context["user"] = self.request.user
		context["form"] = self.form
		context["private"] = self.private
		return context

	def post(self,request,*args,**kwargs):
		from users.forms import UserPrivateForm

		self.private = UserPrivate.objects.get(user=request.user)
		self.form = UserPrivateForm(request.POST, instance=self.private)
		if request.is_ajax() and self.form.is_valid():
			self.form.save()
		return HttpResponse()


class UserQuardSettings(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.template_name = get_my_template("profile/settings_quard.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserQuardSettings,self).get(request,*args,**kwargs)


class UserAboutSettings(TemplateView):
	template_name, form = None, None

	def get(self,request,*args,**kwargs):
		from users.forms import UserInfoForm
		from users.model.profile import UserInfo
		try:
			self.info = UserInfo.objects.get(user=request.user)
		except:
			self.info = UserInfo.objects.create(user=request.user)
		self.form = UserInfoForm(instance=self.info)
		self.template_name = get_my_template("profile/settings_about.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserAboutSettings,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserAboutSettings,self).get_context_data(**kwargs)
		context["user"] = self.request.user
		context["form"] = self.form
		context["info"] = self.info
		return context

	def post(self,request,*args,**kwargs):
		from users.forms import UserInfoForm
		from users.model.profile import UserInfo

		self.info = UserInfo.objects.get(user=request.user)
		self.form = UserInfoForm(request.POST, instance=self.info)
		if request.is_ajax() and self.form.is_valid():
			self.form.save()
		return HttpResponse()
