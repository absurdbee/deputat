from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from common.templates import get_small_template
from policy.models import Policy


class PolicyView(TemplateView, CategoryListMixin):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.last_version = Policy.objects.all().first()
        self.template_name = get_small_template("policy/policy.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(PolicyView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PolicyView,self).get_context_data(**kwargs)
        context["last_version"] = self.last_version
        return context
