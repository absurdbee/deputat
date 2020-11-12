from django.views.generic.base import TemplateView


class StatView(TemplateView):
    template_name = "stat/index.html"
