from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from common.templates import get_small_template


class SearchView(TemplateView, CategoryListMixin):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_small_template("search/search.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(SearchView,self).get(request,*args,**kwargs)


class AllElectSearch(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_small_template("search/elect_search.html", request.user, request.META['HTTP_USER_AGENT'])
        self.query = request.GET.get('elect_search')
		return super(AllElectSearch,self).get(request,*args,**kwargs)

	def get_queryset(self):
        from elects.models import Elect
		return Elect.objects.filter(name__icontains=self.query)

    def get_context_data(self,**kwargs):
		context=super(AllElectSearch,self).get_context_data(**kwargs)
		context["query"] = self.query
		return context
