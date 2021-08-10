from django.views import View
from communities.models import Community


class CommunityLike(View):
    def get(self, request, **kwargs):
        if not request.is_ajax():
            raise Http404
        community = Community.objects.get(pk=self.kwargs["pk"])
        return community.send_like(request.user)

class CommunityDislike(View):
    def get(self, request, **kwargs):
        if not request.is_ajax():
            raise Http404
        community = Community.objects.get(pk=self.kwargs["pk"])
        return community.send_dislike(request.user)

class CommunityInert(View):
    def get(self, request, **kwargs):
        if not request.is_ajax():
            raise Http404
        community = Community.objects.get(pk=self.kwargs["pk"])
        return community.send_inert(request.user)
