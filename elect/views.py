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
        self.template_name = get_full_template("elect/elect/" , "elect.html", request.user, request.META['HTTP_USER_AGENT'])
        if request.user.is_authenticated:
            if not ElectNumbers.objects.filter(user=request.user.pk, elect=self.elect.pk).exists():
                if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
                    ElectNumbers.objects.create(user=request.user.pk, elect=self.elect.pk, platform=1)
                else:
                    ElectNumbers.objects.create(user=request.user.pk, elect=self.elect.pk, platform=0)
                self.elect.view += 1
                self.elect.save(update_fields=["view"])
            return super(ElectDetailView,self).get(request,*args,**kwargs)
        else:
            if not "elect_" + str(self.elect.pk) in request.COOKIES:
                from django.shortcuts import redirect

                response = redirect('elect_detail', pk=self.elect.pk)
                response.set_cookie("elect_" + str(self.elect.pk), "elect_view")
                if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
                    ElectNumbers.objects.create(user=0, elect=self.elect.pk, platform=1)
                else:
                    ElectNumbers.objects.create(user=0, elect=self.elect.pk, platform=0)
                self.elect.view += 1
                self.elect.save(update_fields=["view"])
                return response
            else:
                return super(ElectDetailView,self).get(request,*args,**kwargs)
        return super(ElectDetailView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ElectDetailView,self).get_context_data(**kwargs)
        context["object"] = self.elect
        context["last_articles"] = ElectNew.objects.filter(type="PUB")[:6]
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
        news = ElectNew.objects.filter(elect=self.elect, type=ElectNew.PUBLISHED)
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
        news = ElectNew.objects.filter(elect=self.elect, category__slug="statements", type=ElectNew.PUBLISHED)
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
        news = ElectNew.objects.filter(elect=self.elect, category__slug="work_with_voters", type=ElectNew.PUBLISHED)
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
        news = ElectNew.objects.filter(elect=self.elect, category__slug="pre_election_activities", type=ElectNew.PUBLISHED)
        return news


class ElectNewDetailView(ListView, CategoryListMixin):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        import re
        from stst.models import ElectNewNumbers
        from datetime import datetime
        MOBILE_AGENT_RE, user_agent = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE), request.META['HTTP_USER_AGENT']

        self.new, folder, template = ElectNew.objects.get(pk=self.kwargs["pk"]), "elect/news/", "new.html"
        if request.user.is_authenticated:
            if MOBILE_AGENT_RE.match(user_agent):
                request.user.last_activity, request.user.device = datetime.now(), "Ph"
                request.user.save(update_fields=['last_activity', 'device'])
            else:
                request.user.last_activity, request.user.device = datetime.now(), "De"
                request.user.save(update_fields=['last_activity', 'device'])
            if request.user.type[0] == "_":
                from common.templates import get_fine_request_user
                _template = get_fine_request_user(request.user)
            elif self.new.type[0] == "_":
                if self.new.is_suggested():
                    if self.new.creator.pk == request.user.pk:
                        _template = folder + "my_suggested_" + template
                    elif request.user.is_elect_new_manager():
                        _template = folder + "staff_suggested_" + template
                    else:
                        from rest_framework.exceptions import PermissionDenied
                        raise PermissionDenied("Ошибка доступа")
                elif self.new.is_deleted():
                    if self.new.creator.pk == request.user.pk:
                        _template = folder + "my_deleted_" + template
                    else:
                        return "generic/u_template/deleted.html"
                elif self.new.is_closed():
                    if self.new.creator.pk == request.user.pk:
                        _template = folder + "my_closed_" + template
                    else:
                        _template = folder + "closed_" + template
                elif self.new.is_suspended():
                    if self.new.creator.pk == request.user.pk:
                        _template = folder + "my_suspended_" + template
                    else:
                        _template = "generic/u_template/suspended.html"
            else:
                if self.new.creator.pk == request.user.pk:
                    _template = folder + "my_" + template
                else:
                    _template = folder + template
                if not ElectNewNumbers.objects.filter(user=request.user.pk, new=self.new.pk).exists():
                    if MOBILE_AGENT_RE.match(user_agent):
                        ElectNewNumbers.objects.create(user=request.user.pk, new=self.new.pk, platform=1)
                    else:
                        ElectNewNumbers.objects.create(user=request.user.pk, new=self.new.pk, platform=0)
                    self.new.view += 1
                    self.new.save(update_fields=["view"])
            if MOBILE_AGENT_RE.match(user_agent):
                self.template_name = "" + _template
            else:
                self.template_name = "" + _template

            return super(ElectNewDetailView,self).get(request,*args,**kwargs)
        else:
            if MOBILE_AGENT_RE.match(user_agent):
                self.template_name = "" + folder + "anon_new.html"
            else:
                self.template_name = "" + folder + "anon_new.html"
            if self.new.type[0] == "_":
                if self.new.is_deleted():
                    return "generic/u_template/anon_deleted.html"
                elif self.new.is_closed():
                    return folder + "anon_closed_new.html"
                elif self.new.is_suspended():
                    return "generic/u_template/anon_suspended.html"
                else:
                    from rest_framework.exceptions import PermissionDenied
                    raise PermissionDenied("Ошибка доступа")
            else:
                if not str(self.new.id) in request.COOKIES:
                    from django.shortcuts import redirect
                    response = redirect('elect_new_detail', pk=self.new.pk)
                    response.set_cookie(str(self.new.pk), "elect_new_view")
                    if MOBILE_AGENT_RE.match(user_agent):
                        ElectNewNumbers.objects.create(user=0, new=self.new.pk, platform=1)
                    else:
                        ElectNewNumbers.objects.create(user=0, new=self.new.pk, platform=0)
                    self.new.view += 1
                    self.new.save(update_fields=["view"])
                    return response
        return super(ElectNewDetailView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ElectNewDetailView,self).get_context_data(**kwargs)
        context["object"] = self.new
        return context

    def get_queryset(self):
        return self.new.get_comments()

class ElectNewWindowDetailView(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        import re
        from stst.models import ElectNewNumbers
        from datetime import datetime
        MOBILE_AGENT_RE, user_agent = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE), request.META['HTTP_USER_AGENT']

        self.new, folder, template = ElectNew.objects.get(pk=self.kwargs["pk"]), "elect/new_window/", "new.html"
        self.news = self.new.elect.get_news()
        if request.user.is_authenticated:
            if MOBILE_AGENT_RE.match(user_agent):
                request.user.last_activity, request.user.device = datetime.now(), "Ph"
                request.user.save(update_fields=['last_activity', 'device'])
            else:
                request.user.last_activity, request.user.device = datetime.now(), "De"
                request.user.save(update_fields=['last_activity', 'device'])
            if request.user.type[0] == "_" or self.new.type[0] == "_":
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied("Ошибка доступа")
            else:
                _template = folder + template
                if not ElectNewNumbers.objects.filter(user=request.user.pk, new=self.new.pk).exists():
                    if MOBILE_AGENT_RE.match(user_agent):
                        ElectNewNumbers.objects.create(user=request.user.pk, new=self.new.pk, platform=1)
                    else:
                        ElectNewNumbers.objects.create(user=request.user.pk, new=self.new.pk, platform=0)
                    self.new.view += 1
                    self.new.save(update_fields=["view"])
            if MOBILE_AGENT_RE.match(user_agent):
                self.template_name = "" + _template
            else:
                self.template_name = "" + _template

            return super(ElectNewWindowDetailView,self).get(request,*args,**kwargs)
        else:
            if MOBILE_AGENT_RE.match(user_agent):
                self.template_name = "" + folder + "anon_new.html"
            else:
                self.template_name = "" + folder + "anon_new.html"
            if self.new.type[0] == "_":
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied("Ошибка доступа")
            else:
                if not str(self.new.id) in request.COOKIES:
                    from django.shortcuts import redirect
                    response = redirect('elect_new_detail', pk=self.new.pk)
                    response.set_cookie(str(self.new.pk), "elect_new_view")
                    if MOBILE_AGENT_RE.match(user_agent):
                        ElectNewNumbers.objects.create(user=0, new=self.new.pk, platform=1)
                    else:
                        ElectNewNumbers.objects.create(user=0, new=self.new.pk, platform=0)
                    self.new.view += 1
                    self.new.save(update_fields=["view"])
                    return response
        return super(ElectNewWindowDetailView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ElectNewWindowDetailView,self).get_context_data(**kwargs)
        context["object"] = self.new
        context["next"] = self.news.filter(pk__gt=self.photo.pk).order_by('pk').first()
        context["prev"] = self.news.filter(pk__lt=self.photo.pk).order_by('-pk').first()
        return context

    def get_queryset(self):
        return self.new.get_comments()
