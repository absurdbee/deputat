from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from django.views.generic import ListView
from lists.models import BlogCategory
from blog.models import Blog


class BlogListView(ListView, CategoryListMixin):
	model = Blog
	template_name = "blog_index.html"
	paginate_by = 20

	def get(self,request,*args,**kwargs):
		if self.kwargs["slug"] == None:
			self.cat = BlogCategory.objects.first()
		else:
			self.cat = BlogCategory.objects.get(slug=self.kwargs["slug"])
		return super(BlogListView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		blog = Blog.objects.filter(category=self.cat)
		return blog

	def get_context_data(self,**kwargs):
		context = super(BlogListView,self).get_context_data(**kwargs)
		context["category"] = self.cat
		return context

class BlogLists(TemplateView, CategoryListMixin):
    template_name = "blog_list.html"
