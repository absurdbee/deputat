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
        context["get_elects"] = Elect.objects.filter(list__is_reginal=False)
        return context

    def post(self,request,*args,**kwargs):
        from blog.forms import SuggestElectNewForm
        from elect.models import Elect
        from common.templates import render_for_platform

        self.form_post = SuggestElectNewForm(request.POST)

        if request.is_ajax() and self.form_post.is_valid() and request.user.is_authenticated:
            post = self.form_post.save(commit=False)
            new_post = post.create_suggested_new(creator=request.user, title=post.title, description=post.description, elect=request.POST.get("elect"), attach=request.POST.getlist("attach_items"), category=post.category)
            return HttpResponse()
        else:
            from django.http import HttpResponseBadRequest
            return HttpResponseBadRequest()

class EditElectNew(TemplateView):
    template_name, senat, state_duma, candidate_duma, candidate_municipal, senat_elect_list, elect_region, elect_lists = "elect/edit_elect_new.html", False, False, False, False, None, None, None

    def get(self,request,*args,**kwargs):
        from blog.models import ElectNew
        from elect.models import Elect

        self.new = ElectNew.objects.get(pk=self.kwargs["pk"])
        elect = self.new.elect
        if elect.region:
            self.elect_region = elect.region.all().first()
        elif elect.okrug:
            self.elect_region = elect.okrug.region
        else:
            self.elect_region = elect.area.all().first().region
        self.elect_list = elect.list.all().first()

        if self.elect_list.slug == "senat":
            self.senat = True
            self.senat_elect_list = Elect.objects.filter(list__slug=self.elect_list.slug)
        elif self.elect_list.slug == "state_duma":
            self.state_duma = True
            self.elect_lists = Elect.objects.filter(list__slug=self.elect_list.slug, region=self.elect_region)
        elif self.elect_list.slug == "candidate_duma":
            self.candidate_duma = True
            self.elect_lists = Elect.objects.filter(list__slug=self.elect_list.slug, region=self.elect_region)
        elif self.elect_list.slug == "candidate_municipal":
            self.candidate_municipal = True
            self.elect_lists = Elect.objects.filter(list__slug=self.elect_list.slug, region=self.elect_region)
        return super(EditElectNew,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from blog.forms import SuggestElectNewForm
        from region.models import Region

        context=super(EditElectNew,self).get_context_data(**kwargs)
        context["form"] = SuggestElectNewForm(instance=self.new)
        context["senat"] = self.senat
        context["senat_elect_list"] = self.senat_elect_list
        context["state_duma"] = self.state_duma
        context["candidate_duma"] = self.candidate_duma
        context["candidate_municipal"] = self.candidate_municipal
        context["new"] = self.new
        context["elect_region_pk"] = self.elect_region.pk
        context["elect_lists"] = self.elect_lists
        context["regions"] = Region.objects.filter(is_deleted=False)
        return context

    def post(self,request,*args,**kwargs):
        from blog.forms import SuggestElectNewForm
        from blog.models import ElectNew
        from common.templates import render_for_platform

        self.new = ElectNew.objects.get(pk=self.kwargs["pk"])
        self.form_post = SuggestElectNewForm(request.POST, instance=self.new)

        if request.is_ajax() and self.form_post.is_valid() and request.user.is_authenticated:
            post = self.form_post.save(commit=False)
            new_post = post.edit_new(title=post.title, description=post.description, elect=request.POST.get("elect"), attach=request.POST.getlist("attach_items"), category=post.category)
            return HttpResponse()
        else:
            from django.http import HttpResponseBadRequest
            return HttpResponseBadRequest()

class EditManagerElectNew(TemplateView):
    template_name, senat, state_duma, candidate_duma, candidate_municipal, senat_elect_list, elect_region, elect_lists = "elect/edit_manager_elect_new.html", False, False, False, False, None, None, None

    def get(self,request,*args,**kwargs):
        from blog.models import ElectNew
        from elect.models import Elect

        self.new = ElectNew.objects.get(pk=self.kwargs["pk"])
        elect = self.new.elect
        if elect.region:
            self.elect_region = elect.region.all().first()
        elif elect.okrug:
            self.elect_region = elect.okrug.region
        else:
            self.elect_region = elect.area.all().first().region
        self.elect_list = elect.list.all().first()

        if self.elect_list.slug == "senat":
            self.senat = True
            self.senat_elect_list = Elect.objects.filter(list__slug=self.elect_list.slug)
        elif self.elect_list.slug == "state_duma":
            self.state_duma = True
            self.elect_lists = Elect.objects.filter(list__slug=self.elect_list.slug, region=self.elect_region)
        elif self.elect_list.slug == "candidate_duma":
            self.candidate_duma = True
            self.elect_lists = Elect.objects.filter(list__slug=self.elect_list.slug, region=self.elect_region)
        elif self.elect_list.slug == "candidate_municipal":
            self.candidate_municipal = True
            self.elect_lists = Elect.objects.filter(list__slug=self.elect_list.slug, region=self.elect_region)
        return super(EditManagerElectNew,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from blog.forms import PublishElectNewForm
        from region.models import Region

        context=super(EditManagerElectNew,self).get_context_data(**kwargs)
        context["form"] = PublishElectNewForm(instance=self.new)
        context["senat"] = self.senat
        context["senat_elect_list"] = self.senat_elect_list
        context["state_duma"] = self.state_duma
        context["candidate_duma"] = self.candidate_duma
        context["candidate_municipal"] = self.candidate_municipal
        context["new"] = self.new
        context["elect_region_pk"] = self.elect_region.pk
        context["elect_lists"] = self.elect_lists
        context["regions"] = Region.objects.filter(is_deleted=False)
        return context

    def post(self,request,*args,**kwargs):
        from blog.forms import PublishElectNewForm
        from blog.models import ElectNew
        from common.templates import render_for_platform

        self.new = ElectNew.objects.get(pk=self.kwargs["pk"])
        self.form_post = PublishElectNewForm(request.POST, instance=self.new)

        if request.is_ajax() and self.form_post.is_valid() and request.user.is_supermanager():
            post = self.form_post.save(commit=False)
            new_post = post.edit_manage_new(title=post.title, tags=request.POST.getlist("tags"), description=post.description, elect=request.POST.get("elect"), attach=request.POST.getlist("attach_items"), category=post.category, manager_id=request.user.pk,comments_enabled=post.comments_enabled, votes_on=post.votes_on)
            return HttpResponse()
        else:
            from django.http import HttpResponseBadRequest
            return HttpResponseBadRequest()

class DeleteElectNew(View):
    def get(self,request,*args,**kwargs):
        from blog.models import ElectNew

        new = ElectNew.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax():
            if request.user.pk == new.creator.pk and (new.is_suggested() or new.is_rejected()):
                new.delete_item()
            elif request.user.is_elect_new_manager():
                new.delete_item()
            return HttpResponse()
        else:
            raise Http404

class RestoreElectNew(View):
    def get(self,request,*args,**kwargs):
        from blog.models import ElectNew

        new = ElectNew.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax():
            if request.user.pk == new.creator.pk and new.is_deleted():
                new.restore_item()
            elif request.user.is_elect_new_manager():
                new.restore_item()
            return HttpResponse()
        else:
            raise Http404

class DeleteBlog(View):
	def get(self,request,*args,**kwargs):
		from blog.models import Blog

		blog = Blog.objects.get(pk=self.kwargs["pk"])
		if request.is_ajax() and request.user.is_supermanager():
			blog.delete_item()
			return HttpResponse()
		else:
			raise Http404

class RestoreBlog(View):
    def get(self,request,*args,**kwargs):
        from blog.models import Blog

        blog = Blog.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_supermanager():
            blog.restore_item()
            return HttpResponse()
        else:
            raise Http404


class BlogAddRepostCountVk(View):
    def get(self,request,*args,**kwargs):
        from blog.models import Blog

        blog = Blog.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and not ("blog_repost_vk_" + blog.slug) in request.COOKIES:
            from django.shortcuts import redirect

            response = redirect('blog_detail', slug=blog.slug)
            response.set_cookie("blog_repost_vk_" + blog.slug, "blog_repost_vk_" + blog.slug)
            blog.repost += 1
            blog.save(update_fields=["repost"])
            return response
        else:
            return HttpResponse()
class BlogAddRepostCountFb(View):
    def get(self,request,*args,**kwargs):
        from blog.models import Blog

        blog = Blog.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and not ("blog_repost_fb_" + blog.slug) in request.COOKIES:
            from django.shortcuts import redirect

            response = redirect('blog_detail', slug=blog.slug)
            response.set_cookie("blog_repost_fb_" + blog.slug, "blog_repost_fb_" + blog.slug)
            blog.repost += 1
            blog.save(update_fields=["repost"])
            return response
        else:
            return HttpResponse()
class BlogAddRepostCountTw(View):
    def get(self,request,*args,**kwargs):
        from blog.models import Blog

        blog = Blog.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and not ("blog_repost_tw_" + blog.slug) in request.COOKIES:
            from django.shortcuts import redirect

            response = redirect('blog_detail', slug=blog.slug)
            response.set_cookie("blog_repost_tw_" + blog.slug, "blog_repost_tw_" + blog.slug)
            blog.repost += 1
            blog.save(update_fields=["repost"])
            return response
        else:
            return HttpResponse()
class BlogAddRepostCountTg(View):
    def get(self,request,*args,**kwargs):
        from blog.models import Blog

        blog = Blog.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and not ("blog_repost_tg_" + blog.slug) in request.COOKIES:
            from django.shortcuts import redirect

            response = redirect('blog_detail', slug=blog.slug)
            response.set_cookie("blog_repost_tg_" + blog.slug, "blog_repost_tg_" + blog.slug)
            blog.repost += 1
            blog.save(update_fields=["repost"])
            return response
        else:
            return HttpResponse()


class ElectNewAddRepostCountVk(View):
    def get(self,request,*args,**kwargs):
        from blog.models import ElectNew

        new = ElectNew.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and not ("new_repost_vk_" + str(new.pk)) in request.COOKIES:
            from django.shortcuts import redirect

            response = redirect('elect_new_detail', pk=new.pk)
            response.set_cookie("new_repost_vk_" + str(new.pk), "new_repost_vk_" + str(new.pk))
            new.repost += 1
            new.save(update_fields=["repost"])
            return response
        else:
            return HttpResponse()
class ElectNewAddRepostCountFb(View):
    def get(self,request,*args,**kwargs):
        from blog.models import ElectNew

        new = ElectNew.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and not ("new_repost_fb_" + str(new.pk)) in request.COOKIES:
            from django.shortcuts import redirect

            response = redirect('elect_new_detail', pk=new.pk)
            response.set_cookie("new_repost_fb_" + str(new.pk), "new_repost_fb_" + str(new.pk))
            new.repost += 1
            new.save(update_fields=["repost"])
            return response
        else:
            return HttpResponse()
class ElectNewAddRepostCountTg(View):
    def get(self,request,*args,**kwargs):
        from blog.models import ElectNew

        new = ElectNew.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and not ("new_repost_tg_" + str(new.pk)) in request.COOKIES:
            from django.shortcuts import redirect

            response = redirect('elect_new_detail', pk=new.pk)
            response.set_cookie("new_repost_tg_" + str(new.pk), "new_repost_tg_" + str(new.pk))
            new.repost += 1
            new.save(update_fields=["repost"])
            return response
        else:
            return HttpResponse()
class ElectNewAddRepostCountTw(View):
    def get(self,request,*args,**kwargs):
        from blog.models import ElectNew

        new = ElectNew.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and not ("new_repost_tw_" + str(new.pk)) in request.COOKIES:
            from django.shortcuts import redirect

            response = redirect('elect_new_detail', pk=new.pk)
            response.set_cookie("new_repost_tw_" + str(new.pk), "new_repost_tw_" + str(new.pk))
            new.repost += 1
            new.save(update_fields=["repost"])
            return response
        else:
            return HttpResponse()
