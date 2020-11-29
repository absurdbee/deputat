from django.views.generic.base import TemplateView
from stst.models import *
from common.utils import get_managers_template
from elect.models import Elect
from blog.models import BlogVotes, ElectVotes


class StatView(TemplateView):
    template_name = "stat/index.html"


class ElectYearStat(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.elect = Elect.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_managers_template("stat/elect_year.html", request.user, request.META['HTTP_USER_AGENT'])
        self.years = ElectNumbers.objects.dates('created', 'year')[0:10]
        self.members_views, self.views, self.likes, self.dislikes = [], [], [], []
        for i in self.years:
            members_view = ElectNumbers.objects.filter(created__year=i.year, elect=self.elect.pk).exclude(user=0).distinct("elect").count()
            view = ElectNumbers.objects.filter(created__year=i.year, elect=self.elect.pk).count()
            like = self.elect.likes_count_year(i.year)
            dislike = self.elect.dislikes_count_year(i.year)
            self.members_views += [members_view]
            self.views += [view]
            self.likes += [like]
            self.dislikes += [dislike]
        return super(ElectYearStat,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ElectYearStat,self).get_context_data(**kwargs)
        context["user"] = self.user
        context["years"] = self.years
        context["members_views"] = self.members_views
        context["views"] = self.views
        context["likes"] = self.likes
        context["dislikes"] = self.dislikes
        return context


class UserCoberturaMonth(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_settings_template("users/user_stat/cobertura_month.html", request.user, request.META['HTTP_USER_AGENT'])
		self.months = UserNumbers.objects.dates('created', 'month')[0:10]
		self.views, self.sities = [], []
		for i in self.months:
			view = UserNumbers.objects.filter(created__month=i.month, target=self.user.pk).distinct("target").count()
			self.views += [view]

		current_views = UserNumbers.objects.filter(created__month=self.months[0].month, target=self.user.pk).values('target').distinct()
		user_ids = [use['target'] for use in current_views]
		users = User.objects.filter(id__in=user_ids)
		for user in users:
			try:
				sity = user.get_last_location().city_ru
				self.sities += [sity]
			except:
				self.sities += ["Местоположение не указано",]
		return super(UserCoberturaMonth,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserCoberturaMonth,self).get_context_data(**kwargs)
		context["user"] = self.user
		context["months"] = self.months
		context["views"] = self.views
		context["sities"] = set(self.sities)
		return context


class UserCoberturaWeek(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		import datetime
		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_settings_template("users/user_stat/cobertura_week.html", request.user, request.META['HTTP_USER_AGENT'])
		self.weeks = UserNumbers.objects.dates('created', 'week')[0:10]
		self.range, self.views, self.sities = [], [], []
		for i in self.weeks:
			days = [i.day, i.day + 1, i.day + 2, i.day + 3, i.day + 4, i.day + 5, i.day + 6]
			view = UserNumbers.objects.filter(created__day__in=days, target=self.user.pk).distinct("target").count()
			i6 = i + datetime.timedelta(days=7)
			self.range += [str(i.strftime('%d.%m')) + " - " + str(i6.strftime('%d.%m'))]
			self.views += [view ]
		dss = [self.weeks[0].day, self.weeks[0].day + 1, self.weeks[0].day + 2, self.weeks[0].day + 3, self.weeks[0].day + 4, self.weeks[0].day + 5, self.weeks[0].day + 6]
		current_views = UserNumbers.objects.filter(created__day__in=dss, target=self.user.pk).values('target').distinct()
		user_ids = [use['target'] for use in current_views]
		users = User.objects.filter(id__in=user_ids)
		for user in users:
			try:
				sity = user.get_last_location().city_ru
				self.sities += [sity]
			except:
				self.sities += ["Местоположение не указано",]
		return super(UserCoberturaWeek,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserCoberturaWeek,self).get_context_data(**kwargs)
		context["user"] = self.user
		context["weeks"] = self.weeks
		context["range"] = self.range
		context["views"] = self.views
		context["sities"] = set(self.sities)
		return context

class UserCoberturaDay(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_settings_template("users/user_stat/cobertura_day.html", request.user, request.META['HTTP_USER_AGENT'])
		self.days = UserNumbers.objects.dates('created', 'day')[0:10]
		self.views, self.sities = [], []
		for i in self.days:
			view = UserNumbers.objects.filter(created__day=i.day, target=self.user.pk).distinct("target").count()
			self.views += [view]
		current_views = UserNumbers.objects.filter(created__day=self.days[0].day, target=self.user.pk).values('target').distinct()
		user_ids = [use['target'] for use in current_views]
		users = User.objects.filter(id__in=user_ids)
		for user in users:
			try:
				sity = user.get_last_location().city_ru
				self.sities += [sity]
			except:
				self.sities += ["Местоположение не указано",]
		return super(UserCoberturaDay,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserCoberturaDay,self).get_context_data(**kwargs)
		context["user"] = self.user
		context["days"] = self.days
		context["views"] = self.views
		context["sities"] = set(self.sities)
		return context
