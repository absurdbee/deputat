from blog.models import *
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from django.http import Http404
from django.views.generic.base import TemplateView
from common.templates import get_small_template
from common.model.comments import *


class BlogCommentCreate(View):
	def post(self,request,*args,**kwargs):
		from blog.forms import BlogCommentForm
		from common.templates import render_for_platform

		form_post = BlogCommentForm(request.POST)
		blog = Blog.objects.get(pk=request.POST.get('blog'))
		if request.is_ajax() and form_post.is_valid() and blog.comments_enabled:
			comment = form_post.save(commit=False)
			new_comment = comment.create_comment(
													commenter=request.user,
													blog=blog,
													parent=None,
													text=comment.text,
													attach = request.POST.getlist("attach_items")
												)
			return render_for_platform(request, 'blog/comment/parent.html',{'comment': new_comment})
		else:
			return HttpResponseBadRequest()


class BlogCommentEdit(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.template_name = get_small_template("blog/comment/edit.html", request.user, request.META['HTTP_USER_AGENT'])
		self.comment = BlogComment.objects.get(pk=self.kwargs["pk"])
		return super(BlogCommentEdit,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		from blog.forms import BlogCommentForm

		context = super(BlogCommentEdit,self).get_context_data(**kwargs)
		context["comment"] = self.comment
		context["form_post"] = BlogCommentForm(instance=self.comment)
		return context

	def post(self,request,*args,**kwargs):
		from common.templates import render_for_platform
		from blog.forms import BlogCommentForm

		self.comment = BlogComment.objects.get(pk=self.kwargs["pk"])
		self.form = BlogCommentForm(request.POST,instance=self.comment)
		if request.is_ajax() and self.form.is_valid():
			_comment = self.form.save(commit=False)
			new_comment = _comment.edit_comment(text=_comment.text, attach = request.POST.getlist("attach_items"))
			if self.comment.parent:
				return render_for_platform(request, 'blog/comment/reply.html',{'reply': self.comment}) 
			else:
				return render_for_platform(request, 'blog/comment/parent.html',{'comment': self.comment})
		else:
			return HttpResponseBadRequest()
		return super(BlogCommentEdit,self).get(request,*args,**kwargs)


class BlogReplyCreate(View):
	def post(self,request,*args,**kwargs):
		from blog.forms import BlogCommentForm
		from django.shortcuts import render
		from common.model.comments import BlogComment

		form_post = BlogCommentForm(request.POST)
		parent = BlogComment.objects.get(pk=request.POST.get('post_comment'))
		if request.is_ajax() and form_post.is_valid():
			comment = form_post.save(commit=False)
			new_comment = comment.create_comment(
													commenter=request.user,
													blog=parent.blog,
													parent=parent,
													text=comment.text,
													attach = request.POST.getlist("attach_items")
												)
			return render(request, 'blog/comment/reply.html',{'reply': new_comment, 'comment': parent,})
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


class ElectNewCommentCreate(View):
	def post(self,request,*args,**kwargs):
		from blog.forms import ElectNewCommentForm
		from django.shortcuts import render

		form_post = ElectNewCommentForm(request.POST)
		new = ElectNew.objects.get(pk=request.POST.get('pk'))
		if request.is_ajax() and form_post.is_valid() and new.comments_enabled:
			comment = form_post.save(commit=False)
			new_comment = comment.create_comment(commenter=request.user, parent=None, new=new, text=comment.text)
			return render(request, 'blog/elect_new_comment/new_parent.html',{'comment': new_comment})
		else:
			return HttpResponseBadRequest()


class ElectNewReplyCreate(View):
	def post(self,request,*args,**kwargs):
		from blog.forms import ElectNewCommentForm
		from django.shortcuts import render
		from common.model.comments import ElectNewComment

		form_post = ElectNewCommentForm(request.POST)
		parent = ElectNewComment.objects.get(pk=request.POST.get('post_comment'))
		if request.is_ajax() and form_post.is_valid():
			comment = form_post.save(commit=False)
			new_comment = comment.create_comment(commenter=request.user, parent=parent, new=None, text=comment.text)
			return render(request, 'blog/elect_new_comment/new_reply.html',{'reply': new_comment, 'comment': parent,})
		else:
			return HttpResponseBadRequest()

class ElectNewCommentDelete(View):
	def get(self,request,*args,**kwargs):
		from common.model.comments import ElectNewComment

		comment = ElectNewComment.objects.get(pk=self.kwargs["pk"])
		if request.is_ajax() and request.user.pk == comment.commenter.pk:
			comment.is_deleted = True
			comment.save(update_fields=['is_deleted'])
			return HttpResponse()
		else:
			raise Http404

class ElectNewCommentAbortDelete(View):
	from common.model.comments import ElectNewComment

	def get(self,request,*args,**kwargs):
		comment = ElectNewComment.objects.get(pk=self.kwargs["pk"])
		if request.is_ajax() and request.user.pk == comment.commenter.pk:
			comment.is_deleted = False
			comment.save(update_fields=['is_deleted'])
			return HttpResponse()
		else:
			raise Http404
