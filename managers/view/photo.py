from django.views import View
from users.models import User
from django.http import HttpResponse, HttpResponseBadRequest
from common.staff_progs.photo import *
from gallery.models import Photo, PhotoComment
from managers.forms import ModeratedForm
from django.views.generic.base import TemplateView
from managers.models import Moderated
from django.http import Http404
from common.templates import get_detect_platform_template
from logs.model.manage_photo import PhotoManageLog


class PhotoAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_photo_administrator()):
            add_photo_administrator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PhotoAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_photo_administrator()):
            remove_photo_administrator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PhotoModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_photo_moderator()):
            add_photo_moderator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PhotoModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_photo_moderator()):
            remove_photo_moderator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PhotoEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_photo_editor()):
            add_photo_editor(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PhotoEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_photo_editor()):
            remove_photo_editor(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PhotoWorkerAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_photo_administrator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PhotoWorkerAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_photo_administrator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PhotoWorkerModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_photo_moderator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PhotoWorkerModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_photo_moderator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PhotoWorkerEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_photo_editor_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PhotoWorkerEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_photo_editor_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PhotoCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        if request.user.is_photo_manager() or request.user.is_superuser:
            self.template_name = get_detect_platform_template("managers/manage_create/photo/photo_close", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(PhotoCloseCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PhotoCloseCreate,self).get_context_data(**kwargs)
        context["object"] = Photo.objects.get(uuid=self.kwargs["uuid"])
        return context

    def post(self,request,*args,**kwargs):
        photo, form = Photo.objects.get(uuid=self.kwargs["uuid"]), ModeratedForm(request.POST)
        if request.is_ajax() and form.is_valid() and (request.user.is_photo_manager() or request.user.is_superuser):
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=photo.pk, type="PHO")
            moderate_obj.create_close(object=photo, description=mod.description, manager_id=request.user.pk)
            PhotoManageLog.objects.create(item=photo.pk, manager=request.user.pk, action_type=PhotoManageLog.ITEM_CLOSED)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class PhotoCloseDelete(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_photo_manager() or request.user.is_superuser:
            moderate_obj = Moderated.objects.get(object_id=photo.pk, type="PHO")
            moderate_obj.delete_close(object=photo, manager_id=request.user.pk)
            PhotoManageLog.objects.create(item=photo.pk, manager=request.user.pk, action_type=PhotoManageLog.ITEM_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404

class PhotoClaimCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_detect_platform_template("managers/manage_create/photo/photo_claim", request.user, request.META['HTTP_USER_AGENT'])
        return super(PhotoClaimCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PhotoClaimCreate,self).get_context_data(**kwargs)
        context["object"] = Photo.objects.get(uuid=self.kwargs["uuid"])
        return context

    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        if request.is_ajax():
            description = request.POST.get('description')
            type = request.POST.get('type')
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type="PHO", object_id=self.kwargs["pk"], description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class PhotoRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_photo_manager() or request.user.is_superuser:
            moderate_obj = Moderated.objects.get(object_id=photo.pk, type="PHO")
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            PhotoManageLog.objects.create(item=photo.pk, manager=request.user.pk, action_type=PhotoManageLog.ITEM_REJECT)
            return HttpResponse()
        else:
            raise Http404

class PhotoUnverify(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["photo_uuid"])
        obj = Moderated.objects.get(pk=self.kwargs["obj_pk"])
        if request.is_ajax() and request.user.is_photo_manager() or request.user.is_superuser:
            obj.unverify_moderation(manager_id=request.user.pk)
            PhotoManageLog.objects.create(item=photo.pk, manager=request.user.pk, action_type=PhotoManageLog.ITEM_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404
