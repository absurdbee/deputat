from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from common.utils import get_small_template


class ContactsView(TemplateView, CategoryListMixin):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_small_template("contacts/contacts.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(ContactsView,self).get(request,*args,**kwargs)
