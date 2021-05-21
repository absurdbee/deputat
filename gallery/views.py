from django.views.generic.base import TemplateView
from django.views.generic import ListView
from gallery.models import PhotoList, Photo


class UserLoadPhotoList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from common.templates import get_template_user_window, get_template_anon_user_window

		self.list = PhotoList.objects.get(pk=self.kwargs["pk"])
		if self.list.creator.pk == request.user.pk:
			self.photo_list = self.list.get_staff_photos()
		else:
			self.photo_list = self.list.get_photos()
		if request.user.is_authenticated:
			self.template_name = get_template_user_item(self.list, "user_gallery/load/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_photo_manager())
		else:
			self.template_name = get_template_anon_user_item(self.list, "user_gallery/load/anon_list.html", request.META['HTTP_USER_AGENT'])
		return super(UserLoadPhotoList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(UserLoadPhotoList,self).get_context_data(**kwargs)
		c['user'], c['list'] = self.list.creator, self.list
		return c

	def get_queryset(self):
		list = self.photo_list
		return list


class UserGallery(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from common.templates import get_template_user_item, get_template_anon_user_item
		from users.models import User

		pk = self.kwargs["pk"]
		self.user = User.objects.get(pk=pk)
		self.list = self.user.get_photo_list()
		self.count_lists = self.list.get_user_lists_count(pk)
		if pk == request.user.pk:
			self.photo_list = self.list.get_staff_photos()
			self.get_lists = self.list.get_user_staff_lists(pk) 
		else:
			self.photo_list = self.list.get_photos()
			self.get_lists = self.list.get_user_lists(pk)
		if request.user.is_authenticated:
			self.template_name = get_template_user_item(self.list, "user_gallery/gallery/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_photo_manager())
		else:
			self.template_name = get_template_anon_user_item(self.list, "user_gallery/gallery/anon_list.html", request.META['HTTP_USER_AGENT'])
		return super(UserGallery,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserGallery,self).get_context_data(**kwargs)
		context['user'] = self.user
		context['list'] = self.list
		context['get_lists'] = self.get_lists
		context['count_lists'] = self.count_lists
		return context

	def get_queryset(self):
		return self.photo_list

class UserPhotoList(ListView):
	template_name, paginate_by = None, 12

	def get(self,request,*args,**kwargs):
		from common.templates import get_template_user_item, get_template_anon_user_item

		self.list = PhotoList.objects.get(uuid=self.kwargs["uuid"])
		if self.list.creator.pk == request.user.pk:
			self.photo_list = self.list.get_staff_photos()
		else:
			self.photo_list = self.list.get_photos()
		if request.user.is_authenticated:
			self.template_name = get_template_user_item(self.list, "user_gallery/list/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_photo_manager())
		else:
			self.template_name = get_template_anon_user_item(self.list, "user_gallery/list/anon_list.html", request.META['HTTP_USER_AGENT'])
		return super(UserPhotoList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserPhotoList,self).get_context_data(**kwargs)
		context['user'] = self.list.creator
		context['list'] = self.list
		return context

	def get_queryset(self):
		return self.photo_list


class UserListPhoto(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		from common.templates import get_item_template
		from django.db.models import Q

		self.photo, self.list = Photo.objects.get(pk=self.kwargs["pk"]), PhotoList.objects.get(uuid=self.kwargs["uuid"])
		if request.is_ajax():
			self.template_name = get_item_template(self.photo, "user_gallery/photo/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			from django.http import Http404
			raise Http404
		if request.user.pk == self.photo.creator.pk:
			query = Q(status="PUB") | Q(status="PRI")
			self.photos = self.list.get_photos()
		else:
			query = Q(status="PUB")
			self.photos = self.list.get_staff_photos()
		self.next = self.photos.filter(query, pk__gt=self.photo.pk).order_by('pk').first()
		self.prev = self.photos.filter(query, pk__lt=self.photo.pk).order_by('pk').first()
		return super(UserListPhoto,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserListPhoto,self).get_context_data(**kwargs)
		context["object"] = self.photo
		context["list"] = self.list
		context["next"] = self.next
		context["prev"] = self.prev
		return context


class UserElectNewPhoto(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		from blog.models import ElectNew
		from common.templates import get_item_template

		self.photo = Photo.objects.get(pk=self.kwargs["photo_pk"])
		self.elect_new = ElectNew.objects.get(pk=self.kwargs["pk"])
		self.photos = self.elect_new.get_attach_photos()
		if request.is_ajax():
			self.template_name = get_item_template(self.photo, "user_gallery/photo/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			from django.http import Http404
			raise Http404
		return super(UserElectNewPhoto,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserElectNewPhoto,self).get_context_data(**kwargs)
		context["object"] = self.photo
		context["elect_new"] = self.elect_new
		context["user"] = self.request.user
		context["next"] = self.photos.filter(pk__gt=self.photo.pk, status="PUB").order_by('pk').first()
		context["prev"] = self.photos.filter(pk__lt=self.photo.pk, status="PUB").order_by('-pk').first()
		return context

class UserBlogCommentPhoto(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		from common.model.comments import BlogComment
		from common.templates import get_item_template

		self.photo = Photo.objects.get(pk=self.kwargs["photo_pk"])
		self.comment = BlogComment.objects.get(pk=self.kwargs["pk"])
		self.photos = self.comment.get_attach_photos()
		if request.is_ajax():
			self.template_name = get_item_template(self.photo, "user_gallery/blog_comment_photo/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			from django.http import Http404
			raise Http404
		return super(UserBlogCommentPhoto,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserBlogCommentPhoto,self).get_context_data(**kwargs)
		context["object"] = self.photo
		context["user"] = self.request.user
		context["next"] = self.photos.filter(pk__gt=self.photo.pk, status="PUB").order_by('pk').first()
		context["prev"] = self.photos.filter(pk__lt=self.photo.pk, status="PUB").order_by('-pk').first()
		context["comment"] = self.comment
		return context

class UserElectNewCommentPhoto(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		from common.model.comments import ElectNewComment
		from common.templates import get_item_template

		self.photo = Photo.objects.get(pk=self.kwargs["photo_pk"])
		self.comment = ElectNewComment.objects.get(pk=self.kwargs["pk"])
		self.photos = self.comment.get_attach_photos()
		if request.is_ajax():
			self.template_name = get_item_template(self.photo, "user_gallery/elect_new_comment_photo/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			from django.http import Http404
			raise Http404
		return super(UserElectNewCommentPhoto,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserElectNewCommentPhoto,self).get_context_data(**kwargs)
		context["object"] = self.photo
		context["user"] = self.request.user
		context["next"] = self.photos.filter(pk__gt=self.photo.pk, status="PUB").order_by('pk').first()
		context["prev"] = self.photos.filter(pk__lt=self.photo.pk, status="PUB").order_by('-pk').first()
		context["comment"] = self.comment
		return context


class GetUserPhoto(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		from common.templates import get_small_template
		self.photo = Photo.objects.get(pk=self.kwargs["pk"])
		if request.is_ajax():
			self.template_name = get_small_template("user_gallery/get_photo.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			from django.http import Http404
			raise Http404
		return super(GetUserPhoto,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(GetUserPhoto,self).get_context_data(**kwargs)
		context["object"] = self.photo
		return context
