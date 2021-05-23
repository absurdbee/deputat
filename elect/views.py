from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from elect.models import Elect
from blog.models import ElectNew
from django.views.generic import ListView
from common.templates import get_small_template


"""
    Группируем все представления депутата здесь:
    1. Страница отдельного депутата,
    2. Список всех новостей депутата для подгрузки
	3. Список новостей о высказываниях депутата для подгрузки
	4. Список новостей о работа с избирателями депутата для подгрузки
	5. Список новостей о предвыборная деятельности депутата для подгрузки
	6. Страница отдельной новости депутата
"""

class ElectDetailView(TemplateView, CategoryListMixin):
    template_name = None

    def get(self,request,*args,**kwargs):
        import re
        MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
        from stst.models import ElectNumbers
        from common.templates import get_full_template

        self.elect = Elect.objects.get(pk=self.kwargs["pk"])
        if request.user.is_authenticated:
            current_pk = request.user.pk
        else:
            current_pk = 0
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            ElectNumbers.objects.create(user=current_pk, elect=self.elect.pk, platform=0)
        else:
            ElectNumbers.objects.create(user=current_pk, elect=self.elect.pk, platform=1)
        self.template_name = get_full_template("elect/elect_2.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(ElectDetailView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ElectDetailView,self).get_context_data(**kwargs)
        context["object"] = self.elect
        context["last_articles"] = ElectNew.objects.only("pk")[:6]
        return context


class AllElectNewsView(ListView, CategoryListMixin):
    template_name = None
    paginate_by = 12

    def get(self,request,*args,**kwargs):
        self.elect = Elect.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_small_template("elect/all_news.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(AllElectNewsView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllElectNewsView,self).get_context_data(**kwargs)
        context["elect"] = self.elect
        return context

    def get_queryset(self):
        news = ElectNew.objects.filter(elect=self.elect, status=ElectNew.STATUS_PUBLISHED)
        return news

class StatementsElectNewsView(ListView, CategoryListMixin):
    template_name = None
    paginate_by = 12

    def get(self,request,*args,**kwargs):
        self.elect = Elect.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_small_template("elect/statements_news.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(StatementsElectNewsView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(StatementsElectNewsView,self).get_context_data(**kwargs)
        context["elect"] = self.elect
        return context

    def get_queryset(self):
        news = ElectNew.objects.filter(elect=self.elect, category__slug="statements", status=ElectNew.STATUS_PUBLISHED)
        return news


class WorkWithVotersElectNewsView(ListView, CategoryListMixin):
    template_name = None
    paginate_by = 12

    def get(self,request,*args,**kwargs):
        self.elect = Elect.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_small_template("elect/work_with_voters.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(WorkWithVotersElectNewsView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(WorkWithVotersElectNewsView,self).get_context_data(**kwargs)
        context["elect"] = self.elect
        return context

    def get_queryset(self):
        news = ElectNew.objects.filter(elect=self.elect, category__slug="work_with_voters", status=ElectNew.STATUS_PUBLISHED)
        return news

class PreElectionElectNewsView(ListView, CategoryListMixin):
    template_name = None
    paginate_by = 12

    def get(self,request,*args,**kwargs):
        self.elect = Elect.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_small_template("elect/pre_election_activities.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(PreElectionElectNewsView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PreElectionElectNewsView,self).get_context_data(**kwargs)
        context["elect"] = self.elect
        return context

    def get_queryset(self):
        news = ElectNew.objects.filter(elect=self.elect, category__slug="pre_election_activities", status=ElectNew.STATUS_PUBLISHED)
        return news


class ElectNewDetailView(TemplateView, CategoryListMixin):
    template_name = None

    def get(self,request,*args,**kwargs):
        import re
        MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
        from stst.models import ElectNewNumbers
        from common.templates import get_full_template

        self.new = ElectNew.objects.get(pk=self.kwargs["pk"])
        if request.user.is_authenticated:
            current_pk = request.user.pk
        else:
            current_pk = 0
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            ElectNewNumbers.objects.create(user=current_pk, new=self.new.pk, platform=0)
        else:
            ElectNewNumbers.objects.create(user=current_pk, new=self.new.pk, platform=1)
        self.template_name = get_full_template("elect/elect_new.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(ElectNewDetailView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ElectNewDetailView,self).get_context_data(**kwargs)
        context["object"] = self.new
        return context
