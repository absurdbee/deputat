from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin


class SearchView(TemplateView, CategoryListMixin):
    template_name = "search.html"
