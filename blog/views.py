from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from blog.models import *
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from django.http import Http404
from django.views.generic import ListView
from common.utils import get_small_template


class BlogDetailView(TemplateView, CategoryListMixin):
	template_name = None

	def get(self,request,*args,**kwargs):
		import re
		MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
		from stst.models import BlogNumbers
		from common.utils import get_full_template

		self.blog = Blog.objects.get(pk=self.kwargs["pk"])
		if request.user.is_authenticated:
			current_pk = request.user.pk
		else:
			current_pk = 0
		if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
			BlogNumbers.objects.create(user=current_pk, blog=self.blog.pk, platform=0)
		else:
			BlogNumbers.objects.create(user=current_pk, blog=self.blog.pk, platform=1)
		self.template_name = get_full_template("blog/blog.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(BlogDetailView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(BlogDetailView,self).get_context_data(**kwargs)
		context["object"] = self.blog
		return context


class AllElectsNewsView(ListView, CategoryListMixin):
	template_name, paginate_by = None, 12

	def get(self,request,*args,**kwargs):
		from taggit.models import Tag

		self.tag = Tag.objects.get(name=self.kwargs["name"])
		self.template_name = get_small_template("blog/elect_news.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(AllElectsNewsView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		return ElectNew.objects.filter(tags__name=self.tag)

	def get_context_data(self, **kwargs):
		context = super(AllElectsNewsView, self).get_context_data(**kwargs)
		context['tag'] = self.tag
		return context


class ProectNewsView(ListView, CategoryListMixin):
	template_name, paginate_by = "blog/blog_news.html", 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_small_template("blog/blog_news.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(ProectNewsView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		return Blog.objects.only("pk")


class BlogCommentList(ListView):
    template_name, paginate_by = "blog_comments.html", 15

    def get(self,request,*args,**kwargs):
	    self.blog = Blog.objects.get(pk=self.kwargs["pk"])
	    return super(BlogCommentList,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
	    context = super(BlogCommentList, self).get_context_data(**kwargs)
	    context['parent'] = self.blog
	    return context

    def get_queryset(self):
	    return self.blog.get_comments()


class BlogCommentCreate(View):
	def post(self,request,*args,**kwargs):
		from blog.forms import BlogCommentForm
		from django.shortcuts import render

		form_post = BlogCommentForm(request.POST)
		blog = Blog.objects.get(pk=request.POST.get('pk'))
		if request.is_ajax() and form_post.is_valid() and blog.comments_enabled:
			comment = form_post.save(commit=False)
			new_comment = comment.create_comment(commenter=request.user, parent=None, blog=blog, text=comment.text)
			return render(request, 'parent.html',{'comment': new_comment})
		else:
			return HttpResponseBadRequest()


class BlogReplyCreate(View):
	def post(self,request,*args,**kwargs):
		from blog.forms import BlogCommentForm
		from django.shortcuts import render
		from common.model.comments import BlogComment

		form_post = BlogCommentForm(request.POST)
		parent = BlogComment.objects.get(pk=request.POST.get('post_comment'))
		if request.is_ajax() and form_post.is_valid():
			comment = form_post.save(commit=False)
			new_comment = comment.create_comment(commenter=request.user, parent=parent, blog=None, text=comment.text)
			return render(request, 'blog_reply.html',{'reply': new_comment, 'comment': parent,})
		else:
			return HttpResponseBadRequest()

class BlogCommentDelete(View):
	def get(self,request,*args,**kwargs):
		from common.model.comments import BlogComment

		comment = BlogComment.objects.get(pk=self.kwargs["pk"])
		if request.is_ajax() and request.user.pk == comment.commenter.pk:
			comment.is_deleted = True
			comment.save(update_fields=['is_deleted'])
			return HttpResponse()
		else:
			raise Http404

class BlogCommentAbortDelete(View):
	from common.model.comments import BlogComment

    def get(self,request,*args,**kwargs):
        comment = BlogComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.pk == comment.commenter.pk:
            comment.is_deleted = False
            comment.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404
