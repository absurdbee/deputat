from django.views.generic.base import TemplateView
from users.models import User
from common.utils import get_small_template, get_list_template
from django.views.generic import ListView
from django.views.generic.base import TemplateView


class AllVideoView(TemplateView):
    template_name="all_video.html"


class UserLoadVideoAlbum(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.album = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
		self.template_name = get_small_template("user_video/list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadVideoAlbum,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(UserLoadVideoAlbum,self).get_context_data(**kwargs)
		c['user'], c['album'] = self.album.creator, self.album
		return c

	def get_queryset(self):
		return self.album.get_videos()


class UserVideoListCreate(TemplateView):
    form_post = None
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_small_template("user_video/create_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserVideoListCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserVideoListCreate,self).get_context_data(**kwargs)
        context["form_post"] = AlbumForm()
        return context

    def post(self,request,*args,**kwargs):
        self.form_post = AlbumForm(request.POST)
        self.user = User.objects.get(pk=self.kwargs["pk"])

        if request.is_ajax() and self.form_post.is_valid() and request.user == self.user:
            new_album = self.form_post.save(commit=False)
            new_album.creator = request.user
            new_album.save()
            return render_for_platform(request, 'user_video/list.html',{'album': new_album, 'user': request.user})
        else:
            return HttpResponseBadRequest()


class UserVideoAttachCreate(TemplateView):
    form_post = None
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_small_template("user_video/create_video_attach.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserVideoAttachCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserVideoAttachCreate,self).get_context_data(**kwargs)
        context["form_post"] = VideoForm()
        return context

    def post(self,request,*args,**kwargs):
        self.form_post = VideoForm(request.POST, request.FILES)
        self.user = User.objects.get(pk=self.kwargs["pk"])

        if request.is_ajax() and form_post.is_valid() and request.user == self.user:
            self.my_list = VideoAlbum.objects.get(creator_id=self.user.pk, type=VideoAlbum.MAIN)
            new_video = self.form_post.save(commit=False)
            new_video.creator = request.user
            new_video.save()
            my_list.video_album.add(new_video)
            return render_for_platform(request, 'user_video/video.html',{'object': new_video})
        else:
            return HttpResponseBadRequest()


class UserVideoCreate(TemplateView):
    form_post = None
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_small_template("user_video/create_video.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserVideoCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserVideoCreate,self).get_context_data(**kwargs)
        context["form_post"] = VideoForm()
        return context

    def post(self,request,*args,**kwargs):
        self.form_post = VideoForm(request.POST, request.FILES)
        self.user = User.objects.get(pk=self.kwargs["pk"])

        if request.is_ajax() and self.form_post.is_valid() and request.user == self.user:
            new_video = self.form_post.save(commit=False)
            new_video.creator = request.user
            albums = request.POST.getlist("album")
            new_video.save()
            for _album_pk in albums:
                _album = VideoAlbum.objects.get(pk=_album_pk)
                _album.video_album.add(new_video)
            return render_for_platform(request, 'user_video/video.html',{'object': new_video})
        else:
            return HttpResponse()


class UserVideoAlbumPreview(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.album = VideoAlbum.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_small_template("user_video/album_preview.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserVideoAlbumPreview,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserVideoAlbumPreview,self).get_context_data(**kwargs)
		context["album"] = self.album
		return context


class UserVideolistEdit(TemplateView):
    template_name = None
    form=None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_small_template("user_video/edit_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserVideolistEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserVideolistEdit,self).get_context_data(**kwargs)
        context["user"] = self.user
        context["album"] = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
        return context

    def post(self,request,*args,**kwargs):
        self.list = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
        self.form = AlbumForm(request.POST,instance=self.list)
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and self.form.is_valid() and self.user == request.user:
            list = self.form.save(commit=False)
            self.form.save()
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
        return super(UserVideolistEdit,self).get(request,*args,**kwargs)


class UserVideo(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.list = self.user.get_or_create_video_list()
		if self.user.pk == request.user.pk:
			self.video_list = self.list.get_my_videos()
		else:
			self.video_list = self.list.get_videos()
		self.template_name = get_list_template(self.list, "user_video/", "video.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserVideo,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserVideo,self).get_context_data(**kwargs)
		context['user'] = self.user
		context['list'] = self.list
		return context

	def get_queryset(self):
		return self.video_list


class UserVideoList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from video.models import VideoAlbum

		self.list = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
		self.user = User.objects.get(pk=self.kwargs["pk"])
		if self.user.pk == request.user.pk:
			self.video_list = self.list.get_my_videos()
		else:
			self.video_list = self.list.get_videos()
		self.template_name = get_list_template(self.list, "user_video/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserVideoList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserVideoList,self).get_context_data(**kwargs)
		context['user'] = self.user
		context['list'] = self.list
		return context

	def get_queryset(self):
		return self.video_list
