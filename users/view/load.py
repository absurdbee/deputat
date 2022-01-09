from django.views.generic import ListView
from common.templates import get_my_template
from django.http import HttpResponse
from django.views import View


class UserLoadPhoto(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.list, self.template_name = request.user.get_photo_list(), get_my_template("user_load/u_photo_load.html", request.user, request.META['HTTP_USER_AGENT'])
		self.get_lists = self.list.get_user_lists_not_empty(request.user.pk)
		return super(UserLoadPhoto,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadPhoto,self).get_context_data(**kwargs)
		context['get_lists'], context['list'] = self.get_lists, self.list
		return context

	def get_queryset(self):
		return self.list.get_items()


class UserLoadPhotoList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from gallery.models import PhotoList
		self.list, self.template_name = PhotoList.objects.get(uuid=self.kwargs["uuid"]), get_my_template("user_load/u_photo_list_load.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadPhotoList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadPhotoList,self).get_context_data(**kwargs)
		context["list"] = self.list
		return context

	def get_queryset(self):
		return self.list.get_items()

class UserLoadPhotoComment(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.list, self.template_name = request.user.get_photo_list(), get_my_template("user_load/u_photo_comments_load.html", request.user, request.META['HTTP_USER_AGENT'])
		self.get_lists = self.list.get_user_lists_not_empty(request.user.pk)
		return super(UserLoadPhotoComment,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadPhotoComment,self).get_context_data(**kwargs)
		context['get_lists'], context['list'] = self.get_lists, self.list
		return context

	def get_queryset(self):
		return self.list.get_items()


class UserLoadVideo(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.list, self.template_name = request.user.get_video_list(), get_my_template("user_load/u_video_load.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadVideo,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadVideo,self).get_context_data(**kwargs)
		context["list"] = self.list
		context["get_lists"] = self.list.get_user_lists_not_empty(self.request.user.pk)
		return context

	def get_queryset(self):
		return self.list.get_items()

class UserLoadVideoList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from video.models import VideoList

		self.list, self.template_name = VideoList.objects.get(uuid=self.kwargs["uuid"]), get_my_template("user_load/u_video_list_load.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadVideoList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadVideoList,self).get_context_data(**kwargs)
		context["list"] = self.list
		return context

	def get_queryset(self):
		return self.list.get_items()


class UserLoadMusic(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.list, self.template_name = request.user.get_playlist(), get_my_template("user_load/u_music_load.html", request.user, request.META['HTTP_USER_AGENT'])
		self.get_lists = self.list.get_user_lists_not_empty(request.user.pk)
		return super(UserLoadMusic,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadMusic,self).get_context_data(**kwargs)
		context['get_lists'], context['list'] = self.get_lists, self.list
		return context

	def get_queryset(self):
		return self.list.get_items()

class UserLoadMusicList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from music.models import SoundList
		self.list = SoundList.objects.get(uuid=self.kwargs["uuid"])
		self.template_name = get_my_template("user_load/u_music_list_load.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadMusicList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadMusicList,self).get_context_data(**kwargs)
		context["playlist"] = self.list
		return context

	def get_queryset(self):
		return self.list.get_items()


class UserLoadDoc(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.list, self.template_name = request.user.get_doc_list(), get_my_template("user_load/u_doc_load.html", request.user, request.META['HTTP_USER_AGENT'])
		self.get_lists = self.list.get_user_lists_not_empty(request.user.pk)
		return super(UserLoadDoc,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadDoc,self).get_context_data(**kwargs)
		context['get_lists'], context['list'] = self.get_lists, self.list
		return context

	def get_queryset(self):
		return self.list.get_items()

class UserLoadDocList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from docs.models import DocList
		self.list = DocList.objects.get(uuid=self.kwargs["uuid"])
		self.template_name = get_my_template("user_load/u_doc_list_load.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadDocList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadDocList,self).get_context_data(**kwargs)
		context["list"] = self.list
		return context

	def get_queryset(self):
		return self.list.get_items()


class ChangeTheme(View):
	def get(self,request,*args,**kwargs):
		if request.user.is_authenticated:
			from users.model.profile import UserProfile
			theme = request.GET.get('theme')
			profile = UserProfile.objects.get(user=request.user)
			profile.theme = theme
			profile.save(update_fields=["theme"])
		return HttpResponse()


class SmilesStickersLoad(ListView):
	template_name, populate_smiles, populate_stickers, type, is_have_populate_smiles, is_have_populate_stickers = None, None, None, None, None, None

	def get(self,request,*args,**kwargs):
		from common.model.other import StickerCategory, SmileCategory
		type = request.GET.get("type")

		if not type or type == "standart_smile":
			self.categories = SmileCategory.objects.filter(classic=True)
			self.is_have_populate_smiles = request.user.is_have_populate_smiles()
			if self.is_have_populate_smiles:
				self.populate_smiles = request.user.get_populate_smiles()

		elif type == "gif_smile":
			self.categories = SmileCategory.objects.filter(gif=True)
			self.is_have_populate_smiles = request.user.is_have_populate_smiles()
			if self.is_have_populate_smiles:
				self.populate_smiles = request.user.get_populate_smiles()

		else:
			if StickerCategory.objects.filter(pk=type).exists():
				self.categories = [StickerCategory.objects.get(pk=type)]
			else:
				self.categories = []
			self.is_have_populate_stickers = request.user.is_have_populate_stickers()
			if self.is_have_populate_stickers:
				self.populate_stickers = request.user.get_populate_stickers()

		self.template_name = get_my_template("user_load/smiles_stickers.html", request.user, request.META['HTTP_USER_AGENT'])

		return super(SmilesStickersLoad,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(SmilesStickersLoad,self).get_context_data(**kwargs)
		context["categories"] = self.categories
		context["populate_smiles"] = self.populate_smiles
		context["populate_stickers"] = self.populate_stickers
		context["is_have_populate_smiles"] = self.is_have_populate_smiles
		context["is_have_populate_stickers"] = self.is_have_populate_stickers
		return context

	def get_queryset(self):
		return []

class SmilesLoad(ListView):
	template_name, populate_smiles = None, None

	def get(self,request,*args,**kwargs):
		self.template_name = get_my_template("user_load/smiles.html", request.user, request.META['HTTP_USER_AGENT'])
		self.is_have_populate_smiles = request.user.is_have_populate_smiles()
		if self.is_have_populate_smiles:
			self.populate_smiles = request.user.get_populate_smiles()
		return super(SmilesLoad,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		from common.model.other import SmileCategory, StickerCategory
		context = super(SmilesLoad,self).get_context_data(**kwargs)
		context["smiles_category"] = SmileCategory.objects.only("pk")
		context["populate_smiles"] = self.populate_smiles
		context["is_have_populate_smiles"] = self.is_have_populate_smiles
		return context

	def get_queryset(self):
		return []

class ChatsLoad(ListView):
	template_name, paginate_by = None, 20

	def get(self,request,*args,**kwargs):
		self.template_name = get_my_template("user_load/chats.html", request.user, request.META['HTTP_USER_AGENT'])
		self.list = request.user.get_all_chats()
		return super(ChatsLoad,self).get(request,*args,**kwargs)

	def get_queryset(self):
		return self.list
