from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from common.utils import get_small_template


class PolicyView(TemplateView, CategoryListMixin):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_small_template("policy/policy.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(PolicyView,self).get(request,*args,**kwargs)
