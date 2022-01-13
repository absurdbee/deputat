from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from common.templates import get_small_template
from django.views.generic import ListView
from django.db.models import Q


class SearchView(ListView, CategoryListMixin):
    template_name, paginate_by = None, 20

    def get(self,request,*args,**kwargs):
        self.tag = request.GET.get('tag_name')
        self.elect = request.GET.get('elect_name')
        self._all = request.GET.get('all_name')
        if request.user.is_authenticated:
            self.template_name = "search/search.html"
        else:
            self.template_name = "search/anon_search.html"
        return super(SearchView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(SearchView,self).get_context_data(**kwargs)
        context["tag"] = self.tag
        context["elect"] = self.elect
        context["all"] = self._all
        return context

    def get_queryset(self):
        from blog.models import ElectNew
        from elect.models import Elect
        from itertools import chain

        if self._all:
            query = Q(title__icontains=self._all)|Q(description__icontains=self._all)
            return list(chain(ElectNew.objects.filter(query), Elect.objects.filter(name__icontains=self._all, type='PUB')))
        elif self.tag:
            return ElectNew.objects.filter(tags__name=self.tag)
        elif self.elect:
            return Elect.objects.filter(name__icontains=self.elect, type='PUB')


class AllElectSearch(ListView, CategoryListMixin):
    template_name, paginate_by = None, 20

    def get(self,request,*args,**kwargs):
        self.template_name = get_small_template("search/elect_search.html", request.user, request.META['HTTP_USER_AGENT'])
        self.query = request.GET.get('name')
        return super(AllElectSearch,self).get(request,*args,**kwargs)

    def get_queryset(self):
        from elect.models import Elect
        return Elect.objects.filter(name__icontains=self.query, type='PUB')

    def get_context_data(self,**kwargs):
        context=super(AllElectSearch,self).get_context_data(**kwargs)
        context["query"] = self.query
        return context


class ElectAddElectNewSearch(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_small_template("search/elect_add_elect_new_search.html", request.user, request.META['HTTP_USER_AGENT'])
        self.query = request.GET.get('name')
        return super(ElectAddElectNewSearch,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from elect.models import Elect
        context=super(ElectAddElectNewSearch,self).get_context_data(**kwargs)
        context["query"] = self.query
        context["list"] = Elect.objects.filter(name__icontains=self.query, type='PUB').exclude(list__slug="candidate_municipal")
        return context

class ElectAddBlogSearch(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_small_template("search/elect_add_blog_search.html", request.user, request.META['HTTP_USER_AGENT'])
        self.query = request.GET.get('name')
        return super(ElectAddBlogSearch,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from elect.models import Elect
        context=super(ElectAddBlogSearch,self).get_context_data(**kwargs)
        context["query"] = self.query
        context["list"] = Elect.objects.filter(name__icontains=self.query, type='PUB').exclude(list__slug="candidate_municipal")
        return context

class TagsSearch(ListView, CategoryListMixin):
    template_name, paginate_by = None, 20

    def get(self,request,*args,**kwargs):
        from tags import ManagerTag

        self.template_name = get_small_template("search/tag_search.html", request.user, request.META['HTTP_USER_AGENT'])
        self.tag = ManagerTag.objects.get(pk=self.kwargs["pk"])
        return super(TagsSearch,self).get(request,*args,**kwargs)

    def get_queryset(self):
        from blog.models import ElectNew
        return ElectNew.objects.filter(tags=self.tag)

    def get_context_data(self,**kwargs):
        context=super(TagsSearch,self).get_context_data(**kwargs)
        context["tag"] = self.tag
        return context
