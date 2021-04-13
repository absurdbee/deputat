from django.views.generic import ListView
from docs.models import Doc, DocList
from common.templates import get_small_template, get_list_template
from users.models import User


class DocsView(ListView):
	template_name = "docs.html"

	def get_queryset(self):
		return Doc.objects.only("pk")


class UserDocs(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.list = self.user.get_or_create_main_doclist()
		if self.user.pk == request.user.pk:
			self.doc_list = self.list.get_my_docs()
		else:
			self.doc_list = self.list.get_docs()
		self.template_name = get_list_template(self.list, "user_docs/main/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserDocs,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserDocs,self).get_context_data(**kwargs)
		context['user'] = self.user
		context['list'] = self.list
		return context

	def get_queryset(self):
		return self.doc_list


class UserDocsList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from docs.models import DocList

		self.list = DocList.objects.get(uuid=self.kwargs["uuid"])
		self.user = User.objects.get(pk=self.kwargs["pk"])
		if self.user.pk == request.user.pk:
			self.doc_list = self.list.get_my_docs()
		else:
			self.doc_list = self.list.get_docs()
		self.template_name = get_list_template(self.list, "user_docs/list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserDocsList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserDocsList,self).get_context_data(**kwargs)
		context['user'] = self.user
		context['list'] = self.list
		return context

	def get_queryset(self):
		return self.doc_list


class UserLoadDoclist(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.list = DocList.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_list_template(self.list, "user_docs/load/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadDoclist,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadDoclist,self).get_context_data(**kwargs)
		context['user'] = self.user
		context['list'] = self.list
		return context

	def get_queryset(self):
		list = self.list.get_docs()
		return list
