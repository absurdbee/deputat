from django.views.generic.base import TemplateView
from users.models import User
from common.templates import get_small_template, get_list_template
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


class UserVideo(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        pk = self.kwargs["pk"]
        self.user = User.objects.get(pk=pk)
        self.list = self.user.get_or_create_main_videolist()
        if self.user.pk == request.user.pk:
            self.video_list = self.list.get_my_videos()
            self.is_have_lists = self.list.is_have_my_lists(pk)
            self.get_lists = self.list.get_my_lists(pk)
        else:
            self.video_list = self.list.get_videos()
            self.is_have_lists = self.list.is_have_lists(pk)
            self.get_lists = self.list.get_lists(pk)
        self.count_lists = self.list.get_lists_count(pk)
        self.template_name = get_list_template(self.list, "user_video/", "video.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserVideo,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(UserVideo,self).get_context_data(**kwargs)
        c['user'], c['list'], c['is_have_lists'], c['get_lists'], c['count_lists'] = self.user, self.list, self.is_have_lists, self.get_lists, self.count_lists
        return c

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
