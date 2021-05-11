from django.views import View
from users.models import User
from django.http import HttpResponse, HttpResponseBadRequest
from common.staff_progs.video import *
from video.models import Video, VideoComment
from managers.forms import ModeratedForm
from django.views.generic.base import TemplateView
from managers.models import Moderated
from django.http import Http404
from common.templates import get_detect_platform_template


class VideoAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_video_administrator()):
            add_video_administrator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class VideoAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_video_administrator()):
            remove_video_administrator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class VideoModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_video_moderator()):
            add_video_moderator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class VideoModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_video_moderator()):
            remove_video_moderator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class VideoEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_video_editor()):
            add_video_editor(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class VideoEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_video_editor()):
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
        if request.user.is_video_manager() or request.user.is_superuser:
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
        if request.is_ajax() and form.is_valid() and (request.user.is_video_manager() or request.user.is_superuser):
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=video.pk, type="VID")
            moderate_obj.create_close(object=video, description=mod.description, manager_id=request.user.pk)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class VideoCloseDelete(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and (request.user.is_video_manager() or request.user.is_superuser):
            moderate_obj = Moderated.objects.get(object_id=video.pk, type="VID")
            moderate_obj.delete_close(object=video, manager_id=request.user.pk)
            return HttpResponse()
        else:
            raise Http404

class VideoClaimCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_detect_platform_template("managers/manage_create/video/video_claim.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(VideoClaimCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(VideoClaimCreate,self).get_context_data(**kwargs)
        context["object"] = Video.objects.get(uuid=self.kwargs["uuid"])
        return context

    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        if request.is_ajax() and request.user.is_authenticated:
            description = request.POST.get('description')
            type = request.POST.get('type')
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type="VID", object_id=self.kwargs["pk"], description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class VideoRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_video_manager() or request.user.is_superuser:
            moderate_obj = Moderated.objects.get(object_id=video.pk, type="VID")
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            return HttpResponse()
        else:
            raise Http404

class VideoUnverify(View):
    def get(self,request,*args,**kwargs):
        video, obj = Video.objects.get(uuid=self.kwargs["video_uuid"]), Moderated.objects.get(pk=self.kwargs["obj_pk"])
        if request.is_ajax() and (request.user.is_video_manager() or request.user.is_superuser):
            obj.unverify_moderation(manager_id=request.user.pk)
            return HttpResponse()
        else:
            raise Http404
