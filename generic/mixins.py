from django.views.generic.base import ContextMixin
from django.conf import settings
from lists.models import AuthorityList, BlogCategory


class CategoryListMixin(ContextMixin):

	def get_context_data(self,**kwargs):
		context = super(CategoryListMixin,self).get_context_data(**kwargs)
		context["current_url"] = self.request.path
		context["federal_elect_list"] = AuthorityList.objects.filter(is_reginal=False)
		context["blog_cat"] = BlogCategory.objects.only("pk")
		return context
