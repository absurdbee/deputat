from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from blog.models import *
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from django.http import Http404
from django.views.generic import ListView
from common.templates import get_small_template
import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from stst.models import BlogNumbers


class BlogDetailView(ListView, CategoryListMixin):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from common.templates import get_full_template

		self.blog = Blog.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_full_template("blog/detail/", "blog.html", request.user, request.META['HTTP_USER_AGENT'])
		if request.user.is_authenticated:
			if not BlogNumbers.objects.filter(user=request.user.pk, new=self.blog.pk).exists():
				if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
					BlogNumbers.objects.create(user=request.user.pk, new=self.blog.pk, platform=1)
				else:
					BlogNumbers.objects.create(user=request.user.pk, new=self.blog.pk, platform=0)
				self.blog.view += 1
				self.blog.save(update_fields=["view"])
			return super(BlogDetailView,self).get(request,*args,**kwargs)
		else:
			if not self.blog.slug in request.COOKIES:
				from django.shortcuts import redirect

				response = redirect('blog_detail', slug=self.blog.slug)
				response.set_cookie(self.blog.slug, "blog_view")
				if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
					BlogNumbers.objects.create(user=0, new=self.blog.pk, platform=1)
				else:
					BlogNumbers.objects.create(user=0, new=self.blog.pk, platform=0)
				self.blog.view += 1
				self.blog.save(update_fields=["view"])
				return response
			else:
				return super(BlogDetailView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(BlogDetailView,self).get_context_data(**kwargs)
		context["object"] = self.blog
		context["last_articles"] = Blog.objects.only("pk")[:6]
		return context

	def get_queryset(self):
		return self.blog.get_comments()


class BlogWindowDetailView(ListView, CategoryListMixin):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from common.templates import get_small_template

		self.blog = Blog.objects.get(pk=self.kwargs["pk"])
		self.articles = Blog.objects.only("pk")
		self.template_name = get_small_template("blog/window/blog.html", request.user, request.META['HTTP_USER_AGENT'])
		if request.user.is_authenticated:
			if not BlogNumbers.objects.filter(user=request.user.pk, new=self.blog.pk).exists():
				if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
					BlogNumbers.objects.create(user=request.user.pk, new=self.blog.pk, platform=1)
				else:
					BlogNumbers.objects.create(user=request.user.pk, new=self.blog.pk, platform=0)
				self.blog.view += 1
				self.blog.save(update_fields=["view"])
			return super(BlogWindowDetailView,self).get(request,*args,**kwargs)
		else:
			if not self.blog.slug in request.COOKIES:
				from django.shortcuts import redirect

				response = redirect('blog_detail', pk=self.blog.pk)
				response.set_cookie(self.blog.slug, "blog_view")
				if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
					BlogNumbers.objects.create(user=0, new=self.blog.pk, platform=1)
				else:
					BlogNumbers.objects.create(user=0, new=self.blog.pk, platform=0)
				self.blog.view += 1
				self.blog.save(update_fields=["view"])
				return response
			else:
				return super(BlogWindowDetailView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(BlogWindowDetailView,self).get_context_data(**kwargs)
		context["object"] = self.blog
		context["next"] = self.articles.filter(pk__gt=self.blog.pk).order_by('pk').first()
		context["prev"] = self.articles.filter(pk__lt=self.blog.pk).order_by('-pk').first()
		return context

	def get_queryset(self):
		return self.blog.get_comments()

class BlogListView(ListView, CategoryListMixin):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_small_template("blog/blog_news.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(BlogListView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		return Blog.objects.only("pk")


class SuggestedElectNews(ListView, CategoryListMixin):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from common.templates import get_managers_template
		self.template_name = get_managers_template("blog/suggested_elect_news.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(SuggestedElectNews,self).get(request,*args,**kwargs)

	def get_queryset(self):
		return ElectNew.objects.filter(type=ElectNew.SUGGESTED)


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
