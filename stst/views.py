from django.views.generic.base import TemplateView
from common.utils import get_full_template


class StatView(TemplateView):
    template_name = "stat/index.html"
