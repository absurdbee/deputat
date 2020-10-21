from django.views.generic.base import ContextMixin
from django.conf import settings
from lists.models import ElectList, BlogCategory


class CategoryListMixin(ContextMixin):

	def get_context_data(self,**kwargs):
		context = super(CategoryListMixin,self).get_context_data(**kwargs)
		context["current_url"] = self.request.path
		context["elect_list"] = ElectList.objects.only("pk")
		context["blog_cat"] = BlogCategory.objects.only("pk")
		return context
