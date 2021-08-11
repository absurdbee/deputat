from django.views import View
from users.models import User
from django.http import HttpResponse, HttpResponseBadRequest
from common.staff_progs.organization import *
from organizations.models import Organization
from common.model.comments import OrganizationComment
from django.views.generic.base import TemplateView
from managers.models import Moderated
from django.http import Http404
from common.templates import get_detect_platform_template
from logs.model.manage_organization import OrganizationManageLog
from managers.forms import ModeratedForm, ReportForm


class OrganizationAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_organization_administrator():
            add_organization_administrator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class OrganizationAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_organization_administrator():
            remove_organization_administrator(user, request.user)
            return HttpResponse()
        else:
            raise Http404


class OrganizationModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_organization_moderator():
            add_organization_moderator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class OrganizationModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_organization_moderator():
            remove_organization_moderator(user, request.user)
            return HttpResponse()
        else:
            raise Http404


class OrganizationEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_organization_editor():
            add_organization_editor(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class OrganizationEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_organization_editor():
            remove_organization_editor(user, request.user)
            return HttpResponse()
        else:
            raise Http404


class OrganizationWorkerAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_organization_administrator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class OrganizationWorkerAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_organization_administrator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404


class OrganizationWorkerModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_organization_moderator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class OrganizationWorkerModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_organization_moderator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404


class OrganizationWorkerEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_organization_editor_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class OrganizationWorkerEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_organization_editor_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404


class OrganizationCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        if request.is_ajax() and request.user.is_organization_manager():
            self.template_name = get_detect_platform_template("managers/manage_create/organization/organization_close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(OrganizationCloseCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(OrganizationCloseCreate,self).get_context_data(**kwargs)
        context["object"] = Organization.objects.get(pk=self.kwargs["pk"])
        return context

    def post(self,request,*args,**kwargs):
        from managers.forms import ModeratedForm

        organization, form = Organization.objects.get(pk=self.kwargs["pk"]), ModeratedForm(request.POST)
        if request.is_ajax() and form.is_valid() and request.user.is_organization_manager():
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=organization.pk, type="ORG")
            moderate_obj.create_close(object=organization, description=mod.description, manager_id=request.user.pk)
            OrganizationManageLog.objects.create(item=organization.pk, manager=request.user.pk, action_type=OrganizationManageLog.ITEM_CLOSED)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class OrganizationCloseDelete(View):
    def get(self,request,*args,**kwargs):
        organization = Organization.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_organization_manager():
            moderate_obj = Moderated.objects.get(object_id=organization.pk, type="ORG")
            moderate_obj.delete_close(object=organization, manager_id=request.user.pk)
            OrganizationManageLog.objects.create(item=organization.pk, manager=request.user.pk, action_type=OrganizationManageLog.ITEM_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404


class OrganizationClaimCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.organization = Organization.objects.get(pk=self.kwargs["pk"])
        self.is_reported = ModerationReport.is_user_already_reported(request.user.pk, 'ORG', self.organization.pk)
        self.template_name = get_detect_platform_template("managers/manage_create/organization/organization_claim.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(OrganizationClaimCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from managers.forms import ReportForm

        context = super(OrganizationClaimCreate,self).get_context_data(**kwargs)
        context["object"] = self.organization
        context["is_reported"] = self.is_reported
        return context

    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        organization = Organization.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and not ModerationReport.is_user_already_reported(request.user.pk, 'ORG', organization.pk):
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type="ORG", object_id=organization.pk, description=request.POST.get('description'), type=request.POST.get('type'))
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class OrganizationRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        if request.is_ajax() and request.user.is_organization_manager():
            organization = Organization.objects.get(pk=self.kwargs["pk"])
            moderate_obj = Moderated.objects.get(object_id=organization.pk, type="ORG")
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            OrganizationManageLog.objects.create(item=organization.pk, manager=request.user.pk, action_type=OrganizationManageLog.ITEM_REJECT)
            return HttpResponse()
        else:
            raise Http404


class OrganizationUnverify(View):
    def get(self,request,*args,**kwargs):
        organization = Organization.objects.get(pk=self.kwargs["pk"])
        obj = Moderated.get_or_create_moderated_object(object_id=organization.pk, type="ORG")
        if request.is_ajax() and request.user.is_organization_manager():
            obj.unverify_moderation(organization, manager_id=request.user.pk)
            OrganizationManageLog.objects.create(item=obj.object_id, manager=request.user.pk, action_type=OrganizationManageLog.ITEM_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404


class CommentOrganizationClaimCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.comment = OrganizationComment.objects.get(pk=self.kwargs["pk"])
        self.is_reported = ModerationReport.is_user_already_reported(request.user.pk, 'ORGC', self.comment.pk)
        self.template_name = get_detect_platform_template("managers/manage_create/organization/comment_claim.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(CommentOrganizationClaimCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommentOrganizationClaimCreate,self).get_context_data(**kwargs)
        context["object"] = self.comment
        context["is_reported"] = self.is_reported
        return context

    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        comment = OrganizationComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and not ModerationReport.is_user_already_reported(request.user.pk, 'ORGC', comment.pk):
            description = request.POST.get('description')
            type = request.POST.get('type')
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type="ORGС", object_id=comment.pk, description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CommentOrganizationRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        comment = OrganizationComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_organization_manager():
            moderate_obj = Moderated.objects.get(object_id=comment.pk, type="BLOC")
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            OrganizationManageLog.objects.create(item=comment.pk, manager=request.user.pk, action_type=OrganizationManageLog.COMMENT_REJECT)
            return HttpResponse()
        else:
            raise Http404


class CommentOrganizationUnverify(View):
    def get(self,request,*args,**kwargs):
        comment = OrganizationComment.objects.get(pk=self.kwargs["pk"])
        obj = Moderated.get_or_create_moderated_object(object_id=comment.pk, type="BLOC")
        if request.is_ajax() and request.user.is_organization_manager():
            obj.unverify_moderation(comment, manager_id=request.user.pk)
            OrganizationManageLog.objects.create(item=comment.pk, manager=request.user.pk, action_type=OrganizationManageLog.COMMENT_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404

class CommentOrganizationCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.comment = OrganizationComment.objects.get(pk=self.kwargs["pk"])
        if request.user.is_organization_manager():
            self.template_name = get_detect_platform_template("managers/manage_create/organization/comment_close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(CommentOrganizationCloseCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommentOrganizationCloseCreate,self).get_context_data(**kwargs)
        context["object"] = self.comment
        return context

    def post(self,request,*args,**kwargs):
        comment = OrganizationComment.objects.get(pk=self.kwargs["pk"])
        form = ModeratedForm(request.POST)
        if form.is_valid() and request.user.is_organization_manager():
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=comment.pk, type="ORGC")
            moderate_obj.create_close(object=comment, description=mod.description, manager_id=request.user.pk)
            OrganizationManageLog.objects.create(item=comment.pk, manager=request.user.pk, action_type=OrganizationManageLog.COMMENT_CLOSED)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CommentOrganizationCloseDelete(View):
    def get(self,request,*args,**kwargs):
        comment = OrganizationComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_organization_manager():
            moderate_obj = Moderated.objects.get(object_id=comment.pk, type="ORGC")
            moderate_obj.delete_close(object=comment, manager_id=request.user.pk)
            OrganizationManageLog.objects.create(item=comment.pk, manager=request.user.pk, action_type=OrganizationManageLog.COMMENT_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404


class PublishOrganization(TemplateView):
    template_name = "managers/manage_create/organization/create_publish_organization.html"

    def get(self,request,*args,**kwargs):
        self.organization = Organization.objects.get(pk=self.kwargs["pk"])
        return super(PublishOrganization,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from organizations.forms import OrganizationForm

        context=super(PublishOrganization,self).get_context_data(**kwargs)
        context["form"] = OrganizationForm(instance=self.organization)
        context["organization"] = self.organization
        return context

    def post(self,request,*args,**kwargs):
        from organizations.forms import OrganizationForm
        from common.templates import render_for_platform

        self.organization = Organization.objects.get(pk=self.kwargs["pk"])
        self.form_post = OrganizationForm(request.POST, instance=self.organization)

        if request.is_ajax() and self.form_post.is_valid() and request.user.is_organization_manager():
            post = self.form_post.save(commit=False)
            new_post = post.create_publish_organization(name=post.name,
                                                        description=post.description,
                                                        elect=post.elect,
                                                        image=post.image,
                                                        email_1=post.email_1,
                                                        email_2=post.email_2,
                                                        phone_1=post.phone_1,
                                                        phone_2=post.phone_2,
                                                        address_1=post.address_1,
                                                        address_2=post.address_2,
                                                        type=post.type,
                                                        managet_id=request.user.pk)
            return render_for_platform(request, '<template>',{'organization': new_post})
        else:
            from django.http import HttpResponseBadRequest
            return HttpResponseBadRequest()

class CreateOrganization(TemplateView):
    template_name = "managers/manage_create/organization/create_manager_organization.html"

    def get_context_data(self,**kwargs):
        from organizations.forms import OrganizationForm

        context=super(CreateOrganization,self).get_context_data(**kwargs)
        context["form"] = OrganizationForm()
        return context

    def post(self,request,*args,**kwargs):
        from organizations.forms import OrganizationForm
        from common.templates import render_for_platform

        self.form_post = OrganizationForm(request.POST)

        if request.is_ajax() and self.form_post.is_valid() and request.user.is_organization_manager():
            post = self.form_post.save(commit=False)
            new_post = post.create_manager_organization(name=post.name,
                                                        description=post.description,
                                                        elect=post.elect,
                                                        image=post.image,
                                                        email_1=post.email_1,
                                                        email_2=post.email_2,
                                                        phone_1=post.phone_1,
                                                        phone_2=post.phone_2,
                                                        address_1=post.address_1,
                                                        address_2=post.address_2,
                                                        type=post.type,
                                                        creator=request.user)
            return render_for_platform(request, '<template>',{'organization': new_post})
        else:
            from django.http import HttpResponseBadRequest
            return HttpResponseBadRequest()

class RejectOrganization(View):
    def get(self,request,*args,**kwargs):
        from managers.forms import ModeratedForm

        self.organization = Organization.objects.get(pk=self.kwargs["pk"])
        self.form_post = ModeratedForm(request.POST)

        if request.is_ajax() and self.form_post.is_valid() and request.user.is_organization_manager():
            post = self.form_post.save(commit=False)
            obj = post.get_or_create_moderated_object("ORG", self.organization.pk)
            obj.description = post.description
            obj.save(update_fields=["description"])
            self.organization.type = "_REJ"
            self.organization.save(update_fields=["type"])
            return HttpResponse()
        else:
            from django.http import HttpResponseBadRequest
            return HttpResponseBadRequest()
