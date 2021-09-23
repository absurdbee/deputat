from django.views import View
from users.models import User
from django.http import HttpResponse, HttpResponseBadRequest
from common.staff_progs.video import *
from video.models import Video, VideoList
from managers.forms import ModeratedForm
from django.views.generic.base import TemplateView
from managers.models import Moderated
from django.http import Http404
from common.templates import get_detect_platform_template, render_for_platform
from logs.model.manage_video import VideoManageLog


class VideoAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_video_administrator():
            add_video_administrator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class VideoAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_video_administrator():
            remove_video_administrator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class VideoModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_video_moderator():
            add_video_moderator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class VideoModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_video_moderator():
            remove_video_moderator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class VideoEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_video_editor():
            add_video_editor(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class VideoEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_video_editor():
            remove_video_editor(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class VideoWorkerAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_video_administrator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class VideoWorkerAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_video_administrator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class VideoWorkerModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_video_moderator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class VideoWorkerModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_video_moderator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class VideoWorkerEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_video_editor_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class VideoWorkerEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_video_editor_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class VideoCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.video = Video.objects.get(uuid=self.kwargs["uuid"])
        if request.user.is_video_manager():
            self.template_name = get_detect_platform_template("managers/manage_create/video/video_close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(VideoCloseCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(VideoCloseCreate,self).get_context_data(**kwargs)
        context["object"] = self.video
        return context

    def post(self,request,*args,**kwargs):
        video, form = Video.objects.get(uuid=self.kwargs["uuid"]), ModeratedForm(request.POST)
        if request.is_ajax() and form.is_valid() and request.user.is_video_manager():
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=video.pk, type="VID")
            moderate_obj.create_close(object=video, description=mod.description, manager_id=request.user.pk)
            VideoManageLog.objects.create(item=video.pk, manager=request.user.pk, action_type=VideoManageLog.ITEM_CLOSED)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class VideoCloseDelete(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_video_manager():
            moderate_obj = Moderated.objects.get(object_id=video.pk, type="VID")
            moderate_obj.delete_close(object=video, manager_id=request.user.pk)
            VideoManageLog.objects.create(item=video.pk, manager=request.user.pk, action_type=VideoManageLog.ITEM_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404

class VideoClaimCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.video = Video.objects.get(uuid=self.kwargs["uuid"])
        self.is_reported = ModerationReport.is_user_already_reported(request.user.pk, 'VID', self.video.pk)
        self.template_name = get_detect_platform_template("managers/manage_create/video/video_claim.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(VideoClaimCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(VideoClaimCreate,self).get_context_data(**kwargs)
        context["object"] = self.video
        context["is_reported"] = self.is_reported
        return context

    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and not ModerationReport.is_user_already_reported(request.user.pk, 'VID', video.pk):
            description = request.POST.get('description')
            type = request.POST.get('type')
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type="VID", object_id=video.pk, description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class VideoRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_video_manager():
            moderate_obj = Moderated.objects.get(object_id=video.pk, type="VID")
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            VideoManageLog.objects.create(item=video.pk, manager=request.user.pk, action_type=VideoManageLog.REJECT)
            return HttpResponse()
        else:
            raise Http404

class VideoUnverify(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["video_uuid"])
        obj = Moderated.get_or_create_moderated_object(object_id=video.pk, type="VID")
        if request.is_ajax() and request.user.is_video_manager():
            obj.unverify_moderation(video, manager_id=request.user.pk)
            VideoManageLog.objects.create(item=video.pk, manager=request.user.pk, action_type=VideoManageLog.UNVERIFY)
            return HttpResponse()
        else:
            raise Http404


class ListVideoClaimCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.list = VideoList.objects.get(uuid=self.kwargs["uuid"])
        self.is_reported = ModerationReport.is_user_already_reported(request.user.pk, 'VIL', self.list.pk)
        self.template_name = get_detect_platform_template("managers/manage_create/video/list_claim.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(ListVideoClaimCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ListVideoClaimCreate,self).get_context_data(**kwargs)
        context["object"] = self.list
        context["is_reported"] = self.is_reported
        return context

    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.list = VideoList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and not ModerationReport.is_user_already_reported(request.user.pk, 'VIL', self.list.pk):
            description = request.POST.get('description')
            type = request.POST.get('type')
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type="VIL", object_id=self.list.pk, description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class ListVideoRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        list = VideoList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_video_manager():
            moderate_obj = Moderated.objects.get(object_id=list.pk, type="VIL")
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            VideoManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=VideoManageLog.LIST_REJECT)
            return HttpResponse()
        else:
            raise Http404


class ListVideoUnverify(View):
    def get(self,request,*args,**kwargs):
        list = VideoList.objects.get(uuid=self.kwargs["uuid"])
        obj = Moderated.get_or_create_moderated_object(object_id=list.pk, type="VIL")
        if request.is_ajax() and request.user.is_video_manager():
            obj.unverify_moderation(list, manager_id=request.user.pk)
            VideoManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=VideoManageLog.LIST_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404

class ListVideoCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.list = VideoList.objects.get(uuid=self.kwargs["uuid"])
        if request.user.is_video_manager():
            self.template_name = get_detect_platform_template("managers/manage_create/video/list_close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ListVideoCloseCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ListVideoCloseCreate,self).get_context_data(**kwargs)
        context["object"] = self.list
        return context

    def post(self,request,*args,**kwargs):
        list = VideoList.objects.get(uuid=self.kwargs["uuid"])
        form = ModeratedForm(request.POST)
        if form.is_valid() and request.user.is_video_manager():
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=list.pk, type="VIL")
            moderate_obj.create_close(object=list, description=mod.description, manager_id=request.user.pk)
            VideoManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=VideoManageLog.LIST_CLOSED)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class ListVideoCloseDelete(View):
    def get(self,request,*args,**kwargs):
        list = VideoList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_video_manager():
            moderate_obj = Moderated.objects.get(object_id=list.pk, type="VIL")
            moderate_obj.delete_close(object=list, manager_id=request.user.pk)
            VideoManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=VideoManageLog.LIST_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404


class CreateManagerVideo(TemplateView):
    form_post = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_detect_platform_template("managers/manage_create/video/create_video.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(CreateManagerVideo,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from video.forms import VideoForm
        from video.models import VideoList

        context = super(CreateManagerVideo,self).get_context_data(**kwargs)
        context["form_post"] = VideoForm()
        context["get_lists"] = VideoList.objects.filter(type=VideoList.MANAGER)
        return context

    def post(self,request,*args,**kwargs):
        from video.forms import VideoForm
        form_post = VideoForm(request.POST, request.FILES)

        if request.is_ajax() and form_post.is_valid():
            video = form_post.save(commit=False)
            new_video = Video.create_manager_video(creator=request.user, title=video.title, file=video.file, image=video.image, uri=video.uri, lists=request.POST.getlist("list"))
            return render_for_platform(request, 'user_video/new_video.html',{'object': new_video})
        else:
            return HttpResponseBadRequest()

class EditManagerVideo(TemplateView):
    form_post = None

    def get(self,request,*args,**kwargs):
        self.video = Video.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_detect_platform_template("managers/manage_create/video/edit_video.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(EditManagerVideo,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from video.forms import VideoForm
        from video.models import VideoList

        context = super(EditManagerVideo,self).get_context_data(**kwargs)
        context["form_post"] = VideoForm(instance=self.video)
        context["video"] = self.video
        context["get_lists"] = VideoList.objects.filter(type=VideoList.MANAGER)
        return context

    def post(self,request,*args,**kwargs):
        from video.forms import VideoForm
        self.video = Video.objects.get(pk=self.kwargs["pk"])
        form_post = VideoForm(request.POST, request.FILES, instance=self.video)

        if request.is_ajax() and form_post.is_valid():
            _video = form_post.save(commit=False)
            new_video = self.video.edit_manager_video(title=_video.title, image=_video.image, uri=_video.uri, file=_video.file, lists=request.POST.getlist("list"), manager_id=request.user.pk)
            return render_for_platform(request, 'user_video/new_video.html',{'object': self.video})
        else:
            return HttpResponseBadRequest()


class CreateManagerVideoList(TemplateView):
    def get(self,request,*args,**kwargs):
        self.template_name = get_detect_platform_template("managers/manage_create/video/create_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(CreateManagerVideoList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from video.forms import VideoListForm
        context = super(CreateManagerVideoList,self).get_context_data(**kwargs)
        context["form_post"] = VideoListForm()
        return context

    def post(self,request,*args,**kwargs):
        from video.forms import VideoListForm
        form_post= VideoListForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            list = form_post.save(commit=False)
            new_list = list.create_manager_list(creator=request.user, name=list.name, description=list.description, order=list.order)
            return render_for_platform(request, 'user_video/list/my_list.html',{'list': new_list})
        else:
            return HttpResponseBadRequest()


class EditManagerVideoList(TemplateView):
    def get(self,request,*args,**kwargs):
        self.template_name = get_detect_platform_template("managers/manage_create/video/edit_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(EditManagerVideoList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from video.forms import VideoListForm
        context = super(EditManagerVideoList,self).get_context_data(**kwargs)
        context["list"] = VideoList.objects.get(uuid=self.kwargs["uuid"])
        return context

    def post(self,request,*args,**kwargs):
        from video.forms import VideoListForm
        self.list = VideoList.objects.get(uuid=self.kwargs["uuid"])
        self.form = VideoListForm(request.POST,instance=self.list)
        if request.is_ajax() and self.form.is_valid():
            list = self.form.save(commit=False)
            list.edit_manager_list(name=list.name, description=list.description, order=list.order, manager_id=request.user.pk)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
        return super(EditManagerVideoList,self).get(request,*args,**kwargs)
