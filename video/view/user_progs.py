from video.models import Video, VideoList
from users.models import User
from django.views import View
from django.views.generic.base import TemplateView
from video.forms import VideoListForm, VideoForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.http import Http404
from common.templates import render_for_platform, get_small_template


class AddVideoListInUserCollections(View):
    def get(self,request,*args,**kwargs):
        list = VideoList.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and list.is_user_can_add_list(request.user.pk):
            list.users.add(request.user)
        return HttpResponse()

class RemoveVideoListFromUserCollections(View):
    def get(self,request,*args,**kwargs):
        list = VideoList.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and list.is_user_can_delete_list(request.user.pk):
            list.users.remove(request.user)
        return HttpResponse()


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


class UserVideoRemove(View):
    def get(self, request, *args, **kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and video.creator.pk == request.user.pk:
            video.delete_video(None)
            return HttpResponse(None)
        else:
            raise Http404

class UserVideoAbortRemove(View):
    def get(self, request, *args, **kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and video.creator.pk == request.user.pk:
            video.abort_delete_video(None)
            return HttpResponse()
        else:
            raise Http404

class AddVideoInUserVideoList(View):
    def get(self, request, *args, **kwargs):
        video, list = Video.objects.get(pk=self.kwargs["pk"]), VideoList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and not list.is_item_in_list(video.pk) and list.creator.pk == request.user.pk :
            list.video_list.add(video)
            return HttpResponse()
        else:
            raise Http404

class RemoveVideoInUserVideoList(View):
    def get(self, request, *args, **kwargs):
        video, list = Video.objects.get(pk=self.kwargs["pk"]), VideoList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.is_item_in_list(video.pk) and list.creator.pk == request.user.pk:
            list.video_list.remove(video)
            return HttpResponse()
        else:
            raise Http404

class UserVideolistCreate(TemplateView):
    form_post = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_small_template("user_video/create_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserVideolistCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserVideolistCreate,self).get_context_data(**kwargs)
        context["form_post"] = VideoListForm()
        return context

    def post(self,request,*args,**kwargs):
        form_post= VideoListForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            list = form_post.save(commit=False)
            new_list = list.create_list(creator=request.user, name=list.name, description=list.description, order=list.order, community=None, is_public=request.POST.get("is_public"))
            return render_for_platform(request, 'user_video/list/my_list.html',{'list': new_list})
        else:
            return HttpResponseBadRequest()


class UserVideolistEdit(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_small_template("user_video/edit_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserVideolistEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserVideolistEdit,self).get_context_data(**kwargs)
        context["list"] = VideoList.objects.get(uuid=self.kwargs["uuid"])
        return context

    def post(self,request,*args,**kwargs):
        self.list = VideoList.objects.get(uuid=self.kwargs["uuid"])
        self.form = VideoListForm(request.POST,instance=self.list)
        if request.is_ajax() and self.form.is_valid():
            list = self.form.save(commit=False)
            list.edit_list(name=list.name, description=list.description, order=list.order, is_public=request.POST.get("is_public"))
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
        return super(UserVideolistEdit,self).get(request,*args,**kwargs)


class UserVideoCreate(TemplateView):
    form_post = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_small_template("user_video/create_video.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserVideoCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserVideoCreate,self).get_context_data(**kwargs)
        context["form_post"] = VideoForm()
        return context

    def post(self,request,*args,**kwargs):
        form_post = VideoForm(request.POST, request.FILES)

        if request.is_ajax() and form_post.is_valid():
            video = form_post.save(commit=False)
            new_video = Video.create_video(creator=request.user, title=video.title, file=video.file, image=video.image, uri=video.uri, lists=request.POST.getlist("list"), is_public=request.POST.get("is_public"), community=None)
            return render_for_platform(request, 'user_video/new_video.html',{'object': new_video})
        else:
            return HttpResponseBadRequest()

class UserVideoEdit(TemplateView):
    form_post = None

    def get(self,request,*args,**kwargs):
        self.video = Video.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_small_template("user_video/edit_video.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserVideoEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserVideoEdit,self).get_context_data(**kwargs)
        context["form_post"] = VideoForm(instance=self.video)
        context["video"] = self.video
        return context

    def post(self,request,*args,**kwargs):
        self.video = Video.objects.get(pk=self.kwargs["pk"])
        form_post = VideoForm(request.POST, request.FILES, instance=self.video)

        if request.is_ajax() and form_post.is_valid():
            _video = form_post.save(commit=False)
            new_video = self.video.edit_video(title=_video.title, file=_video.file, lists=request.POST.getlist("list"), is_public=request.POST.get("is_public"))
            return render_for_platform(request, 'user_video/new_video.html',{'video': self.video})
        else:
            return HttpResponseBadRequest()


class UserVideolistDelete(View):
    def get(self,request,*args,**kwargs):
        list = VideoList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.creator.pk == request.user.pk and list.type != VideoList.MAIN:
            list.delete_list()
            return HttpResponse()
        else:
            raise Http404

class UserVideolistAbortDelete(View):
    def get(self,request,*args,**kwargs):
        list = VideoList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.creator.pk == request.user.pk:
            list.abort_delete_list()
            return HttpResponse()
        else:
            raise Http404
