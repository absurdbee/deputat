from django.views.generic.base import TemplateView
from users.models import User
from common.templates import get_small_template
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from video.models import Video, VideoList
from generic.mixins import CategoryListMixin


class AllVideoView(TemplateView):
    template_name="all_video.html"


class UserVideoDetail(TemplateView, CategoryListMixin):
	template_name = None

	def get(self,request,*args,**kwargs):
		from common.templates import get_full_template

		self.video = Video.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_full_template("video/detail/user/", "u.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserVideoDetail,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(UserVideoDetail,self).get_context_data(**kwargs)
		context["object"] = self.video
		return context

class UserVideoDetail_2(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_template_user_window, get_template_anon_user_window

        self.video = Video.objects.get(pk=self.kwargs["pk"])
        self.list = VideoList.objects.get(uuid=self.kwargs["uuid"])
        if request.user.pk == self.video.creator.pk:
            self.videos = self.list.get_staff_items()
        else:
            self.videos = self.list.get_items()
        self.next = self.videos.filter(pk__gt=self.video.pk).order_by('pk').first()
        self.prev = self.videos.filter(pk__lt=self.video.pk).order_by('-pk').first()
        if request.user.is_authenticated:
            self.template_name = get_template_user_window(self.list, "user_video/detail/", "a.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_video_manager())
        else:
            self.template_name = get_template_anon_user_window(self.list, "user_video/detail/", "a.html", request.META['HTTP_USER_AGENT'])
        return super(UserVideoDetail_2,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(UserVideoDetail_2,self).get_context_data(**kwargs)
        c['object'], c['list'], c['next'], c['prev'] = self.video, self.list, self.next, self.prev
        return c


class UserLoadVideoList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        from common.templates import get_template_user_window, get_template_anon_user_window

        self.list = VideoList.objects.get(pk=self.kwargs["pk"])
        if self.list.creator == request.user.pk:
            self.video_list = self.list.get_staff_items()
        else:
            self.video_list = self.list.get_items()
        if request.user.is_authenticated:
            self.template_name = get_template_user_window(self.list, "user_video/load/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_video_manager())
        else:
            self.template_name = get_template_anon_user_window(self.list, "user_video/load/", "list.html", request.META['HTTP_USER_AGENT'])
        return super(UserLoadVideoList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(UserLoadVideoList,self).get_context_data(**kwargs)
        c['user'], c['list'] = self.list.creator, self.list
        return c

    def get_queryset(self):
        return self.video_list


class UserVideo(ListView, CategoryListMixin):
    template_name, paginate_by, can_add_list = None, 15, None

    def get(self,request,*args,**kwargs):
        from common.templates import get_template_user_item, get_template_anon_user_item
        from django.conf import settings

        pk = int(self.kwargs["pk"])
        self.user = User.objects.get(pk=pk)
        self.list = self.user.get_video_list()
        self.count_lists = self.list.get_user_lists_count(pk)
        if pk == request.user.pk:
            self.video_list = self.list.get_staff_items()
            self.get_lists = self.list.get_user_staff_lists(pk)
            if self.count_lists < settings.USER_MAX_VIDEO_LISTS:
                self.can_add_list = True
        else:
            self.video_list = self.list.get_items()
            self.get_lists = self.list.get_user_lists(pk)
        if request.user.is_authenticated:
            self.template_name = get_template_user_item(self.list, "user_video/main/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_video_manager())
        else:
            self.template_name = get_template_anon_user_item(self.list, "user_video/main/", "list.html", request.META['HTTP_USER_AGENT'])
        return super(UserVideo,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(UserVideo,self).get_context_data(**kwargs)
        c['user'], c['list'], c['get_lists'], c['count_lists'], c['can_add_list'] = self.user, self.list, self.get_lists, self.count_lists, self.can_add_list
        return c

    def get_queryset(self):
        return self.video_list


class UserVideoList(ListView, CategoryListMixin):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        from common.templates import get_template_user_item, get_template_anon_user_item

        self.list = VideoList.objects.get(uuid=self.kwargs["uuid"])
        if self.list.creator.pk == request.user.pk:
            self.video_list = self.list.get_staff_items()
        else:
            self.video_list = self.list.get_items()
        if request.user.is_authenticated:
            self.template_name = get_template_user_item(self.list, "user_video/list/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_video_manager())
        else:
            self.template_name = get_template_anon_user_item(self.list, "user_video/list/", "list.html", request.META['HTTP_USER_AGENT'])
        return super(UserVideoList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserVideoList,self).get_context_data(**kwargs)
        context['list'] = self.list
        return context

    def get_queryset(self):
        return self.video_list


class UserLoadPenaltyVideoList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from common.templates import get_managers_template

		self.list = VideoList.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_managers_template("user_video/load/penalty_list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadPenaltyVideoList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadPenaltyVideoList,self).get_context_data(**kwargs)
		context['list'] = self.list
		return context

	def get_queryset(self):
		return self.list.get_penalty_items()

class UserLoadModeratedVideoList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from common.templates import get_managers_template

		self.list = VideoList.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_managers_template("user_video/load/moderated_list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadModeratedVideoList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadModeratedVideoList,self).get_context_data(**kwargs)
		context['list'] = self.list
		return context

	def get_queryset(self):
		return self.list.get_items()


class ManagerVideoDetail(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_full_template
        from lists.models import MediaList

        self.video = Video.objects.get(pk=self.kwargs["pk"])
        self.list = MediaList.objects.get(uuid=self.kwargs["uuid"])
        self.videos = self.list.get_items()
        self.template_name = get_full_template("user_video/media_detail/", "a.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(ManagerVideoDetail,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from lists.models import MediaList
        
        c = super(ManagerVideoDetail,self).get_context_data(**kwargs)
        c['object'], c['list'], c['get_lists'] = self.video, self.list, MediaList.objects.filter(owner__isnull=True, type="LIS")
        return c
