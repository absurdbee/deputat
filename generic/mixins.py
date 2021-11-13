from django.views.generic.base import ContextMixin
from django.conf import settings
from lists.models import AuthorityList, AuthorityListCategory
from region.models import Region
from district.models import District2

class CategoryListMixin(ContextMixin):
	def get_context_data(self,**kwargs):
		context = super(CategoryListMixin,self).get_context_data(**kwargs)
		context["current_url"] = self.request.path
		context["elect_list_cats"] = AuthorityListCategory.objects.only("pk")
		if self.request.user.is_authenticated:
			try:
				context["user_region"] = self.request.user.city.region
				#context["user_district"] = self.request.user.area
			except:
				context["user_region"] = Region.objects.first()
				context["user_district"] = District2.objects.first()
		return context
