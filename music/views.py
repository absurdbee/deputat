from django.views.generic.base import TemplateView
from music.models import *
from django.views.generic import ListView
from common.templates import get_small_template
from users.models import User
from generic.mixins import CategoryListMixin


class UserTrackDetail(TemplateView, CategoryListMixin):
	template_name = None

	def get(self,request,*args,**kwargs):
		from common.templates import get_full_template

		self.track = Music.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_full_template("music/detail/user/", "u.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserTrackDetail,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(UserTrackDetail,self).get_context_data(**kwargs)
		context["object"] = self.track
		return context

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
        from common.templates import get_template_user_item, get_template_anon_user_item
		from django.conf import settings

        pk = int(self.kwargs["pk"])
        self.user = User.objects.get(pk=pk)
        self.list = self.user.get_playlist()
        if pk == request.user.pk:
            self.music_list = self.list.get_staff_items()
            self.get_lists = self.list.get_user_staff_lists(pk)
			if self.count_lists < settings.USER_MAX_MUSIC_LISTS:
				self.can_add_list = True
        else:
            self.music_list = self.list.get_items()
            self.get_lists = self.list.get_user_lists(pk)
        self.count_lists = self.list.get_user_lists_count(pk)
        if request.user.is_authenticated:
            self.template_name = get_template_user_item(self.list, "user_music/main/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_audio_manager())
        else:
            self.template_name = get_template_anon_user_item(self.list, "user_music/main/", "list.html", request.META['HTTP_USER_AGENT'])
        return super(UserMusic,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(UserMusic,self).get_context_data(**kwargs)
        c['user'], c['list'], c['get_lists'], c['count_lists'], c['can_add_list'] = self.user, self.list, self.get_lists, self.count_lists, self.can_add_list
        return c

    def get_queryset(self):
        return self.music_list


class UserMusicList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        from music.models import SoundList
        from common.templates import get_template_user_item, get_template_anon_user_item

        self.list = SoundList.objects.get(uuid=self.kwargs["uuid"])
        if self.list.creator.pk == request.user.pk:
            self.music_list = self.list.get_staff_items()
        else:
            self.music_list = self.list.get_items()
        if request.user.is_authenticated:
            self.template_name = get_template_user_item(self.list, "user_music/list/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_audio_manager())
        else:
            self.template_name = get_template_anon_user_item(self.list, "user_music/list/", "list.html", request.META['HTTP_USER_AGENT'])
        return super(UserMusicList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserMusicList,self).get_context_data(**kwargs)
        context['user'], context['list'] = self.list.creator, self.list
        return context

    def get_queryset(self):
        return self.music_list


class UserLoadPlaylist(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        from common.templates import get_template_user_window, get_template_anon_user_window

        self.list = SoundList.objects.get(pk=self.kwargs["pk"])
        if self.list.creator.pk == request.user.pk:
            self.music_list = self.list.get_staff_items()
        else:
            self.music_list = self.list.get_items()
        if request.user.is_authenticated:
            self.template_name = get_template_user_window(self.list, "user_music/load/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_audio_manager())
        else:
            self.template_name = get_template_anon_user_window(self.list, "user_music/load/", "list.html", request.META['HTTP_USER_AGENT'])
        return super(UserLoadPlaylist,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserLoadPlaylist,self).get_context_data(**kwargs)
        context['list'] = self.list
        return context

    def get_queryset(self):
        return self.music_list


class UserLoadPenaltyPlaylist(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from common.templates import get_managers_template

		self.list = SoundList.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_managers_template("user_music/load/penalty_list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadPenaltyPlaylist,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadPenaltyPlaylist,self).get_context_data(**kwargs)
		context['list'] = self.list
		return context

	def get_queryset(self):
		return self.list.get_penalty_items()

class UserLoadModeratedPlaylist(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from common.templates import get_managers_template

		self.list = SoundList.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_managers_template("user_music/load/moderated_list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadModeratedPlaylist,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadModeratedPlaylist,self).get_context_data(**kwargs)
		context['list'] = self.list
		return context

	def get_queryset(self):
		return self.list.get_items()
