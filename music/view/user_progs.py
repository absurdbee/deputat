from music.models import *
from users.models import User
from django.views import View
from django.views.generic.base import TemplateView
from music.forms import PlaylistForm
from django.http import HttpResponse, HttpResponseBadRequest
from common.parsing_soundcloud.add_playlist import add_playlist
from django.http import Http404


class UserSoundcloudSetCreate(TemplateView):
    form_post = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_small_template("user_music/soundcloud_add_playlist.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserSoundcloudSetCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserSoundcloudSetCreate,self).get_context_data(**kwargs)
        context["form_post"] = PlaylistForm()
        return context

    def post(self,request,*args,**kwargs):
        form_post = PlaylistForm(request.POST)

        if request.is_ajax() and form_post.is_valid():
            new_list = form_post.save(commit=False)
            new_list.creator = request.user
            new_list.save()
            add_playlist(request.POST.get('permalink'), request.user, new_list)
            return render_for_platform(request, 'user_music/list.html',{'playlist': new_list, 'object_list': new_list.playlist_too(),'user': request.user})
        else:
            return HttpResponseBadRequest()

class UserSoundcloudSet(TemplateView):
    def get(self,request,*args,**kwargs):
        self.template_name = get_small_template("user_music/soundcloud_set_playlist.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserSoundcloudSet,self).get(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        list = SoundList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax():
            add_playlist(request.POST.get('permalink'), request.user, list)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class UserPlaylistAdd(View):
    def get(self,request,*args,**kwargs):
        list = SoundList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.is_user_can_add_list(request.user.pk):
            list.users.add(request.user)
            return HttpResponse()
        else:
            return HttpResponse()

class UserPlaylistRemove(View):
    def get(self,request,*args,**kwargs):
        list = SoundList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.is_user_can_delete_list(request.user.pk):
            list.users.remove(request.user)
            return HttpResponse()
        else:
            return HttpResponse()

class UserTrackRemove(View):
    def get(self, request, *args, **kwargs):
        track = Music.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and track.creator.pk == request.user.pk:
            track.delete_track()
            return HttpResponse()
        else:
            raise Http404
class UserTrackAbortRemove(View):
    def get(self,request,*args,**kwargs):
        track = Music.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and video.creator == request.user:
            track.abort_delete_track()
            return HttpResponse()
        else:
            raise Http404

class UserTrackListAdd(View):
    def get(self, request, *args, **kwargs):
        track = Music.objects.get(pk=self.kwargs["pk"])
        list = SoundList.objects.get(uuid=self.kwargs["uuid"])

        if request.is_ajax() and not list.is_track_in_list(track.pk):
            list.players.add(track)
            return HttpResponse()
        else:
            raise Http404

class UserTrackListRemove(View):
    def get(self, request, *args, **kwargs):
        track = Music.objects.get(pk=self.kwargs["pk"])
        list = SoundList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.is_track_in_list(track.pk):
            list.players.remove(track)
            return HttpResponse()
        else:
            raise Http404


class UserPlaylistCreate(View):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_small_template("user_music/create_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserCreatePlaylistWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserPlaylistCreate,self).get_context_data(**kwargs)
        context["form_post"] = PlaylistForm()
        return context

    def post(self,request,*args,**kwargs):
        form_post = PlaylistForm(request.POST)

        if request.is_ajax() and form_post.is_valid():
            new_list = form_post.save(commit=False)
            new_list.creator = request.user
            if not new_list.order:
                new_list.order = 0
            new_list.save()
            return render_for_platform(request, 'users/user_music_list/my_list.html',{'playlist': new_list, 'user': request.user})
        else:
            return HttpResponseBadRequest()


class UserPlaylistEdit(TemplateView):
    template_name = None
    form=None

    def get(self,request,*args,**kwargs):
        self.user = request.user
        self.template_name = get_small_template("user_music/edit_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserPlaylistEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserPlaylistEdit,self).get_context_data(**kwargs)
        context["user"] = self.user
        context["list"] = SoundList.objects.get(uuid=self.kwargs["uuid"])
        return context

    def post(self,request,*args,**kwargs):
        self.list = SoundList.objects.get(uuid=self.kwargs["uuid"])
        self.form = PlaylistForm(request.POST,instance=self.list)
        if request.is_ajax() and self.form.is_valid():
            list = self.form.save(commit=False)
            self.form.save()
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
        return super(UserPlaylistEdit,self).get(request,*args,**kwargs)

class UserPlaylistDelete(View):
    def get(self,request,*args,**kwargs):
        list = SoundList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.type == SoundList.LIST:
            list.is_deleted = True
            list.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class UserPlaylistAbortDelete(View):
    def get(self,request,*args,**kwargs):
        list = SoundList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax():
            list.is_deleted = False
            list.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404
