from django.views.generic.base import TemplateView
from music.models import *
from django.views.generic import ListView
from common.templates import get_small_template
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
        from common.templates import get_template_user_item, get_template_anon_user_item

        pk = self.kwargs["pk"]
        self.user = User.objects.get(pk=pk)
        self.list = self.user.get_or_create_main_playlist()
        if self.user.pk == request.user.pk:
            self.music_list = self.list.get_my_playlist()
            self.is_have_lists = self.list.is_have_my_lists(pk)
            self.get_lists = self.list.get_my_lists(pk)
        else:
            self.music_list = self.list.get_playlist()
            self.is_have_lists = self.list.is_have_lists(pk)
            self.get_lists = self.list.get_lists(pk)
        self.count_lists = self.list.get_lists_count(pk)
        if request.user.is_authenticated:
            self.template_name = get_template_user_item(self.list, "user_music/main/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_audio_manager())
        else:
            self.template_name = get_template_anon_user_item(self.list, "user_music/main/anon_list.html", request.META['HTTP_USER_AGENT'])
        return super(UserMusic,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(UserMusic,self).get_context_data(**kwargs)
        c['user'], c['playlist'], c['is_have_lists'], c['get_lists'], c['count_lists'] = self.user, self.list, self.is_have_lists, self.get_lists, self.count_lists
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
            self.music_list = self.list.get_my_playlist()
        else:
            self.music_list = self.list.get_playlist()
        if request.user.is_authenticated:
            self.template_name = get_template_user_item(self.list, "user_music/list/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_audio_manager())
        else:
            self.template_name = get_template_anon_user_item(self.list, "user_music/list/anon_list.html", request.META['HTTP_USER_AGENT'])
        return super(UserMusicList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserMusicList,self).get_context_data(**kwargs)
        context['user'] = self.list.creator
        context['playlist'] = self.list
        return context

    def get_queryset(self):
        return self.music_list


class UserLoadPlaylist(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        from common.templates import get_template_user_window, get_template_anon_user_window

        self.list = SoundList.objects.get(pk=self.kwargs["pk"])
        if self.list.creator.pk == request.user.pk:
            self.music_list = self.list.get_my_playlist()
        else:
            self.music_list = self.list.get_playlist()
        if request.user.is_authenticated:
            self.template_name = get_template_user_item(self.list, "user_music/load/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_audio_manager())
        else:
            self.template_name = get_template_anon_user_item(self.list, "user_music/load/anon_list.html", request.META['HTTP_USER_AGENT'])
        return super(UserLoadPlaylist,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserLoadPlaylist,self).get_context_data(**kwargs)
        context['playlist'] = self.list
        return context

    def get_queryset(self):
        return self.music_list
