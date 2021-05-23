from django.views.generic.base import TemplateView
from django.views import View
from django.http import HttpResponse
from django.http import Http404


class SuggestElectNew(TemplateView):
    template_name = "elect/suggest_elect_new.html"

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
            elect = Elect.objects.get(name=post.elect)
            #new_post = post.create_suggested_new(creator=request.user, title=post.title, description=post.description, elect=elect, attach=request.POST.getlist("attach_items"), category=post.category)
            return HttpResponse(post.elect)
            return render_for_platform(request, 'elect/elect_new.html',{'object': new_post})
        else:
            from django.http import HttpResponseBadRequest
            return HttpResponseBadRequest()

class PublishElectNew(View):
    template_name = "elect/publish_elect_new.html"

    def get(self,request,*args,**kwargs):
        self.elect_new = ElectNew.objects.get(pk=self.kwargs["pk"])
        return super(PublishElectNew,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from blog.forms import ElectNewForm

        context=super(PublishElectNew,self).get_context_data(**kwargs)
        context["form"] = ElectNewForm()
        context["object"] = self.elect_new
        return context

    def post(self,request,*args,**kwargs):
        from blog.forms import ElectNewForm
        from common.templates import render_for_platform

        self.elect_new = ElectNew.objects.get(pk=self.kwargs["pk"])
        self.form_post = ElectNewForm(request.POST, instance=self.elect_new)

        if request.is_ajax() and self.form_post.is_valid() and request.user.is_authenticated:
            post = self.form_post.save(commit=False)
            new_post = post.make_publish_new(title=post.title, description=post.description, elect=post.elect, attach=request.POST.getlist("attach_items"), category=post.category)
            return render(request, 'elect/elect_new.html', {'object': new_post})
            return render_for_platform(request, 'elect/elect_new.html',{'object': new_post})
        else:
            from django.http import HttpResponseBadRequest
            return HttpResponseBadRequest()
