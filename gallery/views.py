from django.views.generic.base import TemplateView
from django.views.generic import ListView
from gallery.models import PhotoList, Photo
from generic.mixins import CategoryListMixin


class UserLoadPhotoList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from common.templates import get_template_user_window, get_template_anon_user_window

		self.list = PhotoList.objects.get(pk=self.kwargs["pk"])
		if self.list.creator.pk == request.user.pk:
			self.photo_list = self.list.get_staff_items()
		else:
			self.photo_list = self.list.get_items()
		if request.user.is_authenticated:
			self.template_name = get_template_user_window(self.list, "user_gallery/load/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_photo_manager())
		else:
			self.template_name = get_template_anon_user_window(self.list, "user_gallery/load/", "list.html", request.META['HTTP_USER_AGENT'])
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

		pk = int(self.kwargs["pk"])
		self.user = User.objects.get(pk=pk)
		self.list = self.user.get_photo_list()
		self.count_lists = self.list.get_user_lists_count(pk)
		if pk == request.user.pk:
			self.photo_list = self.list.get_staff_items()
			self.get_lists = self.list.get_user_staff_lists(pk)
		else:
			self.photo_list = self.list.get_items()
			self.get_lists = self.list.get_user_lists(pk)
		if request.user.is_authenticated:
			self.template_name = get_template_user_item(self.list, "user_gallery/gallery/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_photo_manager())
		else:
			self.template_name = get_template_anon_user_item(self.list, "user_gallery/gallery/", "list.html", request.META['HTTP_USER_AGENT'])
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
			self.photo_list = self.list.get_staff_items()
		else:
			self.photo_list = self.list.get_items()
		if request.user.is_authenticated:
			self.template_name = get_template_user_item(self.list, "user_gallery/list/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_photo_manager())
		else:
			self.template_name = get_template_anon_user_item(self.list, "user_gallery/list/", "list.html", request.META['HTTP_USER_AGENT'])
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
		from common.templates import get_template_user_window, get_template_anon_user_window

		self.photo, self.list = Photo.objects.get(pk=self.kwargs["pk"]), PhotoList.objects.get(uuid=self.kwargs["uuid"])
		if request.user.is_authenticated:
			self.template_name = get_template_user_window(self.photo, "user_gallery/photo/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_photo_manager())
		else:
			self.template_name = get_template_anon_user_window(self.photo, "user_gallery/photo/", "list.html", request.META['HTTP_USER_AGENT'])
		if request.user.pk == self.photo.creator.pk:
			self.photos = self.list.get_staff_items()
		else:
			self.photos = self.list.get_items()
		self.next = self.photos.filter(pk__gt=self.photo.pk).order_by('pk').first()
		self.prev = self.photos.filter(pk__lt=self.photo.pk).order_by('pk').first()
		return super(UserListPhoto,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserListPhoto,self).get_context_data(**kwargs)
		context["object"] = self.photo
		context["list"] = self.list
		context["next"] = self.next
		context["prev"] = self.prev
		return context

class UserPhotoDetail(TemplateView, CategoryListMixin):
	template_name = None

	def get(self,request,*args,**kwargs):
		from common.templates import get_full_template

		self.photo = Photo.objects.get(uuid=self.kwargs["uuid"])
		self.template_name = get_full_template("user_gallery/detail_photo/", "photo.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserPhotoDetail,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(UserPhotoDetail,self).get_context_data(**kwargs)
		context["object"] = self.photo
		return context

class UserElectNewPhoto(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		from blog.models import ElectNew
		from common.templates import get_template_user_window, get_template_anon_user_window

		self.photo = Photo.objects.get(pk=self.kwargs["photo_pk"])
		self.elect_new = ElectNew.objects.get(pk=self.kwargs["pk"])
		self.photos = self.elect_new.get_attach_photos()
		if request.user.is_authenticated:
			self.template_name = get_template_user_window(self.photo, "user_gallery/elect_new_photo/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_photo_manager())
		else:
			self.template_name = get_template_anon_user_window(self.photo, "user_gallery/elect_new_photo/", "list.html", request.META['HTTP_USER_AGENT'])
		return super(UserElectNewPhoto,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserElectNewPhoto,self).get_context_data(**kwargs)
		context["object"] = self.photo
		context["elect_new"] = self.elect_new
		context["user"] = self.request.user
		context["next"] = self.photos.filter(pk__gt=self.photo.pk, type="PUB").order_by('pk').first()
		context["prev"] = self.photos.filter(pk__lt=self.photo.pk, type="PUB").order_by('-pk').first()
		return context

class UserBlogPhoto(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		from blog.models import Blog
		from common.templates import get_template_user_window, get_template_anon_user_window

		self.photo = Photo.objects.get(pk=self.kwargs["photo_pk"])
		self.blog = Blog.objects.get(pk=self.kwargs["pk"])
		self.photos = self.blog.get_attach_photos()
		if request.user.is_authenticated:
			self.template_name = get_template_user_window(self.photo, "user_gallery/blog_photo/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_photo_manager())
		else:
			self.template_name = get_template_anon_user_window(self.photo, "user_gallery/blog_photo/", "list.html", request.META['HTTP_USER_AGENT'])
		return super(UserBlogPhoto,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserBlogPhoto,self).get_context_data(**kwargs)
		context["object"] = self.photo
		context["blog"] = self.blog
		context["user"] = self.request.user
		context["next"] = self.photos.filter(pk__gt=self.photo.pk, type="PUB").order_by('pk').first()
		context["prev"] = self.photos.filter(pk__lt=self.photo.pk, type="PUB").order_by('-pk').first()
		return context

class UserBlogCommentPhoto(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		from common.model.comments import BlogComment
		from common.templates import get_template_user_window, get_template_anon_user_window

		self.photo = Photo.objects.get(pk=self.kwargs["photo_pk"])
		self.comment = BlogComment.objects.get(pk=self.kwargs["pk"])
		self.photos = self.comment.get_attach_photos()
		if request.user.is_authenticated:
			self.template_name = get_template_user_window(self.photo, "user_gallery/blog_comment_photo/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_photo_manager())
		else:
			self.template_name = get_template_anon_user_window(self.photo, "user_gallery/blog_comment_photo/", "list.html", request.META['HTTP_USER_AGENT'])
		return super(UserBlogCommentPhoto,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserBlogCommentPhoto,self).get_context_data(**kwargs)
		context["object"] = self.photo
		context["user"] = self.request.user
		context["next"] = self.photos.filter(pk__gt=self.photo.pk, type="PUB").order_by('pk').first()
		context["prev"] = self.photos.filter(pk__lt=self.photo.pk, type="PUB").order_by('-pk').first()
		context["comment"] = self.comment
		return context

class UserElectNewCommentPhoto(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		from common.model.comments import ElectNewComment
		from common.templates import get_template_user_window, get_template_anon_user_window

		self.photo = Photo.objects.get(pk=self.kwargs["photo_pk"])
		self.comment = ElectNewComment.objects.get(pk=self.kwargs["pk"])
		self.photos = self.comment.get_attach_photos()
		if request.user.is_authenticated:
			self.template_name = get_template_user_window(self.photo, "user_gallery/elect_new_comment_photo/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_photo_manager())
		else:
			self.template_name = get_template_anon_user_window(self.photo, "user_gallery/elect_new_comment_photo/", "list.html", request.META['HTTP_USER_AGENT'])
		return super(UserElectNewCommentPhoto,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserElectNewCommentPhoto,self).get_context_data(**kwargs)
		context["object"] = self.photo
		context["user"] = self.request.user
		context["next"] = self.photos.filter(pk__gt=self.photo.pk, type="PUB").order_by('pk').first()
		context["prev"] = self.photos.filter(pk__lt=self.photo.pk, type="PUB").order_by('-pk').first()
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


class GetUserPenaltyPhoto(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		from common.templates import get_small_template
		self.photo = Photo.objects.get(pk=self.kwargs["pk"])
		if request.is_ajax():
			self.template_name = get_small_template("user_gallery/penalty_photo.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			from django.http import Http404
			raise Http404
		return super(GetUserPenaltyPhoto,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(GetUserPenaltyPhoto,self).get_context_data(**kwargs)
		context["object"] = self.photo
		return context

class GetUserModeratedPhoto(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		from common.templates import get_small_template
		self.photo = Photo.objects.get(pk=self.kwargs["pk"])
		if request.is_ajax():
			self.template_name = get_small_template("user_gallery/get_moderated.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			from django.http import Http404
			raise Http404
		return super(GetUserModeratedPhoto,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(GetUserModeratedPhoto,self).get_context_data(**kwargs)
		context["object"] = self.photo
		return context


class UserLoadPenaltyPhotolist(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from common.templates import get_managers_template

		self.list = PhotoList.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_managers_template("user_gallery/load/penalty_list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadPenaltyPhotolist,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadPenaltyPhotolist,self).get_context_data(**kwargs)
		context['list'] = self.list
		return context

	def get_queryset(self):
		return self.list.get_penalty_items()

class UserLoadModeratedPhotolist(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from common.templates import get_managers_template

		self.list = PhotoList.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_managers_template("user_gallery/load/moderated_list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadModeratedPhotolist,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadModeratedPhotolist,self).get_context_data(**kwargs)
		context['list'] = self.list
		return context

	def get_queryset(self):
		return self.list.get_items()
