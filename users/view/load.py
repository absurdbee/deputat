from django.views.generic import ListView
from common.utils import get_my_template


class UserLoadPhoto(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from gallery.models import Album

		self.album, self.template_name = Album.objects.get(creator_id=request.user.pk, type=Album.WALL), get_my_template("user_load/u_photo_load.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadPhoto,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadPhoto,self).get_context_data(**kwargs)
		context["album"] = self.album
		return context

	def get_queryset(self):
		return self.album.get_photos()


class UserLoadPhotoAlbum(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from gallery.models import Album

		self.album, self.template_name = Album.objects.get(uuid=self.kwargs["uuid"]), get_my_template("user_load/u_photo_list_load.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadPhotoAlbum,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadPhotoAlbum,self).get_context_data(**kwargs)
		context["album"] = self.album
		return context

	def get_queryset(self):
		return self.album.get_photos()

class UserLoadPhotoComment(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from gallery.models import Album
		self.album, self.template_name = Album.objects.get(creator_id=request.user.pk, type=Album.WALL), get_my_template("user_load/u_photo_comments_load.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadPhotoComment,self).get(request,*args,**kwargs)

	def get_queryset(self):
		return self.album.get_photos()

class UserLoadPhotoAlbumComment(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from gallery.models import Album

		self.album, self.template_name = Album.objects.get(uuid=self.kwargs["uuid"]), get_my_template("user_load/u_photo_list_comments_load.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadPhotoAlbumComment,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadPhotoAlbumComment,self).get_context_data(**kwargs)
		context["album"] = self.album
		return context

	def get_queryset(self):
		return self.album.get_photos()


class UserLoadVideo(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from video.models import VideoAlbum

		self.album, self.template_name = VideoAlbum.objects.get(creator_id=request.user.pk, type=VideoAlbum.MAIN), get_my_template("user_load/u_video_load.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadVideo,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadVideo,self).get_context_data(**kwargs)
		context["album"] = self.album
		return context

	def get_queryset(self):
		return self.album.get_queryset()

class UserLoadVideoAlbum(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from video.models import VideoAlbum

		self.album, self.template_name = VideoAlbum.objects.get(uuid=self.kwargs["uuid"]), get_my_template("user_load/u_video_list_load.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadVideoAlbum,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadVideoAlbum,self).get_context_data(**kwargs)
		context["album"] = self.album
		return context

	def get_queryset(self):
		return self.album.get_queryset().order_by('-created')


class UserLoadMusic(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from music.models import SoundList
		self.playlist = SoundList.objects.get(creator_id=request.user.pk, type=SoundList.MAIN)
		self.template_name = get_my_template("user_load/u_music_load.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadMusic,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadMusic,self).get_context_data(**kwargs)
		context["playlist"] = self.playlist
		return context

	def get_queryset(self):
		return self.playlist.playlist_too().order_by('-created_at')

class UserLoadMusicList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from music.models import SoundList
		self.playlist = SoundList.objects.get(uuid=self.kwargs["uuid"])
		self.template_name = get_settings_template("user_load/u_music_list_load.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadMusicList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadMusicList,self).get_context_data(**kwargs)
		context["playlist"] = self.playlist
		return context

	def get_queryset(self):
		return self.playlist.playlist_too().order_by('-created_at')


class UserLoadDoc(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from docs.models import DocList
		self.list = DocList.objects.get(creator_id=request.user.pk, type=DocList.MAIN)
		self.template_name = get_settings_template("user_load/u_doc_load.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadDoc,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadDoc,self).get_context_data(**kwargs)
		context["list"] = self.list
		return context

	def get_queryset(self):
		return self.list.get_docs().order_by('-created')

class UserLoadDocList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from docs.models import DocList
		self.list = DocList.objects.get(uuid=self.kwargs["uuid"])
		self.template_name = get_settings_template("user_load/u_doc_list_load.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadDocList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadDocList,self).get_context_data(**kwargs)
		context["list"] = self.list
		return context

	def get_queryset(self):
		return self.list.get_docs().order_by('-created')
