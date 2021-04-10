from docs.models import Doc, DocList
from users.models import User
from django.views import View
from django.views.generic.base import TemplateView
from docs.forms import DoclistForm, DocForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.http import Http404
from common.templates import render_for_platform, get_small_template


class UserDoclistAdd(View):
    def get(self,request,*args,**kwargs):
        list = DocList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.is_user_can_add_list(request.user.pk):
            list.users.add(request.user)
        return HttpResponse()

class UserDoclistRemove(View):
    def get(self,request,*args,**kwargs):
        list = DocList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.is_user_can_delete_list(request.user.pk):
            list.users.remove(request.user)
        return HttpResponse()


class UserDocAdd(View):
    def get(self, request, *args, **kwargs):
        doc, list = Doc.objects.get(pk=self.kwargs["pk"]), DocList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and not list.is_doc_in_list(doc.pk):
            list.doc_list.add(doc)
            return HttpResponse()
        else:
            raise Http404

class UserDocRemove(View):
    def get(self, request, *args, **kwargs):
        doc = Doc.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and list.is_doc_in_list(doc.pk):
            doc.remove()
            return HttpResponse()
        else:
            raise Http404

class UserDocListAdd(View):
    def get(self, request, *args, **kwargs):
        doc, list = Doc.objects.get(pk=self.kwargs["pk"]), DocList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and not list.is_item_in_list(doc.pk):
            list.doc_list.add(doc)
            return HttpResponse()
        else:
            raise Http404

class UserDocListRemove(View):
    def get(self, request, *args, **kwargs):
        doc, list = Doc.objects.get(pk=self.kwargs["pk"]), DocList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.is_item_in_list(doc.pk):
            list.doc_list.remove(doc)
            return HttpResponse()
        else:
            raise Http404

class UserDoclistCreate(TemplateView):
    form_post = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_small_template("user_docs/create_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserDoclistCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserDoclistCreate,self).get_context_data(**kwargs)
        context["form_post"] = DoclistForm()
        return context

    def post(self,request,*args,**kwargs):
        form_post= DoclistForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            new_list = form_post.save(commit=False)
            new_list.creator = request.user
            if not new_list.order:
                new_list.order = 0
            new_list.save()
            return render_for_platform(request, 'user_docs/list/my_list.html',{'list': new_list, 'user': request.user})
        else:
            return HttpResponseBadRequest()


class UserDoclistEdit(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_small_template("user_docs/edit_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserDoclistEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserDoclistEdit,self).get_context_data(**kwargs)
        context["list"] = DocList.objects.get(uuid=self.kwargs["uuid"])
        return context

    def post(self,request,*args,**kwargs):
        self.list = DocList.objects.get(uuid=self.kwargs["uuid"])
        self.form = DoclistForm(request.POST,instance=self.list)
        if request.is_ajax() and self.form.is_valid():
            list = self.form.save(commit=False)
            self.form.save()
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
        return super(UserDoclistEdit,self).get(request,*args,**kwargs)


class UserDocCreate(TemplateView):
    form_post = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_small_template("user_docs/create_doc.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserDocCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserDocCreate,self).get_context_data(**kwargs)
        context["form_post"] = DocForm()
        return context

    def post(self,request,*args,**kwargs):
        form_post = DocForm(request.POST, request.FILES)

        if request.is_ajax() and form_post.is_valid():
            doc = form_post.save(commit=False)
            new_doc = Doc.create_doc(creator=request.user, title=doc.title, file=doc.file, lists=request.POST.getlist("list"), is_public=request.POST.list("is_public"))
            return render_for_platform(request, 'user_docs/new_doc.html',{'doc': new_doc})
        else:
            return HttpResponseBadRequest()

class UserDocEdit(TemplateView):
    form_post = None

    def get(self,request,*args,**kwargs):
        self.doc = Doc.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_small_template("user_docs/edit_doc.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserDocEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserDocEdit,self).get_context_data(**kwargs)
        context["form_post"] = DocForm(instance=self.doc)
        context["doc"] = self.doc
        return context

    def post(self,request,*args,**kwargs):
        self.doc = Doc.objects.get(pk=self.kwargs["pk"])
        form_post = DocForm(request.POST, request.FILES, instance=self.doc)

        if request.is_ajax() and form_post.is_valid():
            _doc = form_post.save(commit=False)
            new_doc = Doc.edit_doc(title=_doc.title, file=_doc.file, lists=request.POST.getlist("list"), is_public=request.POST.get("is_public"))
            return render_for_platform(request, 'user_docs/new_doc.html',{'doc': new_doc})
        else:
            return HttpResponseBadRequest()


class UserDoclistDelete(View):
    def get(self,request,*args,**kwargs):
        list = DocList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and self.kwargs["pk"] == request.user.pk and list.status == DocList.LIST:
            list.type = "DEL"
            list.save(update_fields=['type'])
            return HttpResponse()
        else:
            raise Http404

class UserDoclistAbortDelete(View):
    def get(self,request,*args,**kwargs):
        list = DocList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and self.kwargs["pk"] == request.user.pk:
            list.type = "LIS"
            list.save(update_fields=['type'])
            return HttpResponse()
        else:
            raise Http404
