from django.views.generic.base import TemplateView
from django.views import View
from django.http import HttpResponse
from django.http import Http404


class ElectNewCreate(View):
    template_name = "elect/add_new.html"

    def get(self,request,*args,**kwargs):
        from elect.models import Elect

        self.elect = Elect.objects.get(pk=self.kwargs["pk"])
        return super(ElectNewCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from blog.forms import ElectNewForm

        context=super(ElectNewCreate,self).get_context_data(**kwargs)
        context["form"] = ElectNewForm()
        return context

    def post(self,request,*args,**kwargs):
        from blog.forms import ElectNewForm
        from django.shortcuts import render
        from elect.models import Elect

        self.form_post = ElectNewForm(request.POST)
        self.elect = Elect.objects.get(pk=self.kwargs["pk"])

        if request.is_ajax() and self.form_post.is_valid() and request.user.is_authenticated:
            post = self.form_post.save(commit=False)
            post.creator = request.user
            post.save()
            return render(request, 'elect/elect_new.html', {'object': new_post})
        else:
            from django.http import HttpResponseBadRequest
            return HttpResponseBadRequest()
