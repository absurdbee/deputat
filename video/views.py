from django.views.generic.base import TemplateView
from users.models import User
from common.utils import get_small_template


class AllVideoView(TemplateView):
    template_name="all_video.html"


class UserLoadVideoAlbum(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.album = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
		self.template_name = get_small_template("user_video/list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadVideoAlbum,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(UserLoadVideoAlbum,self).get_context_data(**kwargs)
		c['user'], c['album'] = self.album.creator, self.album
		return c

	def get_queryset(self):
		return self.album.get_videos()
