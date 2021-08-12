from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from organizations.models import Organization
from django.views.generic import ListView
from common.templates import get_full_template
from django.http import Http404


class AllOrganizationsList(ListView, CategoryListMixin):
	template_name, paginate_by = None, 12

	def get(self,request,*args,**kwargs):
		self.template_name = get_full_template("organizations/", "all.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(CityListView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		return Organization.objects.only("pk")


class SuggestOrganizationView(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		from common.templates import get_detect_platform_template
		if request.user.is_identified():
			self.template_name = get_detect_platform_template("organizations/suggest_organization.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			raise Http404
		return super(SuggestOrganizationView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		from organizations.forms import OrganizationForm

		c = super(SuggestOrganizationView,self).get_context_data(**kwargs)
		c["form"] = OrganizationForm()
		return c

	def post(self,request,*args,**kwargs):
		from common.templates import render_for_platform
		from organizations.forms import OrganizationForm

		self.form = CommunityForm(request.POST)
		if self.form.is_valid() and request.is_ajax() and request.user.is_identified():
			_organization = self.form.save(commit=False)
			organization = _community.suggest_organization(
															name=_organization.name,
															image=_organization.image,
															creator=request.user,
															city=_organization.city,
															description=_organization.description,
															email_1=_organization.email_1,
															email_2=_organization.email_2,
															phone_1=_organization.phone_1,
															phone_2=_organization.phone_2,
															address_1=_organization.address_1,
															address_2=_organization.address_2,
															type=_organization.type,
															)
			return render_for_platform(request, 'organizations/detail/suggest_community.html',{'organization': organization})
		else:
			from django.http import HttpResponseBadRequest
			return HttpResponseBadRequest()
