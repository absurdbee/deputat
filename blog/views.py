from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from blog.models import *
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from django.http import Http404
from django.views.generic import ListView
from common.utils import get_small_template
import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from stst.models import BlogNumbers


class BlogDetailView(TemplateView, CategoryListMixin):
	template_name = None

	def get(self,request,*args,**kwargs):
		from common.utils import get_full_template

		self.blog = Blog.objects.get(slug=self.kwargs["slug"])
		self.template_name = get_full_template("blog/blog.html", request.user, request.META['HTTP_USER_AGENT'])
		if request.user.is_authenticated:
			if not BlogNumbers.objects.filter(user=request.user.pk, new=self.blog.pk).exists():
				if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
					BlogNumbers.objects.create(user=request.user.pk, new=self.blog.pk, platform=1)
				else:
					BlogNumbers.objects.create(user=request.user.pk, new=self.blog.pk, platform=0)
			return super(BlogDetailView,self).get(request,*args,**kwargs)
		else:
			if not blog_id in request.COOKIES:
				from django.shortcuts import redirect

				response = redirect('blog_detail', slug=self.blog.slug)
				response.set_cookie(blog_id, "blog_view")
				if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
					BlogNumbers.objects.create(user=request.user.pk, new=self.blog.pk, platform=1)
				else:
					BlogNumbers.objects.create(user=request.user.pk, new=self.blog.pk, platform=0)
				return response
			else:
				return super(BlogDetailView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(BlogDetailView,self).get_context_data(**kwargs)
		context["object"] = self.blog
		context["last_articles"] = Blog.objects.only("pk")[:6]
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
