from music.models import *
from django.views import View
from django.views.generic.base import TemplateView
from music.forms import PlaylistForm, TrackForm
from django.http import HttpResponse, HttpResponseBadRequest
from common.parsing_soundcloud.add_playlist import add_playlist
from django.http import Http404
from common.templates import render_for_platform, get_small_template


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

class AddPlayListInUserCollections(View):
    def get(self,request,*args,**kwargs):
        list = SoundList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.is_user_can_add_list(request.user.pk):
            list.users.add(request.user)
        return HttpResponse()

class RemovePlayListFromUserCollections(View):
    def get(self,request,*args,**kwargs):
        list = SoundList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.is_user_can_delete_list(request.user.pk):
            list.users.remove(request.user)
        return HttpResponse()

class UserTrackRemove(View):
    def get(self, request, *args, **kwargs):
        track = Music.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and track.creator.pk == request.user.pk:
            track.delete_track(None)
            return HttpResponse()
        else:
            raise Http404
class UserTrackAbortRemove(View):
    def get(self,request,*args,**kwargs):
        track = Music.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and track.creator == request.user:
            track.abort_delete_track(None)
            return HttpResponse()
        else:
            raise Http404

class AddTrackInUserPlayList(View):
    def get(self, request, *args, **kwargs):
        track = Music.objects.get(pk=self.kwargs["pk"])
        list = SoundList.objects.get(uuid=self.kwargs["uuid"])

        if request.is_ajax() and not list.is_item_in_list(track.pk) and list.creator.pk == request.user.pk:
            list.playlist.add(track)
            return HttpResponse()
        else:
            raise Http404

class RemoveTrackInUserPlayList(View):
    def get(self, request, *args, **kwargs):
        track = Music.objects.get(pk=self.kwargs["pk"])
        list = SoundList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.is_item_in_list(track.pk) and list.creator.pk == request.user.pk:
            list.playlist.remove(track)
            return HttpResponse()
        else:
            raise Http404


class UserPlaylistCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_small_template("user_music/create_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserPlaylistCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserPlaylistCreate,self).get_context_data(**kwargs)
        context["form_post"] = PlaylistForm()
        return context

    def post(self,request,*args,**kwargs):
        form_post = PlaylistForm(request.POST)

        if request.is_ajax() and form_post.is_valid():
            list = form_post.save(commit=False)
            new_list = list.create_list(creator=request.user, name=list.name, description=list.description, order=list.order, community=None,is_public=request.POST.get("is_public"))
            return render_for_platform(request, 'user_music/list/my_list.html',{'list': new_list, 'user': request.user})
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
            new_list = list.edit_list(name=list.name, description=list.description, order=list.order, is_public=request.POST.get("is_public"))
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
        return super(UserPlaylistEdit,self).get(request,*args,**kwargs)

class UserPlaylistDelete(View):
    def get(self,request,*args,**kwargs):
        list = SoundList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.creator.pk == request.user.pk and not list.type == SoundList.MAIN:
            list.delete_list()
            return HttpResponse()
        else:
            raise Http404

class UserPlaylistAbortDelete(View):
    def get(self,request,*args,**kwargs):
        list = SoundList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.creator.pk == request.user.pk:
            list.abort_delete_list()
            return HttpResponse()
        else:
            raise Http404


class UserTrackCreate(TemplateView):
    form_post = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_small_template("user_music/create_track.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserTrackCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserTrackCreate,self).get_context_data(**kwargs)
        context["form_post"] = TrackForm()
        return context

    def post(self,request,*args,**kwargs):
        form_post = TrackForm(request.POST, request.FILES)

        if request.is_ajax() and form_post.is_valid():
            track = form_post.save(commit=False)
            new_track = track.create_track(creator=request.user, title=track.title, file=track.file, lists=request.POST.getlist("list"), is_public=request.POST.get("is_public"), community=None)
            return render_for_platform(request, 'user_music/new_track.html',{'object': new_track})
        else:
            return HttpResponseBadRequest()

class UserTrackEdit(TemplateView):
    form_post = None

    def get(self,request,*args,**kwargs):
        self.track = Music.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_small_template("user_music/edit_track.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserTrackEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserTrackEdit,self).get_context_data(**kwargs)
        context["form_post"] = TrackForm(instance=self.track)
        context["track"] = self.track
        return context

    def post(self,request,*args,**kwargs):
        self.track = Music.objects.get(pk=self.kwargs["pk"])
        form_post = TrackForm(request.POST, request.FILES, instance=self.track)

        if request.is_ajax() and form_post.is_valid():
            _track = form_post.save(commit=False)
            new_doc = _track.edit_track(title=_track.title, file=_track.file, lists=request.POST.getlist("list"), is_public=request.POST.get("is_public"))
            return render_for_platform(request, 'user_music/new_track.html',{'object': self.track})
        else:
            return HttpResponseBadRequest()


class AddTrackInUserMediaList(View):
    def get(self, request, *args, **kwargs):
        track, list = Music.objects.get(pk=self.kwargs["pk"]), request.user.get_or_create_media_list()
        if request.is_ajax() and not list.is_track_in_list(track.pk):
            track.media_list.add(list)
            return HttpResponse()
        else:
            raise Http404

class RemoveTrackInUserMediaList(View):
    def get(self, request, *args, **kwargs):
        track, list = Music.objects.get(pk=self.kwargs["pk"]),request.user.get_or_create_media_list()
        if request.is_ajax() and list.is_track_in_list(track.pk) and list.creator.pk == request.user.pk:
            track.media_list.remove(list)
            return HttpResponse()
        else:
            raise Http404
