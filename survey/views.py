from django.views.generic import ListView
from survey.models import Survey, SurveyList
from users.models import User
from generic.mixins import CategoryListMixin
from django.views.generic.base import TemplateView


class SurveyView(ListView):
	template_name = "survey.html"

	def get_queryset(self):
		return Survey.objects.only("pk")

class UserSurveyDetail(TemplateView, CategoryListMixin):
	template_name = None

	def get(self,request,*args,**kwargs):
		from common.templates import get_full_template

		self.survey = Survey.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_full_template("survey/detail/", "u.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserSurveyDetail,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(UserSurveyDetail,self).get_context_data(**kwargs)
		context["object"] = self.survey
		return context

class UserSurvey(ListView, CategoryListMixin):
	template_name, paginate_by, can_add_list = None, 15, None

	def get(self,request,*args,**kwargs):
		from common.templates import get_template_user_item, get_template_anon_user_item
		from django.conf import settings

		pk = int(self.kwargs["pk"])
		self.user = User.objects.get(pk=pk)
		self.list = self.user.get_survey_list()
		self.count_lists = self.list.get_user_lists_count(pk)
		self.get_lists = self.list.get_user_lists(pk)
		if self.user.pk == int(self.kwargs["pk"]) and self.count_lists < settings.USER_MAX_SURVEY_LISTS:
			self.can_add_list = True
		if request.user.is_authenticated:
			self.template_name = get_template_user_item(self.list, "user_survey/main/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_survey_manager())
		else:
			self.template_name = get_template_anon_user_item(self.list, "user_survey/main/", "list.html", request.META['HTTP_USER_AGENT'])
		return super(UserSurvey,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserSurvey,self).get_context_data(**kwargs)
		context['user'] = self.user
		context['list'] = self.list
		context['get_lists'] = self.get_lists
		context['count_lists'] = self.count_lists
		context['can_add_list'] = self.can_add_list
		return context

	def get_queryset(self):
		return self.list.get_items()


class UserSurveyList(ListView, CategoryListMixin):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from survey.models import SurveyList
		from common.templates import get_template_user_item, get_template_anon_user_item

		self.list = SurveyList.objects.get(uuid=self.kwargs["uuid"])
		if request.user.is_authenticated:
			self.template_name = get_template_user_item(self.list, "user_survey/list/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_survey_manager())
		else:
			self.template_name = get_template_anon_user_item(self.list, "user_survey/list/", "list.html", request.META['HTTP_USER_AGENT'])
		return super(UserSurveyList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserSurveyList,self).get_context_data(**kwargs)
		context['user'] = self.list.creator
		context['list'] = self.list
		return context

	def get_queryset(self):
		return self.list.get_items()


class UserLoadSurveylist(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from common.templates import get_template_user_window, get_template_anon_user_window

		self.list = SurveyList.objects.get(pk=self.kwargs["pk"])
		if request.user.is_authenticated:
			self.template_name = get_template_user_window(self.list, "user_survey/load/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_doc_manager())
		else:
			self.template_name = get_template_anon_user_window(self.list, "user_survey/load/", "list.html", request.META['HTTP_USER_AGENT'])
		return super(UserLoadSurveylist,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadSurveylist,self).get_context_data(**kwargs)
		context['list'] = self.list
		return context

	def get_queryset(self):
		return self.list.get_items()


class UserLoadPenaltySurveyList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from common.templates import get_managers_template

		self.list = SurveyList.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_managers_template("user_survey/load/penalty_list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadPenaltySurveyList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadPenaltySurveyList,self).get_context_data(**kwargs)
		context['list'] = self.list
		return context

	def get_queryset(self):
		return self.list.get_penalty_items()

class UserLoadModeratedSurveyList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from common.templates import get_managers_template

		self.list = SurveyList.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_managers_template("user_survey/load/moderated_list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadModeratedSurveyList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadModeratedSurveyList,self).get_context_data(**kwargs)
		context['list'] = self.list
		return context

	def get_queryset(self):
		return self.list.get_items()
