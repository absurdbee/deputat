from django.views.generic.base import TemplateView
from elect.models import Elect, SubscribeElect
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest
from elect.forms import ElectNewForm
from users.models import User
from django.http import Http404
from django.shortcuts import render


class ElectSubscribe(View):
    def get(self,request,*args,**kwargs):
        elect = Elect.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and not SubscribeElect.is_elect_subscribe(elect.pk, request.user.pk):
            SubscribeElect.create_elect_subscribe(request.user.pk, elect.pk)
        else:
            raise Http404

class ElectUnSubscribe(View):
    def get(self,request,*args,**kwargs):
        elect = Elect.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and SubscribeElect.is_elect_subscribe(elect.pk, request.user.pk):
            subscribe = SubscribeElect.objects.filter(user_id=request.user.pk, elect_id=elect.pk)[0]
            subscribe.delete()
            return HttpResponse()
        else:
            raise Http404


class ElectNewCreate(View):
    template_name = "elect/add_new.html"

    def get(self,request,*args,**kwargs):
        self.elect = Elect.objects.get(pk=self.kwargs["pk"])
        return super(ElectNewCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ElectNewCreate,self).get_context_data(**kwargs)
        context["form"] = ElectNewForm()
        return context

    def post(self,request,*args,**kwargs):
        self.form_post = ElectNewForm(request.POST)
        self.elect = Elect.objects.get(pk=self.kwargs["pk"])

        if request.is_ajax() and self.form_post.is_valid() and request.user.is_authenticated:
            post = self.form_post.save(commit=False)
            post.creator = request.user
            post.save()
            return render(request, 'elect/elect_new.html', {'object': new_post})
        else:
            return HttpResponseBadRequest()
