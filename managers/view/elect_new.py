from django.views import View
from users.models import User
from django.http import HttpResponse, HttpResponseBadRequest
from common.staff_progs.elect_new import *
from common.model.comments import ElectNewComment
from blog.models import ElectNew
from managers.forms import ModeratedForm
from django.views.generic.base import TemplateView
from managers.models import Moderated
from django.http import Http404
from common.templates import get_detect_platform_template
from logs.model.manage_elect_new import ElectNewManageLog


class ElectNewAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_elect_new_administrator():
            add_elect_new_administrator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class ElectNewAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_elect_new_administrator():
            remove_elect_new_administrator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class ElectNewModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_elect_new_moderator():
            add_elect_new_moderator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class ElectNewModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_elect_new_moderator():
            remove_elect_new_moderator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class ElectNewEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_elect_new_editor():
            add_post_editor(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class ElectNewEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_elect_new_editor():
            remove_elect_new_editor(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class ElectNewWorkerAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_elect_new_administrator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class ElectNewWorkerAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_elect_new_administrator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class ElectNewWorkerModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_elect_new_moderator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class ElectNewWorkerModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_elect_new_moderator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class ElectNewWorkerEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_elect_new_editor_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class ElectNewWorkerEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_elect_new_editor_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class ElectNewCloseCreate(View):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.post = ElectNew.objects.get(uuid=self.kwargs["uuid"])
        if request.user.is_elect_new_manager():
            self.template_name = get_detect_platform_template("managers/manage_create/elect_new/close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ElectNewCloseCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ElectNewCloseCreate,self).get_context_data(**kwargs)
        context["object"] = self.post
        return context

    def post(self,request,*args,**kwargs):
        post, form = ElectNew.objects.get(uuid=self.kwargs["uuid"]), ModeratedForm(request.POST)
        if request.is_ajax() and form.is_valid() and request.user.is_elect_new_manager():
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=post.pk, type="POS")
            moderate_obj.create_close(object=post, description=mod.description, manager_id=request.user.pk)
            ElectNewManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=ElectNewManageLog.ITEM_CLOSED)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class ElectNewCloseDelete(View):
    def get(self,request,*args,**kwargs):
        post = ElectNew.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_elect_new_manager():
            moderate_obj = Moderated.objects.get(object_id=post.pk, type="POS")
            moderate_obj.delete_close(object=post, manager_id=request.user.pk)
            ElectNewManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=ElectNewManageLog.ITEM_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404

class ElectNewClaimCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_detect_platform_template("managers/manage_create/elect_new/claim.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(ElectNewClaimCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ElectNewClaimCreate,self).get_context_data(**kwargs)
        context["object"] = ElectNew.objects.get(uuid=self.kwargs["uuid"])
        return context

    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        if request.is_ajax():
            description = request.POST.get('description')
            type = request.POST.get('type')
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type="POS", object_id=self.kwargs["pk"], description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class ElectNewRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        post = ElectNew.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_elect_new_manager():
            moderate_obj = Moderated.objects.get(object_id=post.pk, type="POS")
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            ElectNewManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=ElectNewManageLog.ITEM_REJECT)
            return HttpResponse()
        else:
            raise Http404


class ElectNewUnverify(View):
    def get(self,request,*args,**kwargs):
        post = ElectNew.objects.get(uuid=self.kwargs["elect_new_uuid"])
        obj = Moderated.objects.get(pk=self.kwargs["obj_pk"])
        if request.is_ajax() and request.user.is_elect_new_manager():
            obj.unverify_moderation(manager_id=request.user.pk)
            ElectNewManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=ElectNewManageLog.ITEM_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404


class PublishElectNew(View):
    template_name = "elect/make_publish_elect_new.html"

    def get(self,request,*args,**kwargs):
        self.elect_new = ElectNew.objects.get(pk=self.kwargs["pk"])
        return super(PublishElectNew,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from blog.forms import ElectNewForm

        context=super(PublishElectNew,self).get_context_data(**kwargs)
        context["form"] = ElectNewForm()
        context["object"] = self.elect_new
        return context

    def post(self,request,*args,**kwargs):
        from blog.forms import ElectNewForm
        from common.templates import render_for_platform

        self.elect_new = ElectNew.objects.get(pk=self.kwargs["pk"])
        self.form_post = ElectNewForm(request.POST, instance=self.elect_new)

        if request.is_ajax() and self.form_post.is_valid() and request.user.is_authenticated:
            post = self.form_post.save(commit=False)
            new_post = post.make_publish_new(title=post.title, description=post.description, elect=post.elect, attach=request.POST.getlist("attach_items"), category=post.category)
            return render_for_platform(request, 'elect/elect_new.html',{'object': new_post})
        else:
            from django.http import HttpResponseBadRequest
            return HttpResponseBadRequest()

class RejectElectNew(View):
    template_name = "elect/reject_elect_new.html"

    def get(self,request,*args,**kwargs):
        self.elect_new = ElectNew.objects.get(pk=self.kwargs["pk"])
        return super(RejectElectNew,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from managers.forms import ModeratedForm

        context=super(RejectElectNew,self).get_context_data(**kwargs)
        context["form"] = ModeratedForm()
        context["object"] = self.elect_new
        return context

    def post(self,request,*args,**kwargs):
        from managers.forms import ModeratedForm

        self.elect_new = ElectNew.objects.get(pk=self.kwargs["pk"])
        self.form_post = ModeratedForm(request.POST)

        if request.is_ajax() and self.form_post.is_valid() and request.user.is_elect_new_manager():
            post = self.form_post.save(commit=False)
            obj = post.get_or_create_moderated_object("ELE", self.elect_new.pk)
            obj.description = post.description
            obj.save(update_fields=["description"])
            self.elect_new.type = "REJ"
            self.elect_new.save(update_fields=["type"])
            return HttpResponse()
        else:
            from django.http import HttpResponseBadRequest
            return HttpResponseBadRequest()


class CommentElectNewClaimCreate(View):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.comment = ElectNewComment.objects.get(pk=self.kwargs["pk"])
        try:
            self.post = self.comment.parent.new
        except:
            self.post = self.comment.new
        self.template_name = get_detect_platform_template("managers/manage_create/elect_new/comment_claim.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(CommentPostClaimCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommentPostClaimCreate,self).get_context_data(**kwargs)
        context["comment"] = self.comment
        context["post"] = self.post
        return context

    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        comment = ElectNewComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax():
            description = request.POST.get('description')
            type = request.POST.get('type')
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type="POSС", object_id=comment.pk, description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CommentElectNewRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        comment = ElectNewComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_elect_new_manager():
            moderate_obj = Moderated.objects.get(object_id=comment.pk, type="POSC")
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            ElectNewManageLog.objects.create(item=comment.pk, manager=request.user.pk, action_type=ElectNewManageLog.COMMENT_REJECT)
            return HttpResponse()
        else:
            raise Http404


class CommentElectNewUnverify(View):
    def get(self,request,*args,**kwargs):
        comment = ElectNewComment.objects.get(pk=self.kwargs["pk"])
        obj = Moderated.objects.get(pk=self.kwargs["obj_pk"])
        if request.is_ajax() and request.user.is_elect_new_manager():
            obj.unverify_moderation(manager_id=request.user.pk)
            ElectNewManageLog.objects.create(item=comment.pk, manager=request.user.pk, action_type=ElectNewManageLog.COMMENT_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404

class CommentElectNewCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.comment = ElectNewComment.objects.get(pk=self.kwargs["pk"])
        if request.user.is_elect_new_manager():
            self.template_name = get_detect_platform_template("managers/manage_create/elect_new/comment_close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(CommentElectNewCloseCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommentElectNewCloseCreate,self).get_context_data(**kwargs)
        context["comment"] = self.comment
        return context

    def post(self,request,*args,**kwargs):
        comment = ElectNewComment.objects.get(pk=self.kwargs["pk"])
        form = ModeratedForm(request.POST)
        if form.is_valid() and request.user.is_elect_new_manager():
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=comment.pk, type="POSC")
            moderate_obj.create_close(object=comment, description=mod.description, manager_id=request.user.pk)
            ElectNewManageLog.objects.create(item=comment.pk, manager=request.user.pk, action_type=ElectNewManageLog.COMMENT_CLOSED)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CommentElectNewCloseDelete(View):
    def get(self,request,*args,**kwargs):
        comment = ElectNewComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_elect_new_manager():
            moderate_obj = Moderated.objects.get(object_id=comment.pk, type="POSC")
            moderate_obj.delete_close(object=comment, manager_id=request.user.pk)
            ElectNewManageLog.objects.create(item=comment.pk, manager=request.user.pk, action_type=ElectNewManageLog.COMMENT_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404
