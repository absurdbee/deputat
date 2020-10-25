from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from lists.models import Region


class MainPageView(TemplateView, CategoryListMixin):
	template_name="main/mainpage.html"

	def get_context_data(self,**kwargs):
		context = super(MainPageView,self).get_context_data(**kwargs)
		context["regions"] = Region.objects.only("pk")
		return context
