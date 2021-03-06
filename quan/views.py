from django.views.generic.base import TemplateView
from django.views.generic import ListView
from quan.models import *
from common.templates import get_detect_platform_template
from generic.mixins import CategoryListMixin
from django.views import View
from django.http import HttpResponse, Http404


class QuanView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_detect_platform_template("quan/quan_home.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(QuanView,self).get(request,*args,**kwargs)


class QuanCategoryView(TemplateView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.template_name, self.category = get_detect_platform_template("quan/questions.html", request.user, request.META['HTTP_USER_AGENT']), QuestionsCategory.objects.get(name_en=self.kwargs["cat_name"])
		return super(QuanCategoryView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(QuanCategoryView,self).get_context_data(**kwargs)
		context["category"] = self.category
		context["quest_categories"] = QuestionsCategory.objects.only("pk")
		return context

	def get_queryset(self):
		questions = Question.objects.filter(category=self.category)
		return questions


class WhoContactView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_detect_platform_template("quan/who_to_contact.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(WhoContactView,self).get(request,*args,**kwargs)

class HowApplyView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_detect_platform_template("quan/how_to_apply.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(HowApplyView,self).get(request,*args,**kwargs)

class WhereApplyView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_detect_platform_template("quan/where_to_apply.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(WhereApplyView,self).get(request,*args,**kwargs)

class WhyPublishView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_detect_platform_template("quan/why_publish.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(WhyPublishView,self).get(request,*args,**kwargs)

class HowPublishView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_detect_platform_template("quan/how_to_publish.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(HowPublishView,self).get(request,*args,**kwargs)


class CreateSupport(TemplateView):
    template_name = "quan/create_support.html"

    def get_context_data(self,**kwargs):
        from quan.forms import SupportForm

        context=super(CreateSupport,self).get_context_data(**kwargs)
        context["form"] = SupportForm()
        return context

    def post(self,request,*args,**kwargs):
        from quan.forms import SupportForm

        self.form_post = SupportForm(request.POST, request.FILES)

        if request.is_ajax() and self.form_post.is_valid() and request.user.is_authenticated:
            support = self.form_post.save(commit=False)
            support.creator = request.user
            support.save()
            files = request.FILES.getlist('files')
            if files:
                for file in files:
                    SupportFile.objects.create(support=support, file=file)
            return HttpResponse()
        else:
            from django.http import HttpResponseBadRequest
            return HttpResponseBadRequest()


class SupportList(ListView, CategoryListMixin):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        if request.user.is_supermanager():
            self.template_name = get_detect_platform_template("quan/support_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(SupportList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return Support.objects.all()


class ReadSupportMessage(View):
    def get(self, request, *args, **kwargs):
        message  = Support.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_supermanager():
            message.is_read = True
            message.save(update_fields=["is_read"])
            return HttpResponse()
        else:
            raise Http404
