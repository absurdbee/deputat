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

class ElectNewCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.post = ElectNew.objects.get(pk=self.kwargs["pk"])
        if request.user.is_elect_new_manager():
            self.template_name = get_detect_platform_template("managers/manage_create/elect_new/elect_new_close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ElectNewCloseCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ElectNewCloseCreate,self).get_context_data(**kwargs)
        context["object"] = self.post
        return context

    def post(self,request,*args,**kwargs):
        post, form = ElectNew.objects.get(pk=self.kwargs["pk"]), ModeratedForm(request.POST)
        if request.is_ajax() and form.is_valid() and request.user.is_elect_new_manager():
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=post.pk, type="ELE")
            moderate_obj.create_close(object=post, description=mod.description, manager_id=request.user.pk)
            ElectNewManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=ElectNewManageLog.ITEM_CLOSED)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class ElectNewCloseDelete(View):
    def get(self,request,*args,**kwargs):
        post = ElectNew.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_elect_new_manager():
            moderate_obj = Moderated.objects.get(object_id=post.pk, type="ELE")
            moderate_obj.delete_close(object=post, manager_id=request.user.pk)
            ElectNewManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=ElectNewManageLog.ITEM_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404

class ElectNewClaimCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.template_name = get_detect_platform_template("managers/manage_create/elect_new/elect_new_claim.html", request.user, request.META['HTTP_USER_AGENT'])
        self.new = ElectNew.objects.get(pk=self.kwargs["pk"])
        self.is_reported = ModerationReport.is_user_already_reported(request.user.pk, 'ELE', self.new.pk)
        return super(ElectNewClaimCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from managers.models import ModerationReport

        context = super(ElectNewClaimCreate,self).get_context_data(**kwargs)
        context["object"] = self.new
        context["is_reported"] = self.is_reported
        return context

    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.new = ElectNew.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and not ModerationReport.is_user_already_reported(request.user.pk, 'ELE', self.new.pk):
            description = request.POST.get('description')
            type = request.POST.get('type')
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type="ELE", object_id=self.new.pk, description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class ElectNewRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        post = ElectNew.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_elect_new_manager():
            moderate_obj = Moderated.objects.get(object_id=post.pk, type="ELE")
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            ElectNewManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=ElectNewManageLog.ITEM_REJECT)
            return HttpResponse()
        else:
            raise Http404


class ElectNewUnverify(View):
    def get(self,request,*args,**kwargs):
        post = ElectNew.objects.get(pk=self.kwargs["pk"])
        obj = Moderated.get_or_create_moderated_object(object_id=post.pk, type="ELE")
        if request.is_ajax() and request.user.is_elect_new_manager():
            obj.unverify_moderation(post, manager_id=request.user.pk)
            ElectNewManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=ElectNewManageLog.ITEM_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404


class PublishElectNew(TemplateView):
    template_name = "managers/manage_create/elect_new/create_publish_elect_new.html"

    def get(self,request,*args,**kwargs):
        self.elect_new = ElectNew.objects.get(pk=self.kwargs["pk"])
        return super(PublishElectNew,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from blog.forms import PublishElectNewForm
        from tags.models import ManagerTag
        from elect.models import Elect

        context=super(PublishElectNew,self).get_context_data(**kwargs)
        context["form"] = PublishElectNewForm(instance=self.elect_new)
        context["new"] = self.elect_new
        context["tags"] = ManagerTag.objects.only("pk")
        context["get_elects"] = Elect.objects.only("pk")
        return context

    def post(self,request,*args,**kwargs):
        from blog.forms import PublishElectNewForm
        from common.templates import render_for_platform

        self.elect_new = ElectNew.objects.get(pk=self.kwargs["pk"])
        self.form_post = PublishElectNewForm(request.POST, instance=self.elect_new)

        if request.is_ajax() and self.form_post.is_valid() and request.user.is_elect_new_manager():
            post = self.form_post.save(commit=False)
            new_post = post.make_publish_new(title=post.title, description=post.description, elect=post.elect, attach=request.POST.getlist("attach_items"), category=post.category, tags=request.POST.getlist("tags"), manager_id=request.user.pk, comments_enabled=post.comments_enabled, votes_on=post.votes_on)
            return render_for_platform(request, 'elect/news/new.html',{'object': new_post})
        else:
            from django.http import HttpResponseBadRequest
            return HttpResponseBadRequest()

class CreateElectNew(TemplateView):
    template_name = "managers/manage_create/elect_new/create_manager_elect_new.html"

    def get_context_data(self,**kwargs):
        from blog.forms import PublishElectNewForm
        from tags.models import ManagerTag
        from elect.models import Elect

        context=super(CreateElectNew,self).get_context_data(**kwargs)
        context["form"] = PublishElectNewForm()
        context["tags"] = ManagerTag.objects.only("pk")
        context["get_elects"] = Elect.objects.only("pk")
        return context

    def post(self,request,*args,**kwargs):
        from blog.forms import PublishElectNewForm
        from common.templates import render_for_platform

        self.form_post = PublishElectNewForm(request.POST)

        if request.is_ajax() and self.form_post.is_valid() and request.user.is_elect_new_manager():
            post = self.form_post.save(commit=False)
            new_post = post.create_manager_new(creator=request.user, title=post.title, description=post.description, elect=request.POST.get("elect"), attach=request.POST.getlist("attach_items"), category=post.category, tags=request.POST.getlist("tags"), comments_enabled=post.comments_enabled, votes_on=post.votes_on)
            return render_for_platform(request, 'elect/news/new.html',{'object': new_post})
        else:
            from django.http import HttpResponseBadRequest
            return HttpResponseBadRequest()

class RejectElectNew(View):
    def get(self,request,*args,**kwargs):
        from managers.forms import ModeratedForm

        self.elect_new = ElectNew.objects.get(pk=self.kwargs["pk"])
        self.form_post = ModeratedForm(request.POST)

        if request.is_ajax() and self.form_post.is_valid() and request.user.is_elect_new_manager():
            post = self.form_post.save(commit=False)
            obj = post.get_or_create_moderated_object("ELE", self.elect_new.pk)
            obj.description = post.description
            obj.save(update_fields=["description"])
            self.elect_new.type = "_REJ"
            self.elect_new.save(update_fields=["type"])
            return HttpResponse()
        else:
            from django.http import HttpResponseBadRequest
            return HttpResponseBadRequest()


class CommentElectNewClaimCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.comment = ElectNewComment.objects.get(pk=self.kwargs["pk"])
        self.is_reported = ModerationReport.is_user_already_reported(request.user.pk, 'ELEC', self.comment.pk)
        self.template_name = get_detect_platform_template("managers/manage_create/elect_new/comment_claim.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(CommentElectNewClaimCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommentElectNewClaimCreate,self).get_context_data(**kwargs)
        context["object"] = self.comment
        context["is_reported"] = self.is_reported
        return context

    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        comment = ElectNewComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and not ModerationReport.is_user_already_reported(request.user.pk, 'ELEC', comment.pk):
            description = request.POST.get('description')
            type = request.POST.get('type')
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type="ELEC", object_id=comment.pk, description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CommentElectNewRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        comment = ElectNewComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_elect_new_manager():
            moderate_obj = Moderated.objects.get(object_id=comment.pk, type="ELEC")
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            ElectNewManageLog.objects.create(item=comment.pk, manager=request.user.pk, action_type=ElectNewManageLog.COMMENT_REJECT)
            return HttpResponse()
        else:
            raise Http404


class CommentElectNewUnverify(View):
    def get(self,request,*args,**kwargs):
        comment = ElectNewComment.objects.get(pk=self.kwargs["pk"])
        obj = Moderated.get_or_create_moderated_object(object_id=comment.pk, type="ELEC")
        if request.is_ajax() and request.user.is_elect_new_manager():
            obj.unverify_moderation(comment, manager_id=request.user.pk)
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
        context["object"] = self.comment
        return context

    def post(self,request,*args,**kwargs):
        comment = ElectNewComment.objects.get(pk=self.kwargs["pk"])
        form = ModeratedForm(request.POST)
        if form.is_valid() and request.user.is_elect_new_manager():
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=comment.pk, type="ELEC")
            moderate_obj.create_close(object=comment, description=mod.description, manager_id=request.user.pk)
            ElectNewManageLog.objects.create(item=comment.pk, manager=request.user.pk, action_type=ElectNewManageLog.COMMENT_CLOSED)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CommentElectNewCloseDelete(View):
    def get(self,request,*args,**kwargs):
        comment = ElectNewComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_elect_new_manager():
            moderate_obj = Moderated.objects.get(object_id=comment.pk, type="ELEC")
            moderate_obj.delete_close(object=comment, manager_id=request.user.pk)
            ElectNewManageLog.objects.create(item=comment.pk, manager=request.user.pk, action_type=ElectNewManageLog.COMMENT_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404
