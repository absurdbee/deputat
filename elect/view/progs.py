from elect.models import Elect, SubscribeElect
from django.views import View
from django.http import HttpResponse
from django.http import Http404


class ElectSubscribe(View):
    def get(self,request,*args,**kwargs):
        elect = Elect.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_authenticated and not SubscribeElect.is_elect_subscribe(elect.pk, request.user.pk):
            SubscribeElect.create_elect_subscribe(request.user.pk, elect.pk)
            return HttpResponse()
        else:
            raise Http404

class ElectUnSubscribe(View):
    def get(self,request,*args,**kwargs):
        elect = Elect.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_authenticated and SubscribeElect.is_elect_subscribe(elect.pk, request.user.pk):
            subscribe = SubscribeElect.objects.filter(user_id=request.user.pk, elect_id=elect.pk)[0]
            subscribe.delete()
            return HttpResponse()
        else:
            raise Http404


class CreateSuggestElect(TemplateView):
    template_name = "elect/suggest_elect.html"

    def get_context_data(self,**kwargs):
        from elect.forms import ElectForm
        from lists.models import AuthorityList

        context=super(CreateSuggestElect,self).get_context_data(**kwargs)
        context["form"] = ElectForm()
        context["lists"] = AuthorityList.objects.filter(is_active=True)
        return context

    def post(self,request,*args,**kwargs):
        from elect.forms import ElectForm

        self.form_post = ElectForm(request.POST, request.FILES)

        if request.is_ajax() and self.form_post.is_valid() and request.user.is_authenticated:
            post = self.form_post.save(commit=False)
            new_post = post.create_elect(creator=request.user, name=post.name, description=post.description, image=post.image,  list=request.POST.getlist("list"), region=request.POST.getlist("region"), area=request.POST.getlist("area"), birthday=post.birthday, fraction=post.fraction, post_2=post.post_2,vk=post.vk, tg=post.tg, tw=post.tw, ig=post.ig, fb=post.fb, mail=post.mail, phone=post.phone, i_address=post.i_address, address=post.address, site=post.site, type="SUG")
            return HttpResponse()
        else:
            from django.http import HttpResponseBadRequest
            return HttpResponseBadRequest()
