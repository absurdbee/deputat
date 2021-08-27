from django.views.generic.base import ContextMixin
from django.conf import settings
from lists.models import AuthorityList


class CategoryListMixin(ContextMixin):
	def get_context_data(self,**kwargs):
		context = super(CategoryListMixin,self).get_context_data(**kwargs)
		context["current_url"] = self.request.path
		context["federal_elect_list"] = AuthorityList.objects.filter(is_in_left_menu=True)
		if self.request.user.is_authenticated:
			context["user_region"] = self.request.user.city.region
			context["user_city"] = self.request.user.city
		#else:
		#	context["user_region"] = None
		#	context["user_city"] = None
		return context
