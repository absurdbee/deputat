from django.views import View
from users.models import User
from django.http import HttpResponse, HttpResponseBadRequest
from common.staff_progs.photo import *
from gallery.models import Photo, PhotoList
from managers.forms import ModeratedForm
from django.views.generic.base import TemplateView
from managers.models import Moderated
from django.http import Http404
from common.templates import get_detect_platform_template, render_for_platform
from logs.model.manage_photo import PhotoManageLog


class PhotoAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_photo_administrator():
            add_photo_administrator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PhotoAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_photo_administrator():
            remove_photo_administrator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PhotoModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_photo_moderator():
            add_photo_moderator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PhotoModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_photo_moderator():
            remove_photo_moderator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PhotoEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_photo_editor():
            add_photo_editor(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PhotoEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_photo_editor():
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
        if request.user.is_photo_manager():
            self.template_name = get_detect_platform_template("managers/manage_create/photo/photo_close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(PhotoCloseCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PhotoCloseCreate,self).get_context_data(**kwargs)
        context["object"] = Photo.objects.get(uuid=self.kwargs["uuid"])
        return context

    def post(self,request,*args,**kwargs):
        photo, form = Photo.objects.get(uuid=self.kwargs["uuid"]), ModeratedForm(request.POST)
        if request.is_ajax() and form.is_valid() and request.user.is_photo_manager():
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
        if request.is_ajax() and request.user.is_photo_manager():
            moderate_obj = Moderated.objects.get(object_id=photo.pk, type="PHO")
            moderate_obj.delete_close(object=photo, manager_id=request.user.pk)
            PhotoManageLog.objects.create(item=photo.pk, manager=request.user.pk, action_type=PhotoManageLog.ITEM_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404

class PhotoClaimCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        self.is_reported = ModerationReport.is_user_already_reported(request.user.pk, 'PHO', self.photo.pk)
        self.template_name = get_detect_platform_template("managers/manage_create/photo/photo_claim.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(PhotoClaimCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PhotoClaimCreate,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["is_reported"] = self.is_reported
        return context

    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and not ModerationReport.is_user_already_reported(request.user.pk, 'PHO', photo.pk):
            description = request.POST.get('description')
            type = request.POST.get('type')
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type="PHO", object_id=photo.pk, description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class PhotoRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_photo_manager():
            moderate_obj = Moderated.objects.get(object_id=photo.pk, type="PHO")
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            PhotoManageLog.objects.create(item=photo.pk, manager=request.user.pk, action_type=PhotoManageLog.ITEM_REJECT)
            return HttpResponse()
        else:
            raise Http404

class PhotoUnverify(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["photo_uuid"])
        obj = Moderated.get_or_create_moderated_object(object_id=photo.pk, type="PHO")
        if request.is_ajax() and request.user.is_photo_manager():
            obj.unverify_moderation(photo, manager_id=request.user.pk)
            PhotoManageLog.objects.create(item=photo.pk, manager=request.user.pk, action_type=PhotoManageLog.ITEM_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404


class ListPhotoClaimCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.list = PhotoList.objects.get(uuid=self.kwargs["uuid"])
        self.is_reported = ModerationReport.is_user_already_reported(request.user.pk, 'PHL', self.list.pk)
        self.template_name = get_detect_platform_template("managers/manage_create/photo/list_claim.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(ListPhotoClaimCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ListPhotoClaimCreate,self).get_context_data(**kwargs)
        context["object"] = self.list
        context["is_reported"] = self.is_reported
        return context

    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.list = PhotoList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and not ModerationReport.is_user_already_reported(request.user.pk, 'PHL', self.list.pk):
            description = request.POST.get('description')
            type = request.POST.get('type')
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type="PHL", object_id=self.list.pk, description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class ListPhotoRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        list = PhotoList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_photo_manager():
            moderate_obj = Moderated.objects.get(object_id=list.pk, type="PHL")
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            PhotoManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=PhotoManageLog.LIST_REJECT)
            return HttpResponse()
        else:
            raise Http404


class ListPhotoUnverify(View):
    def get(self,request,*args,**kwargs):
        list = PhotoList.objects.get(uuid=self.kwargs["uuid"])
        obj = Moderated.get_or_create_moderated_object(object_id=list.pk, type="PHL")
        if request.is_ajax() and request.user.is_photo_manager():
            obj.unverify_moderation(list, manager_id=request.user.pk)
            PhotoManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=PhotoManageLog.LIST_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404

class ListPhotoCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.list = PhotoList.objects.get(uuid=self.kwargs["uuid"])
        if request.user.is_photo_manager():
            self.template_name = get_detect_platform_template("managers/manage_create/photo/list_close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ListPhotoCloseCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ListPhotoCloseCreate,self).get_context_data(**kwargs)
        context["object"] = self.list
        return context

    def post(self,request,*args,**kwargs):
        list = PhotoList.objects.get(uuid=self.kwargs["uuid"])
        form = ModeratedForm(request.POST)
        if form.is_valid() and request.user.is_photo_manager():
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=list.pk, type="PHL")
            moderate_obj.create_close(object=list, description=mod.description, manager_id=request.user.pk)
            PhotoManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=PhotoManageLog.LIST_CLOSED)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class ListPhotoCloseDelete(View):
    def get(self,request,*args,**kwargs):
        list = PhotoList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_photo_manager():
            moderate_obj = Moderated.objects.get(object_id=list.pk, type="PHL")
            moderate_obj.delete_close(object=list, manager_id=request.user.pk)
            PhotoManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=PhotoManageLog.LIST_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404


class CreateManagerPhoto(View):
    def post(self, request, *args, **kwargs):
        from lists.models import MediaList

        if request.is_ajax():
            list, photos = MediaList.objects.get(uuid=self.kwargs["uuid"]), []
            for p in request.FILES.getlist('file'):
                photo = Photo.create_manager_photo(creator=request.user, image=p, list=list)
                photos += [photo]
            return render_for_platform(request, 'managers/manage_create/photo/new_manager_photos.html',{'object_list': photos})
        else:
            raise Http404


class ManagerPhotoDelete(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_manager():
            photo.delete_photo(None)
            return HttpResponse()
        else:
            raise Http404

class ManagerPhotoAbortDelete(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_manager():
            photo.abort_delete_photo(None)
            return HttpResponse()
        else:
            raise Http404


class AddPhotoInMediaList(View):
    def get(self, request, *args, **kwargs):
        from lists.models import MediaList

        photo, list = Photo.objects.get(pk=self.kwargs["pk"]), MediaList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and not list.is_photo_in_list(photo.pk) and request.user.is_manager():
            list.media_list.add(photo)
            return HttpResponse()
        else:
            raise Http404

class RemovePhotoFromMediaList(View):
    def get(self, request, *args, **kwargs):
        from lists.models import MediaList

        photo, list = Photo.objects.get(pk=self.kwargs["pk"]), MediaList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.is_photo_in_list(photo.pk) and request.user.is_manager():
            list.media_list.remove(photo)
            return HttpResponse()
        else:
            raise Http404
