from users.models import User
from video.models import Video, VideoAlbum
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.views import View
from video.forms import AlbumForm, VideoForm
from common.templates import get_small_template


class UserVideoAlbumAdd(View):
    def get(self,request,*args,**kwargs):
        list = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.is_user_can_add_list(request.user.pk):
            list.users.add(request.user)
        return HttpResponse()

class UserVideoAlbumRemove(View):
    def get(self,request,*args,**kwargs):
        list = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.is_user_can_delete_list(request.user.pk):
            list.users.remove(request.user)
        return HttpResponse()


class UserVideoDelete(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and video.creator.pk == request.user.pk:
            video.delete_video()
            return HttpResponse()
        else:
            raise Http404

class UserVideoAbortDelete(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and video.creator.pk == request.user.pk:
            video.abort_delete_video()
            return HttpResponse()
        else:
            raise Http404


class UserOnPrivateVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and video.creator.pk == request.user.pk:
            video.make_private()
            return HttpResponse()
        else:
            raise Http404

class UserOffPrivateVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and video.creator.pk == request.user.pk:
            video.make_publish()
            return HttpResponse()
        else:
            raise Http404

class UserVideolistDelete(View):
    def get(self,request,*args,**kwargs):
        list = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.creator.pk == request.user.pk and list.type == VideoAlbum.ALBUM:
            list.delete_list()
            return HttpResponse()
        else:
            raise Http404

class UserVideolistAbortDelete(View):
    def get(self,request,*args,**kwargs):
        list = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.creator.pk == request.user.pk:
            list.abort_delete_list()
            return HttpResponse()
        else:
            raise Http404

class UserVideoListAdd(View):
    def get(self, request, *args, **kwargs):
        video, list = Video.objects.get(pk=self.kwargs["pk"]), VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and not list.is_item_in_list(video.pk):
            list.video_album.add(video)
            return HttpResponse()
        else:
            raise Http404

class UserVideoListRemove(View):
    def get(self, request, *args, **kwargs):
        video, list = Video.objects.get(pk=self.kwargs["pk"]), VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.is_item_in_list(video.pk):
            list.video_album.remove(video)
            return HttpResponse()
        else:
            raise Http404
