from django.views import View
from elect.models import Elect
from django.http import Http404
from django.views.generic import ListView


class ElectLike(View):
    def get(self, request, **kwargs):
        if not request.is_ajax():
            raise Http404
        elect = Elect.objects.get(pk=self.kwargs["pk"])
        return elect.send_like(request.user)

class ElectDislike(View):
    def get(self, request, **kwargs):
        if not request.is_ajax():
            raise Http404
        elect = Elect.objects.get(pk=self.kwargs["pk"])
        return elect.send_dislike(request.user)

class ElectInert(View):
    def get(self, request, **kwargs):
        if not request.is_ajax():
            raise Http404
        elect = Elect.objects.get(pk=self.kwargs["pk"])
        return elect.send_inert(request.user)


class ElectSendRating(View):

    def post(self, request, **kwargs):
        if not request.is_ajax():
            raise Http404
        from common.model.votes import ElectRating
        import json
        from django.http import HttpResponse

        vakcine = request.POST.get('vakcine')
        pp_825 = request.POST.get('pp_825')
        safe_family = request.POST.get('safe_family')
        pro_life = request.POST.get('pro_life')
        free_vacation = request.POST.get('free_vacation')

        elect = Elect.objects.get(pk=self.kwargs["pk"])
        if not ElectRating.objects.filter(elect_id=elect.id, user_id=request.user.pk).exists():
            ElectRating.objects.create(elect_id=elect.id, user_id=request.user.pk, vakcine=vakcine,pp_825=pp_825,safe_family=safe_family,pro_life=pro_life,free_vacation=free_vacation)
        else:
            rat = ElectRating.objects.create(elect_id=elect.id, user_id=request.user.pk)
            rat.vakcine = -5
            rat.pp_825 = 5
            rat.safe_family = 0
            rat.pro_life = 2
            rat.free_vacation = 1
            rat.save()

        return HttpResponse()


class ElectDeleteRating(View):
    def get(self, request, **kwargs):
        if not request.is_ajax():
            raise Http404
        from common.model.votes import ElectRating
        from elect.models import Elect
        from django.http import HttpResponse

        elect = Elect.objects.get(pk=self.kwargs["pk"])

        if ElectRating.objects.filter(elect_id=elect.pk, user_id=request.user.pk).exists():
            rat = ElectRating.objects.get(elect_id=elect.pk, user_id=request.user.pk)
            rat.delete()
        return HttpResponse()


class ShowElectRatingVoters(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        from common.templates import get_managers_template

        self.elect = Elect.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_managers_template("elect/load/elect_rating_voters.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(ShowElectRatingVoters,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ShowElectRatingVoters,self).get_context_data(**kwargs)
        context["elect"] = self.elect
        return context

    def get_queryset(self):
        return self.elect.get_ratings()
