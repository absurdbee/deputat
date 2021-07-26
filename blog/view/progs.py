from django.views.generic.base import TemplateView
from django.views import View
from django.http import HttpResponse
from django.http import Http404


class BlogCreateView(TemplateView):
    template_name = "blog/create_blog.html"

    def get_context_data(self,**kwargs):
        from blog.forms import BlogForm
        from tags.models import ManagerTag

        context=super(BlogCreateView,self).get_context_data(**kwargs)
        context["form"] = BlogForm()
        context["tags"] = ManagerTag.objects.only("pk")
        return context

    def post(self,request,*args,**kwargs):
        from blog.forms import BlogForm
        from common.templates import render_for_platform

        self.form_post = BlogForm(request.POST, request.FILES)

        if request.is_ajax() and self.form_post.is_valid() and request.user.is_elect_new_manager():
            post = self.form_post.save(commit=False)
            new_post = post.create_blog(creator=request.user, title=post.title, image=post.image, description=post.description, comments_enabled=post.comments_enabled, votes_on=post.votes_on, tags=request.POST.getlist("tags"))
            return render_for_platform(request, 'blog/detail/blog.html',{'object': new_post})
        else:
            from django.http import HttpResponseBadRequest
            return HttpResponseBadRequest()

class BlogEditView(TemplateView):
    template_name = "blog/edit_blog.html"

    def get(self,request,*args,**kwargs):
        from blog.models import Blog

        self.blog = Blog.objects.get(pk=self.kwargs["pk"])
        return super(BlogEditView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from blog.forms import BlogForm
        from tags.models import ManagerTag

        context=super(BlogEditView,self).get_context_data(**kwargs)
        context["form"] = BlogForm(instance=self.blog)
        context["blog"] = self.blog
        context["tags"] = ManagerTag.objects.only("pk")
        return context

    def post(self,request,*args,**kwargs):
        from blog.forms import BlogForm
        from blog.models import Blog
        from common.templates import render_for_platform

        self.blog = Blog.objects.get(pk=self.kwargs["pk"])
        self.form_post = BlogForm(request.POST, request.FILES, instance=self.blog)

        if request.is_ajax() and self.form_post.is_valid() and request.user.is_supermanager():
            post = self.form_post.save(commit=False)
            new_post = post.edit_blog(title=post.title, image=post.image, description=post.description, comments_enabled=post.comments_enabled, votes_on=post.votes_on, tags=request.POST.getlist("tags"), manager_id=request.user.pk)
            return render_for_platform(request, 'blog/detail/blog.html',{'object': new_post})
        else:
            from django.http import HttpResponseBadRequest
            return HttpResponseBadRequest()


class SuggestElectNew(TemplateView):
    template_name = "elect/add_suggest_elect_new.html"

    def get_context_data(self,**kwargs):
        from blog.forms import SuggestElectNewForm
        from elect.models import Elect

        context=super(SuggestElectNew,self).get_context_data(**kwargs)
        context["form"] = SuggestElectNewForm()
        context["get_elects"] = Elect.objects.only("pk")
        return context

    def post(self,request,*args,**kwargs):
        from blog.forms import SuggestElectNewForm
        from elect.models import Elect
        from common.templates import render_for_platform

        self.form_post = SuggestElectNewForm(request.POST)

        if request.is_ajax() and self.form_post.is_valid() and request.user.is_authenticated:
            post = self.form_post.save(commit=False)
            new_post = post.create_suggested_new(creator=request.user, title=post.title, description=post.description, elect=request.POST.get("elect"), attach=request.POST.getlist("attach_items"), category=post.category)
            return render_for_platform(request, 'elect/news/new.html',{'object': new_post})
        else:
            from django.http import HttpResponseBadRequest
            return HttpResponseBadRequest()

class EditElectNew(TemplateView):
    template_name = "elect/edit_elect_new.html"

    def get(self,request,*args,**kwargs):
        from blog.models import ElectNew

        self.new = ElectNew.objects.get(pk=self.kwargs["pk"])
        return super(EditElectNew,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from blog.forms import ElectNewForm
        from elect.models import Elect

        context=super(EditElectNew,self).get_context_data(**kwargs)
        context["form"] = ElectNewForm(instance=self.new)
        context["get_elects"] = Elect.objects.only("pk")
        context["new"] = self.new
        return context

    def post(self,request,*args,**kwargs):
        from blog.forms import ElectNewForm
        from blog.models import ElectNew
        from common.templates import render_for_platform

        self.new = ElectNew.objects.get(pk=self.kwargs["pk"])
        self.form_post = ElectNewForm(request.POST, instance=self.new)

        if request.is_ajax() and self.form_post.is_valid() and request.user.is_authenticated:
            post = self.form_post.save(commit=False)
            new_post = post.edit_new(title=post.title, description=post.description, elect=request.POST.get("elect"), attach=request.POST.getlist("attach_items"), category=post.category)
            return render_for_platform(request, 'elect/elect_new.html',{'object': new_post})
        else:
            from django.http import HttpResponseBadRequest
            return HttpResponseBadRequest()

class EditManagerElectNew(TemplateView):
    template_name = "elect/edit_manager_elect_new.html"

    def get(self,request,*args,**kwargs):
        from blog.models import ElectNew

        self.new = ElectNew.objects.get(pk=self.kwargs["pk"])
        return super(EditManagerElectNew,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from blog.forms import PublishElectNewForm
        from elect.models import Elect
        from tags.models import ManagerTag

        context=super(EditManagerElectNew,self).get_context_data(**kwargs)
        context["form"] = PublishElectNewForm(instance=self.new)
        context["get_elects"] = Elect.objects.only("pk")
        context["new"] = self.new
        context["tags"] = ManagerTag.objects.only("pk")
        return context

    def post(self,request,*args,**kwargs):
        from blog.forms import PublishElectNewForm
        from blog.models import ElectNew
        from common.templates import render_for_platform

        self.new = ElectNew.objects.get(pk=self.kwargs["pk"])
        self.form_post = PublishElectNewForm(request.POST, instance=self.new)

        if request.is_ajax() and self.form_post.is_valid() and request.user.is_supermanager():
            post = self.form_post.save(commit=False)
            new_post = post.edit_manage_new(title=post.title, description=post.description, elect=request.POST.get("elect"), attach=request.POST.getlist("attach_items"), category=post.category, manager_id=request.user.pk,comments_enabled=post.comments_enabled, votes_on=post.votes_on)
            return render_for_platform(request, 'elect/elect_new.html',{'object': new_post})
        else:
            from django.http import HttpResponseBadRequest
            return HttpResponseBadRequest()

class DeleteElectNew(View):
	def get(self,request,*args,**kwargs):
		from blog.models import ElectNew

		new = ElectNew.objects.get(pk=self.kwargs["pk"])
		if request.is_ajax() and request.user.pk == new.creator.pk and (new.is_suggested() or new.is_rejected()):
			new.delete_item()
			return HttpResponse()
		else:
			raise Http404

class RestoreElectNew(View):
    def get(self,request,*args,**kwargs):
        from blog.models import ElectNew

        new = ElectNew.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.pk == new.creator.pk and new.is_deleted():
            new.restore_item()
            return HttpResponse()
        else:
            raise Http404
