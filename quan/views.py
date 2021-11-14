from django.views.generic.base import TemplateView
from django.views.generic import ListView
from quan.models import Question, QuestionsCategory
from common.templates import get_detect_platform_template


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
        from django.http import HttpResponse

        self.form_post = SupportForm(request.POST, request.FILES)

        if request.is_ajax() and self.form_post.is_valid() and request.user.is_authenticated:
            support = self.form_post.save(commit=False)
            support.creator = request.user
            support.save()
            images = request.FILES.getlist('files')
            if images:
                from quan.models import SupportFile
                for image in images:
                    SupportFile.objects.create(support=support, image=image)
            return HttpResponse()
        else:
            from django.http import HttpResponseBadRequest
            return HttpResponseBadRequest()
