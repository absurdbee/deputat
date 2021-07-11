from django.views import View
from elect.models import Elect


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
