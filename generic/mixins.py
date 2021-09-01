from django.views.generic.base import ContextMixin
from django.conf import settings
from lists.models import AuthorityList
from region.models import Region
from city.models import City


class CategoryListMixin(ContextMixin):
	def get_context_data(self,**kwargs):
		context = super(CategoryListMixin,self).get_context_data(**kwargs)
		context["current_url"] = self.request.path
		context["federal_elect_list"] = AuthorityList.objects.filter(is_in_left_menu=True)
		if self.request.user.is_authenticated:
			try:
				context["user_region"] = self.request.user.city.region
				context["user_city"] = self.request.user.city
			except:
				context["user_region"] = Region.objects.get(pk=1)
				context["user_city"] = City.objects.get(pk=1)
		#else:
		#	context["user_region"] = None
		#	context["user_city"] = None
		return context
