from django.views.generic.base import TemplateView
from users.models import User
from common.templates import get_small_template
from django.views.generic import ListView
from django.views.generic.base import TemplateView


class AllVideoView(TemplateView):
    template_name="all_video.html"


class UserLoadVideoList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        from common.templates import get_template_user_window, get_template_anon_user_window

        self.list = VideoList.objects.get(uuid=self.kwargs["uuid"])
        if self.user.pk == request.user.pk:
            self.video_list = self.list.get_my_videos()
        else:
            self.video_list = self.list.get_videos()
        if request.user.is_authenticated:
            self.template_name = get_template_user_item(self.list, "user_video/load/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_video_manager())
        else:
            self.template_name = get_template_anon_user_item(self.list, "user_video/load/anon_list.html", request.META['HTTP_USER_AGENT'])
        return super(UserLoadVideoList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(UserLoadVideoList,self).get_context_data(**kwargs)
        c['user'], c['list'] = self.list.creator, self.list
        return c

    def get_queryset(self):
        return self.video_list


class UserVideo(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        from common.templates import get_template_user_item, get_template_anon_user_item

        pk = self.kwargs["pk"]
        self.user = User.objects.get(pk=pk)
        self.list = self.user.get_video_list()
        if self.user.pk == request.user.pk:
            self.video_list = self.list.get_my_videos()
            self.is_have_lists = self.list.is_have_my_lists(pk)
            self.get_lists = self.list.get_my_lists(pk)
        else:
            self.video_list = self.list.get_videos()
            self.is_have_lists = self.list.is_have_lists(pk)
            self.get_lists = self.list.get_lists(pk)
        self.count_lists = self.list.get_lists_count(pk)
        if request.user.is_authenticated:
            self.template_name = get_template_user_item(self.list, "user_video/main/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_video_manager())
        else:
            self.template_name = get_template_anon_user_item(self.list, "user_video/main/anon_list.html", request.META['HTTP_USER_AGENT'])
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
        from video.models import VideoList
        from common.templates import get_template_user_item, get_template_anon_user_item

        self.list = VideoList.objects.get(uuid=self.kwargs["uuid"])
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.pk == request.user.pk:
            self.video_list = self.list.get_my_videos()
        else:
            self.video_list = self.list.get_videos()
        if request.user.is_authenticated:
            self.template_name = get_template_user_item(self.list, "user_video/list/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_video_manager())
        else:
            self.template_name = get_template_anon_user_item(self.list, "user_video/list/anon_list.html", request.META['HTTP_USER_AGENT'])
        return super(UserVideoList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserVideoList,self).get_context_data(**kwargs)
        context['user'] = self.user
        context['list'] = self.list
        return context

    def get_queryset(self):
        return self.video_list
