from django.views.generic import ListView
from common.templates import get_my_template, get_small_template
from django.views.generic.base import TemplateView
from notify.models import Notify, Wall
from generic.mixins import CategoryListMixin


class AllNotifyView(ListView, CategoryListMixin):
    """ Все уведомления пользователя """
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.template_name = get_my_template("notify/all_notify.html", request.user, request.META['HTTP_USER_AGENT'])
        self.user, self.all_notify = request.user, request.user.get_user_notify()
        return super(AllNotifyView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllNotifyView,self).get_context_data(**kwargs)
        context["user"] = self.user
        return context

    def get_queryset(self):
        return self.all_notify

class RecentNotifyView(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.template_name = get_my_template("notify/recent_notify.html", request.user, request.META['HTTP_USER_AGENT'])
        self.user, self.all_notify = request.user, request.user.get_user_notify()
        return super(RecentNotifyView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(RecentNotifyView,self).get_context_data(**kwargs)
        context["user"] = self.user
        return context

    def get_queryset(self):
        return self.all_notify


class NewWall(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.notify = Wall.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_small_template("notify/new_notify.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(NewWall,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(NewWall,self).get_context_data(**kwargs)
		context["object"] = self.notify
		return context
