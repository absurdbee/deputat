from django.views.generic.base import TemplateView
from music.models import *
from django.views.generic import ListView
from common.utils import get_small_template


class AllMusicView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_small_template("music/all.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(AllMusicView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllMusicView,self).get_context_data(**kwargs)
        return context

class UserLoadPlaylist(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.playlist = SoundList.objects.get(uuid=self.kwargs["uuid"])
		self.template_name = get_small_template("user_music/load_list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadPlaylist,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadPlaylist,self).get_context_data(**kwargs)
		context['user'] = self.user
		context['playlist'] = self.playlist
		return context

	def get_queryset(self):
		playlist = self.playlist.playlist_too()
		return playlist


class MusicPlaylistPreview(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.playlist, self.template_name = SoundList.objects.get(pk=self.kwargs["pk"]), get_small_template("user_music/playlist_preview.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(MusicPlaylistPreview,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(MusicPlaylistPreview,self).get_context_data(**kwargs)
		context["playlist"] = self.playlist
		return context
