from django.views.generic.base import TemplateView
from django.views.generic import ListView
from common.templates import get_managers_template
from generic.mixins import CategoryListMixin
from django.http import HttpResponse, Http404
from lists.models import MediaList
from django.views import View


class ManagersView(TemplateView, CategoryListMixin):
    template_name = None

    def get(self,request,*args,**kwargs):
        if request.user.is_manager() or request.user.is_superuser:
            self.template_name = get_managers_template("managers/managers.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(ManagersView,self).get(request,*args,**kwargs)

class SuperManagersView(TemplateView, CategoryListMixin):
    template_name = None

    def get(self,request,*args,**kwargs):
        if request.user.is_supermanager() or request.user.is_superuser:
            self.template_name = get_managers_template("managers/managers.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(SuperManagersView,self).get(request,*args,**kwargs)


class LoadClaims(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        from managers.models import Moderated

        self.obj = Moderated.objects.get(pk=self.kwargs["pk"])
        if request.user.is_manager():
            self.template_name = get_managers_template("managers/claims.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(LoadClaims,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(LoadClaims,self).get_context_data(**kwargs)
        context["report"] = self.obj
        return context

    def get_queryset(self):
        return self.obj.reports.all()


class CreateMediaList(TemplateView):
    def get(self,request,*args,**kwargs):
        from common.templates import get_managers_template

        self.template_name = get_managers_template("managers/manage_create/create_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(CreateMediaList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from lists.forms import MedialistForm

        context = super(CreateMediaList,self).get_context_data(**kwargs)
        context["form_post"] = MedialistForm()
        return context

    def post(self,request,*args,**kwargs):
        from lists.forms import MedialistForm
        from common.templates import render_for_platform

        form_post = MedialistForm(request.POST)
        if request.is_ajax() and form_post.is_valid() and request.user.is_manager():
            list = form_post.save(commit=False)
            new_list = list.create_list(creator=request.user, name=list.name, description=list.description, order=list.order)
            return render_for_platform(request, 'main/media.html',{'list': new_list})
        else:
            from django.http import HttpResponseBadRequest
            return HttpResponseBadRequest()


class EditMediaList(TemplateView):
    def get(self,request,*args,**kwargs):
        from common.templates import get_managers_template

        self.template_name = get_managers_template("managers/manage_create/edit_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(EditMediaList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from lists.forms import MedialistForm

        context = super(EditMediaList,self).get_context_data(**kwargs)
        context["list"] = MediaList.objects.get(uuid=self.kwargs["uuid"])
        return context

    def post(self,request,*args,**kwargs):
        from lists.forms import MedialistForm

        self.list = MediaList.objects.get(uuid=self.kwargs["uuid"])
        self.form = MedialistForm(request.POST,instance=self.list)
        if request.is_ajax() and self.form.is_valid() and request.user.is_manager():
            list = self.form.save(commit=False)
            list.edit_list(name=list.name, description=list.description, order=list.order, manager_id=request.user.pk)
            return HttpResponse()
        else:
            from django.http import HttpResponseBadRequest
            return HttpResponseBadRequest()
        return super(EditMediaList,self).get(request,*args,**kwargs)


class UserMediaListDelete(View):
    def get(self,request,*args,**kwargs):
        list = MediaList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_manager() and list.type == MediaList.LIST:
            list.delete_list()
            return HttpResponse()
        else:
            raise Http404

class UserMediaListAbortDelete(View):
    def get(self,request,*args,**kwargs):
        list = MediaList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_manager() and list.type == MediaList.DELETED:
            list.abort_delete_list()
            return HttpResponse()
        else:
            raise Http404
