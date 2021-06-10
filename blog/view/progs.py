from django.views.generic.base import TemplateView
from django.views import View
from django.http import HttpResponse
from django.http import Http404


class SuggestElectNew(TemplateView):
    template_name = "elect/add_suggest_elect_new.html"

    def get_context_data(self,**kwargs):
        from blog.forms import ElectNewForm
        from elect.models import Elect

        context=super(SuggestElectNew,self).get_context_data(**kwargs)
        context["form"] = ElectNewForm()
        context["get_elects"] = Elect.objects.only("pk")
        return context

    def post(self,request,*args,**kwargs):
        from blog.forms import ElectNewForm
        from elect.models import Elect
        from common.templates import render_for_platform

        self.form_post = ElectNewForm(request.POST)

        if request.is_ajax() and self.form_post.is_valid() and request.user.is_authenticated:
            post = self.form_post.save(commit=False)
            new_post = post.create_suggested_new(creator=request.user, title=post.title, description=post.description, elect=request.POST.get("elect"), attach=request.POST.getlist("attach_items"), category=post.category)
            return render_for_platform(request, 'elect/elect_new.html',{'object': new_post})
        else:
            from django.http import HttpResponseBadRequest
            return HttpResponseBadRequest()

class EditElectNew(TemplateView):
    template_name = "elect/edit_elect_new.html"

    def get(self,request,*args,**kwargs):
        self.new = ElectNew.objects.get(pk=self.kwargs["pk"])
        return super(EditElectNew,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from blog.forms import ElectNewForm
        from elect.models import Elect

        context=super(EditElectNew,self).get_context_data(**kwargs)
        context["form"] = ElectNewForm(instance=self.new)
        context["get_elects"] = Elect.objects.only("pk")
        return context

    def post(self,request,*args,**kwargs):
        from blog.forms import ElectNewForm
        from common.templates import render_for_platform

        self.new = ElectNew.objects.get(pk=self.kwargs["pk"])
        self.form_post = ElectNewForm(request.POST, instance=self.new)

        if request.is_ajax() and self.form_post.is_valid() and request.user.is_authenticated:
            post = self.form_post.save(commit=False)
            new_post = post.edit_new(title=post.title, description=post.description, elect=request.POST.get("elect"), attach=request.POST.getlist("attach_items"), category=post.category)
            return render_for_platform(request, 'elect/elect_new.html',{'object': new_post})
        else:
            from django.http import HttpResponseBadRequest
            return HttpResponseBadRequest()
