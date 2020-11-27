from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from lists.models import Region
from blog.models import Blog, ElectNew


class MainPageView(TemplateView, CategoryListMixin):
	template_name="main/mainpage.html"

	def get_context_data(self,**kwargs):
		context = super(MainPageView,self).get_context_data(**kwargs)
		context["regions"] = Region.objects.only("pk")
		context["last_elect_news"] = ElectNew.objects.only("pk")[:10]
		context["last_blog_news"] = Blog.objects.only("pk")[:10]
		return context


class MainPhoneSend(TemplateView):
	template_name = "main/phone_verification.html"
