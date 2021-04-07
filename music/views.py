from django.views.generic.base import TemplateView
from music.models import *
from django.views.generic import ListView
from common.templates import get_small_template, get_list_template
from users.models import User


class AllMusicView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_small_template("music/all.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(AllMusicView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllMusicView,self).get_context_data(**kwargs)
        return context


class UserMusic(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.list = self.user.get_or_create_main_playlist()
		if self.user.pk == request.user.pk:
			self.music_list = self.list.get_my_playlist()
		else:
			self.music_list = self.list.get_playlist()
		self.template_name = get_list_template(self.list, "user_music/", "music.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserMusic,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserMusic,self).get_context_data(**kwargs)
		context['user'] = self.user
		context['list'] = self.list
		return context

	def get_queryset(self):
		return self.music_list


class UserMusicList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from music.models import SoundList

		self.list = SoundList.objects.get(uuid=self.kwargs["uuid"])
		self.user = User.objects.get(pk=self.kwargs["pk"])
		if self.user.pk == request.user.pk:
			self.music_list = self.list.get_my_playlist()
		else:
			self.music_list = self.list.get_playlist()
		self.template_name = get_list_template(self.list, "user_docs/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserMusicList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserMusicList,self).get_context_data(**kwargs)
		context['user'] = self.user
		context['list'] = self.list
		return context

	def get_queryset(self):
		return self.music_list


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
