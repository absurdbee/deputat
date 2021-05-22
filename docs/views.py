from django.views.generic import ListView
from docs.models import Doc, DocList
from common.templates import get_small_template
from users.models import User


class DocsView(ListView):
	template_name = "docs.html"

	def get_queryset(self):
		return Doc.objects.only("pk")


class UserDocs(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from common.templates import get_template_user_item, get_template_anon_user_item

		pk = int(self.kwargs["pk"])
		self.user = User.objects.get(pk=pk)
		self.list = self.user.get_doc_list()
		self.count_lists = self.list.get_user_lists_count(pk)
		if pk == request.user.pk:
			self.doc_list = self.list.get_my_docs()
			self.get_lists = self.list.get_user_staff_lists(pk)
		else:
			self.doc_list = self.list.get_docs()
			self.get_lists = self.list.get_user_lists(pk)
		if request.user.is_authenticated:
			self.template_name = get_template_user_item(self.list, "user_docs/main/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_doc_manager())
		else:
			self.template_name = get_template_anon_user_item(self.list, "user_docs/main/anon_list.html", request.META['HTTP_USER_AGENT'])
		return super(UserDocs,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserDocs,self).get_context_data(**kwargs)
		context['user'] = self.user
		context['list'] = self.list
		context['get_lists'] = self.get_lists
		context['count_lists'] = self.count_lists
		return context

	def get_queryset(self):
		return self.doc_list


class UserDocsList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from docs.models import DocList
		from common.templates import get_template_user_item, get_template_anon_user_item

		self.list = DocList.objects.get(uuid=self.kwargs["uuid"])
		if self.list.creator.pk == request.user.pk:
			self.doc_list = self.list.get_my_docs()
		else:
			self.doc_list = self.list.get_docs()
		if request.user.is_authenticated:
			self.template_name = get_template_user_item(self.list, "user_docs/list/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_doc_manager())
		else:
			self.template_name = get_template_anon_user_item(self.list, "user_docs/list/anon_list.html", request.META['HTTP_USER_AGENT'])
		return super(UserDocsList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserDocsList,self).get_context_data(**kwargs)
		context['user'] = self.list.creator
		context['list'] = self.list
		return context

	def get_queryset(self):
		return self.doc_list


class UserLoadDoclist(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from common.templates import get_template_user_window, get_template_anon_user_window

		self.list = DocList.objects.get(pk=self.kwargs["pk"])
		if self.list.creator.pk == request.user.pk:
			self.doc_list = self.list.get_my_docs()
		else:
			self.doc_list = self.list.get_docs()
		if request.user.is_authenticated:
			self.template_name = get_template_user_window(self.list, "user_docs/load/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_doc_manager())
		else:
			self.template_name = get_template_anon_user_window(self.list, "user_docs/load/anon_list.html", request.META['HTTP_USER_AGENT'])
		return super(UserLoadDoclist,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadDoclist,self).get_context_data(**kwargs)
		context['list'] = self.list
		return context

	def get_queryset(self):
		return self.doc_list
