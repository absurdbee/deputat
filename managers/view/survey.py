from django.views import View
from users.models import User
from django.http import HttpResponse, HttpResponseBadRequest
from common.staff_progs.survey import *
from survey.models import Survey, SurveyList
from django.views.generic.base import TemplateView
from managers.models import Moderated
from django.http import Http404
from common.templates import get_detect_platform_template
from logs.model.manage_survey import SurveyManageLog


class SurveyAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_survey_administrator()):
            add_survey_administrator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class SurveyAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_survey_administrator()):
            remove_survey_administrator(user, request.user)
            return HttpResponse()
        else:
            raise Http404


class SurveyModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_survey_moderator()):
            add_survey_moderator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class SurveyModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_survey_moderator()):
            remove_survey_moderator(user, request.user)
            return HttpResponse()
        else:
            raise Http404


class SurveyEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_survey_editor()):
            add_survey_editor(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class SurveyEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_survey_editor()):
            remove_survey_editor(user, request.user)
            return HttpResponse()
        else:
            raise Http404


class SurveyWorkerAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_survey_administrator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class SurveyWorkerAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_survey_administrator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404


class SurveyWorkerModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_survey_moderator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class SurveyWorkerModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_survey_moderator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404


class SurveyWorkerEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_survey_editor_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class SurveyWorkerEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_survey_editor_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404


class SurveyCloseCreate(View):
    template_name = None

    def get(self,request,*args,**kwargs):
        if request.is_ajax() and (request.user.is_survey_manager() or request.user.is_superuser):
            self.template_name = get_detect_platform_template("managers/manage_create/survey/survey_close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(SurveyCloseCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(SurveyCloseCreate,self).get_context_data(**kwargs)
        context["object"] = Survey.objects.get(uuid=self.kwargs["uuid"])
        return context

    def post(self,request,*args,**kwargs):
        from managers.forms import ModeratedForm

        survey, form = Survey.objects.get(uuid=self.kwargs["uuid"]), ModeratedForm(request.POST)
        if request.is_ajax() and form.is_valid() and (request.user.is_survey_manager() or request.user.is_superuser):
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=survey.pk, type="MUS")
            moderate_obj.create_close(object=survey, description=mod.description, manager_id=request.user.pk)
            SurveyManageLog.objects.create(item=survey.pk, manager=request.user.pk, action_type=SurveyManageLog.ITEM_CLOSED)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class SurveyCloseDelete(View):
    def get(self,request,*args,**kwargs):
        survey = Survey.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and (request.user.is_survey_manager() or request.user.is_superuser):
            moderate_obj = Moderated.objects.get(object_id=survey.pk, type="MUS")
            moderate_obj.delete_close(object=survey, manager_id=request.user.pk)
            SurveyManageLog.objects.create(item=survey.pk, manager=request.user.pk, action_type=SurveyManageLog.ITEM_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404


class SurveyClaimCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_detect_platform_template("managers/manage_create/survey/survey_claim.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(SurveyClaimCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(SurveyClaimCreate,self).get_context_data(**kwargs)
        context["object"] = Survey.objects.get(uuid=self.kwargs["uuid"])
        return context

    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        if request.is_ajax():
            survey = Survey.objects.get(uuid=self.kwargs["uuid"])
            description = request.POST.get('description')
            type = request.POST.get('type')
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type="MUS", object_id=survey.pk, description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class SurveyRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        if request.is_ajax() and (request.user.is_survey_manager() or request.user.is_superuser):
            survey = Survey.objects.get(uuid=self.kwargs["uuid"])
            moderate_obj = Moderated.objects.get(object_id=survey.pk, type="MUS")
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            SurveyManageLog.objects.create(item=survey.pk, manager=request.user.pk, action_type=SurveyManageLog.ITEM_REJECT)
            return HttpResponse()
        else:
            raise Http404


class SurveyUnverify(View):
    def get(self,request,*args,**kwargs):
        obj = Moderated.objects.get(pk=self.kwargs["obj_pk"])
        if request.is_ajax() and (request.user.is_survey_manager() or request.user.is_superuser):
            obj.unverify_moderation(manager_id=request.user.pk)
            SurveyManageLog.objects.create(item=obj.object_id, manager=request.user.pk, action_type=SurveyManageLog.ITEM_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404


class ListSurveyClaimCreate(View):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.list = SurveyList.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = get_detect_platform_template("managers/manage_create/survey/list_claim.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(ListSurveyClaimCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ListSurveyClaimCreate,self).get_context_data(**kwargs)
        context["list"] = self.list
        return context

    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.list = SurveyList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax():
            description = request.POST.get('description')
            type = request.POST.get('type')
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type="SUL", object_id=list.pk, description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class ListSurveyRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        list = SurveyList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and (request.user.is_survey_manager() or request.user.is_superuser):
            moderate_obj = Moderated.objects.get(object_id=list.pk, type="SUL")
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            SurveyManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=SurveyManageLog.LIST_REJECT)
            return HttpResponse()
        else:
            raise Http404


class ListSurveyUnverify(View):
    def get(self,request,*args,**kwargs):
        list = SurveyList.objects.get(uuid=self.kwargs["uuid"])
        obj = Moderated.objects.get(pk=self.kwargs["obj_pk"])
        if request.is_ajax() and (request.user.is_survey_manager() or request.user.is_superuser):
            obj.unverify_moderation(manager_id=request.user.pk)
            SurveyManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=SurveyManageLog.LIST_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404

class ListSurveyCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.list = SurveyList.objects.get(uuid=self.kwargs["uuid"])
        if request.user.is_survey_manager() or request.user.is_superuser:
            self.template_name = get_detect_platform_template("managers/manage_create/survey/list_close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ListSurveyCloseCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ListSurveyCloseCreate,self).get_context_data(**kwargs)
        context["list"] = self.list
        return context

    def post(self,request,*args,**kwargs):
        list = SurveyList.objects.get(uuid=self.kwargs["uuid"])
        form = ModeratedForm(request.POST)
        if form.is_valid() and (request.user.is_survey_manager() or request.user.is_superuser):
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=list.pk, type="SUL")
            moderate_obj.create_close(object=list, description=mod.description, manager_id=request.user.pk)
            SurveyManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=SurveyManageLog.LIST_CLOSED)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class ListSurveyCloseDelete(View):
    def get(self,request,*args,**kwargs):
        list = SurveyList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and (request.user.is_survey_manager() or request.user.is_superuser):
            moderate_obj = Moderated.objects.get(object_id=list.pk, type="SUL")
            moderate_obj.delete_close(object=list, manager_id=request.user.pk)
            SurveyManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=SurveyManageLog.LIST_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404
