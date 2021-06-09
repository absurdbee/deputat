from django.views import View
from users.models import User
from django.http import HttpResponse, HttpResponseBadRequest
from common.staff_progs.blog import *
from common.model.comments import BlogComment
from blog.models import Blog
from managers.forms import ModeratedForm
from django.views.generic.base import TemplateView
from managers.models import Moderated
from django.http import Http404
from common.templates import get_detect_platform_template
from logs.model.manage_blog import BlogManageLog


class BlogAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_blog_administrator():
            add_blog_administrator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class BlogAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_blog_administrator():
            remove_blog_administrator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class BlogModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_blog_moderator():
            add_blog_moderator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class BlogModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_blog_moderator():
            remove_blog_moderator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class BlogEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_blog_editor():
            add_post_editor(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class BlogEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_blog_editor():
            remove_blog_editor(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class BlogWorkerAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_blog_administrator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class BlogWorkerAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_blog_administrator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class BlogWorkerModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_blog_moderator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class BlogWorkerModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_blog_moderator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class BlogWorkerEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_blog_editor_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class BlogWorkerEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_blog_editor_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class BlogCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.post = Blog.objects.get(uuid=self.kwargs["uuid"])
        if request.user.is_blog_manager():
            self.template_name = get_detect_platform_template("managers/manage_create/blog/close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(BlogCloseCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(BlogCloseCreate,self).get_context_data(**kwargs)
        context["object"] = self.post
        return context

    def post(self,request,*args,**kwargs):
        post, form = Blog.objects.get(uuid=self.kwargs["uuid"]), ModeratedForm(request.POST)
        if request.is_ajax() and form.is_valid() and request.user.is_blog_manager():
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=post.pk, type="BLO")
            moderate_obj.create_close(object=post, description=mod.description, manager_id=request.user.pk)
            BlogManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=BlogManageLog.ITEM_CLOSED)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class BlogCloseDelete(View):
    def get(self,request,*args,**kwargs):
        post = Blog.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_blog_manager():
            moderate_obj = Moderated.objects.get(object_id=post.pk, type="BLO")
            moderate_obj.delete_close(object=post, manager_id=request.user.pk)
            BlogManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=BlogManageLog.ITEM_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404

class BlogClaimCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.template_name = get_detect_platform_template("managers/manage_create/blog/claim.html", request.user, request.META['HTTP_USER_AGENT'])
        self.new = Blog.objects.get(uuid=self.kwargs["uuid"])
        self.is_reported = ModerationReport.is_user_already_reported(request.user.pk, 'BLO', self.new.pk)
        return super(BlogClaimCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from managers.models import ModerationReport

        context = super(BlogClaimCreate,self).get_context_data(**kwargs)
        context["object"] = self.new
        context["is_reported"] = self.is_reported
        return context

    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.new = Blog.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and not ModerationReport.is_user_already_reported(request.user.pk, 'BLO', self.new.pk):
            description = request.POST.get('description')
            type = request.POST.get('type')
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type="BLO", object_id=self.kwargs["pk"], description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class BlogRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        post = Blog.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_blog_manager():
            moderate_obj = Moderated.objects.get(object_id=post.pk, type="BLO")
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            BlogManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=BlogManageLog.ITEM_REJECT)
            return HttpResponse()
        else:
            raise Http404


class BlogUnverify(View):
    def get(self,request,*args,**kwargs):
        post = Blog.objects.get(uuid=self.kwargs["blog_uuid"])
        obj = Moderated.get_or_create_moderated_object(object_id=post.pk, type="BLO")
        if request.is_ajax() and request.user.is_blog_manager():
            obj.unverify_moderation(post, manager_id=request.user.pk)
            BlogManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=BlogManageLog.ITEM_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404

class RejectBlog(TemplateView):
    template_name = "elect/reject_blog.html"

    def get(self,request,*args,**kwargs):
        self.blog = Blog.objects.get(pk=self.kwargs["pk"])
        return super(RejectBlog,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from managers.forms import ModeratedForm

        context=super(RejectBlog,self).get_context_data(**kwargs)
        context["form"] = ModeratedForm()
        context["object"] = self.blog
        return context

    def post(self,request,*args,**kwargs):
        from managers.forms import ModeratedForm

        self.blog = Blog.objects.get(pk=self.kwargs["pk"])
        self.form_post = ModeratedForm(request.POST)

        if request.is_ajax() and self.form_post.is_valid() and request.user.is_blog_manager():
            post = self.form_post.save(commit=False)
            obj = post.get_or_create_moderated_object("BLO", self.blog.pk)
            obj.description = post.description
            obj.save(update_fields=["description"])
            self.blog.type = "REJ"
            self.blog.save(update_fields=["type"])
            return HttpResponse()
        else:
            from django.http import HttpResponseBadRequest
            return HttpResponseBadRequest()


class CommentBlogClaimCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.comment = BlogComment.objects.get(pk=self.kwargs["pk"])
        self.is_reported = ModerationReport.is_user_already_reported(request.user.pk, 'BLOC', self.comment.pk)
        self.template_name = get_detect_platform_template("managers/manage_create/blog/comment_claim.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(CommentPostClaimCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommentPostClaimCreate,self).get_context_data(**kwargs)
        context["comment"] = self.comment
        context["is_reported"] = self.is_reported
        return context

    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        comment = BlogComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and not ModerationReport.is_user_already_reported(request.user.pk, 'BLOC', comment.pk):
            description = request.POST.get('description')
            type = request.POST.get('type')
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type="BLOС", object_id=comment.pk, description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CommentBlogRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        comment = BlogComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_blog_manager():
            moderate_obj = Moderated.objects.get(object_id=comment.pk, type="BLOC")
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            BlogManageLog.objects.create(item=comment.pk, manager=request.user.pk, action_type=BlogManageLog.COMMENT_REJECT)
            return HttpResponse()
        else:
            raise Http404


class CommentBlogUnverify(View):
    def get(self,request,*args,**kwargs):
        comment = BlogComment.objects.get(pk=self.kwargs["pk"])
        obj = Moderated.get_or_create_moderated_object(object_id=comment.pk, type="BLOC")
        if request.is_ajax() and request.user.is_blog_manager():
            obj.unverify_moderation(comment, manager_id=request.user.pk)
            BlogManageLog.objects.create(item=comment.pk, manager=request.user.pk, action_type=BlogManageLog.COMMENT_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404

class CommentBlogCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.comment = BlogComment.objects.get(pk=self.kwargs["pk"])
        if request.user.is_blog_manager():
            self.template_name = get_detect_platform_template("managers/manage_create/blog/comment_close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(CommentBlogCloseCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommentBlogCloseCreate,self).get_context_data(**kwargs)
        context["comment"] = self.comment
        return context

    def post(self,request,*args,**kwargs):
        comment = BlogComment.objects.get(pk=self.kwargs["pk"])
        form = ModeratedForm(request.POST)
        if form.is_valid() and request.user.is_blog_manager():
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=comment.pk, type="BLOC")
            moderate_obj.create_close(object=comment, description=mod.description, manager_id=request.user.pk)
            BlogManageLog.objects.create(item=comment.pk, manager=request.user.pk, action_type=BlogManageLog.COMMENT_CLOSED)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CommentBlogCloseDelete(View):
    def get(self,request,*args,**kwargs):
        comment = BlogComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_blog_manager():
            moderate_obj = Moderated.objects.get(object_id=comment.pk, type="BLOC")
            moderate_obj.delete_close(object=comment, manager_id=request.user.pk)
            BlogManageLog.objects.create(item=comment.pk, manager=request.user.pk, action_type=BlogManageLog.COMMENT_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404
