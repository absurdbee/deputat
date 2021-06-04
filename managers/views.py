from django.views.generic.base import TemplateView
from django.views.generic import ListView
from common.templates import get_managers_template


class ManagersView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        if request.user.is_manager() or request.user.is_superuser:
            self.template_name = get_managers_template("managers/managers.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(ManagersView,self).get(request,*args,**kwargs)

class SuperManagersView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        if request.user.is_supermanager() or request.user.is_superuser:
            self.template_name = get_managers_template("managers/managers.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(SuperManagersView,self).get(request,*args,**kwargs)


class LoadClaims(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        from managers.models import Moderated

        self.obj = Moderated.objects.get(pk=self.kwargs["pk"])
        if request.user.is_manager():
            self.template_name = get_managers_template("managers/claims.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(LoadClaims,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(LoadClaims,self).get_context_data(**kwargs)
        context["report"] = self.obj
        return context

    def get_queryset(self):
        return self.obj.reports.all()
