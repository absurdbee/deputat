from django.views.generic import ListView
from django.http import Http404
from generic.mixins import CategoryListMixin
from common.templates import get_managers_template
from users.models import User


class ElectNewLogs(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        if request.user.is_supermanager():
            self.user = User.objects.get(pk=self.kwargs["pk"])
            self.template_name = get_managers_template("managers/logs/elect_new.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ElectNewLogs,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ElectNewLogs,self).get_context_data(**kwargs)
        context["user"] = self.user
        return context

    def get_queryset(self):
        from logs.model.manage_elect_new import ElectNewManageLog

        return ElectNewManageLog.objects.filter(manager=self.user.pk)
