from django.views.generic import ListView
from survey.models import Survey, SurveyList
from users.models import User


class SurveyView(ListView):
	template_name = "survey.html"

	def get_queryset(self):
		return Survey.objects.only("pk")


class UserSurvey(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from common.templates import get_template_user_item, get_template_anon_user_item

		pk = self.kwargs["pk"]
		self.user = User.objects.get(pk=pk)
		self.list = self.user.get_survey_list()
		self.count_lists = self.list.get_user_lists_count(pk)
		self.is_have_lists = self.list.is_have_user_lists(pk)
		self.get_lists = self.list.get_user_lists(pk)
		if request.user.is_authenticated:
			self.template_name = get_template_user_item(self.list, "user_survey/main/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_survey_manager())
		else:
			self.template_name = get_template_anon_user_item(self.list, "user_survey/main/anon_list.html", request.META['HTTP_USER_AGENT'])
		return super(UserSurvey,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserSurvey,self).get_context_data(**kwargs)
		context['user'] = self.user
		context['list'] = self.list
		context['is_have_lists'] = self.is_have_lists
		context['get_lists'] = self.get_lists
		context['count_lists'] = self.count_lists
		return context

	def get_queryset(self):
		return self.list.get_items()


class UserSurveyList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from survey.models import SurveyList
		from common.templates import get_template_user_item, get_template_anon_user_item

		self.list = SurveyList.objects.get(uuid=self.kwargs["uuid"])
		if request.user.is_authenticated:
			self.template_name = get_template_user_item(self.list, "user_survey/list/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_survey_manager())
		else:
			self.template_name = get_template_anon_user_item(self.list, "user_survey/list/anon_list.html", request.META['HTTP_USER_AGENT'])
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
			self.template_name = get_template_user_item(self.list, "user_survey/load/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_doc_manager())
		else:
			self.template_name = get_template_anon_user_item(self.list, "user_survey/load/anon_list.html", request.META['HTTP_USER_AGENT'])
		return super(UserLoadSurveylist,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadSurveylist,self).get_context_data(**kwargs)
		context['list'] = self.list
		return context

	def get_queryset(self):
		return self.list.get_items()
