from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from common.templates import get_full_template
from terms.models import Terms


class TermsView(TemplateView, CategoryListMixin):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.last_version = Terms.objects.all().first()
        self.template_name = get_full_template("terms/" , "terms.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(TermsView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(TermsView,self).get_context_data(**kwargs)
        context["last_version"] = self.last_version
        return context


class WindowAboutView(TemplateView):
    template_name = "terms/window_about.html"
