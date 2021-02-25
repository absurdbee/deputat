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
