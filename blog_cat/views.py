from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from django.views.generic import ListView
from lists.models import BlogCategory
from blog.models import Blog


class BlogListView(ListView, CategoryListMixin):
	model = Blog
	template_name = "blog/blog_index.html"
	paginate_by = 20

	def get_queryset(self):
		blog = Blog.objects.only("pk")
		return blog
