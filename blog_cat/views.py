from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from django.views.generic import ListView
from lists.models import BlogCategory
from blog.models import Blog
from common.utils import get_small_template


class BlogListView(ListView, CategoryListMixin):
	template_name = None
	paginate_by = 20

	def get(self,request,*args,**kwargs):
        self.template_name = get_small_template("blog/blog_index.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(BlogListView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		blog = Blog.objects.only("pk")
		return blog
