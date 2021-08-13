from django.views.generic.base import TemplateView
from users.model.settings import *
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from common.templates import get_my_template
from generic.mixins import CategoryListMixin


class UserProfileSettings(TemplateView, CategoryListMixin):
	template_name, form = None, None

	def get(self,request,*args,**kwargs):
		self.template_name = get_my_template("profile/settings/profile.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserProfileSettings,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		from users.forms import UserForm
		from region.models import Region

		context = super(UserProfileSettings,self).get_context_data(**kwargs)
		context["form"] = UserForm()
		context["regions"] = Region.objects.only("pk")
		context["cities"] = self.request.user.city.region.get_cities()
		return context

	def post(self,request,*args,**kwargs):
		from users.forms import UserForm

		self.form = UserForm(request.POST, request.FILES, instance=request.user)
		if request.is_ajax() and self.form.is_valid():
			self.form.save()
			photo_input = request.FILES.get('s_avatar')
			if photo_input:
				request.user.create_s_avatar(photo_input)
			return HttpResponse()
		return super(UserProfileSettings,self).post(request,*args,**kwargs)


class UserNotifySettings(TemplateView, CategoryListMixin):
    template_name, form = None, None

    def get(self,request,*args,**kwargs):
        from users.forms import UserNotifyForm

        self.template_name = get_my_template("profile/settings/notify.html", request.user, request.META['HTTP_USER_AGENT'])
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


class UserPrivateSettings(TemplateView, CategoryListMixin):
	template_name, form = None, None

	def get(self,request,*args,**kwargs):
		from users.forms import UserPrivateForm
		try:
			self.private = UserPrivate.objects.get(user=request.user)
		except:
			self.private = UserPrivate.objects.create(user=request.user)
		self.form = UserPrivateForm(instance=self.private)
		self.template_name = get_my_template("profile/settings/private.html", request.user, request.META['HTTP_USER_AGENT'])
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


class UserQuardSettings(TemplateView, CategoryListMixin):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.template_name = get_my_template("profile/settings/quard.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserQuardSettings,self).get(request,*args,**kwargs)


class UserAboutSettings(TemplateView, CategoryListMixin):
	template_name, form = None, None

	def get(self,request,*args,**kwargs):
		from users.forms import UserProfileForm
		from users.model.profile import UserProfile
		try:
			self.info = UserProfile.objects.get(user=request.user)
		except:
			self.info = UserProfile.objects.create(user=request.user)
		self.form = UserProfileForm(instance=self.info)
		self.template_name = get_my_template("profile/settings/about.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserAboutSettings,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserAboutSettings,self).get_context_data(**kwargs)
		context["user"] = self.request.user
		context["form"] = self.form
		context["info"] = self.info
		return context

	def post(self,request,*args,**kwargs):
		from users.forms import UserProfileForm
		from users.model.profile import UserProfile
		from datetime import datetime
		from users.model.profile import UserCheck

		self.info = UserProfile.objects.get(user=request.user)
		self.form = UserProfileForm(request.POST, instance=self.info)
		if request.is_ajax() and self.form.is_valid():
			new_info = self.form.save(commit=False)
			new_info.save()
			try:
				check = UserCheck.objects.get(user_id=request.user.pk)
			except:
				check = UserCheck.objects.create(user_id=request.user.pk)
			if not check.profile_info:
				info = UserProfile.objects.get(user_id=request.user.pk)
				if info.education and info.employment:
					check.profile_info = True
					check.save(update_fields=['profile_info'])
					request.user.plus_carma(100, "ADD")
		return HttpResponse()


class UserEditPassword(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.template_name = get_my_template("profile/settings/password.html", request.user, request.META['HTTP_USER_AGENT'])
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

class UserEditPhone(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.template_name = get_my_template("profile/settings/phone.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserEditPhone,self).get(request,*args,**kwargs)


class UserCreateKey(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.template_name = get_my_template("profile/settings/secret_key.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserCreateKey,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		from users.forms import UserKeyForm
		context = super(UserCreateKey,self).get_context_data(**kwargs)
		context["form"] = UserKeyForm()
		return context

	def post(self,request,*args,**kwargs):
		from users.forms import UserKeyForm
		from users.model.settings import UserSecretKey

		if not UserSecretKey.objects.filter(user=request.user).exists():
			user_key = UserSecretKey.objects.create(user=request.user)
		self.form = UserKeyForm(request.POST)
		if request.is_ajax() and self.form.is_valid():
			_item = self.form.save(commit=False)
			user_key.key = _item.key
			user_key.save(update_fields=["key"])
			return HttpResponse()
		return super(UserCreateKey,self).post(request,*args,**kwargs)


class UserDeputatSend(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.template_name = get_my_template("profile/settings/deputat_send.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserDeputatSend,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		from users.forms import DeputatSendForm
		context = super(UserDeputatSend,self).get_context_data(**kwargs)
		context["form"] = DeputatSendForm()
		return context

	def post(self,request,*args,**kwargs):
		from users.forms import DeputatSendForm
		from users.model.settings import DeputatSend

		if DeputatSend.objects.filter(user=request.user, key__isnull=False).exists():
			return HttpResponseBadRequest()
		self.form = DeputatSendForm(request.POST)
		if request.is_ajax() and self.form.is_valid():
			_item = self.form.save(commit=False)
			DeputatSend.create_item(user=request.user, text=_item.text)
			return HttpResponse()
		return super(UserDeputatSend,self).post(request,*args,**kwargs)

class PasswordRecovery(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		if request.user.is_anonymous:
			self.template_name = "account/password_forgot_main.html"
		else:
			self.template_name = "account/login.html"
		return super(PasswordRecovery,self).get(request,*args,**kwargs)


class GetPasswordRecoverySecretKey(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		if request.user.is_anonymous:
			self.template_name = "account/secret_key_window.html"
		else:
			raise Http404
		return super(GetPasswordRecoverySecretKey,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		from users.forms import UserKeyForm
		context = super(GetPasswordRecoverySecretKey,self).get_context_data(**kwargs)
		context["form"] = UserKeyForm()
		return context

	def post(self,request,*args,**kwargs):
		from users.forms import UserKeyForm
		from users.model.settings import UserSecretKey
		from users.models import User
		from common.templates import render_for_platform

		self.form = UserKeyForm(request.POST)
		if request.is_ajax() and self.form.is_valid():
			_item = self.form.save(commit=False)
			if UserSecretKey.objects.filter(key=_item.key):
				key_item = UserSecretKey.objects.get(key=_item.key)
				user = User.objects.filter(pk=key_item.user_id)
				return render_for_platform(request, 'profile/settings/quard.html',{'user': user})
			else:
				return HttpResponseBadRequest()
		return super(GetPasswordRecoverySecretKey,self).post(request,*args,**kwargs)

class GetPasswordRecoveryPhone(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		if request.user.is_anonymous:
			self.template_name = "account/phone_window.html"
		else:
			raise Http404
		return super(GetPasswordRecoveryPhone,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		from users.forms import UserPhoneForm
		context = super(GetPasswordRecoveryPhone,self).get_context_data(**kwargs)
		context["form"] = UserPhoneForm()
		return context

	def post(self,request,*args,**kwargs):
		from users.forms import UserPhoneForm
		from users.model.settings import DeputatSend

		if DeputatSend.objects.filter(user=request.user, key__isnull=False).exists():
			return HttpResponseBadRequest()
		self.form = UserPhoneForm(request.POST)
		if request.is_ajax() and self.form.is_valid():
			_item = self.form.save(commit=False)
			DeputatSend.create_item(user=request.user, text=_item.text)
			return HttpResponse()
		return super(GetPasswordRecoveryPhone,self).post(request,*args,**kwargs)
