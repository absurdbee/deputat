from django.views.generic import ListView
from django.http import Http404
from generic.mixins import CategoryListMixin
from common.templates import get_managers_template
from users.models import User


class ElectNewLogs(ListView):
    template_name, paginate_by = None, 30

    def get(self,request,*args,**kwargs):
        if request.user.is_supermanager():
            self.user = User.objects.get(pk=self.kwargs["pk"])
            self.template_name = get_managers_template("managers/logs/elect_new.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ElectNewLogs,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ElectNewLogs,self).get_context_data(**kwargs)
        context["user"] = self.user
        return context

    def get_queryset(self):
        from logs.model.manage_elect_new import ElectNewManageLog
        return ElectNewManageLog.objects.filter(manager=self.user.pk)


class UserLogs(ListView):
    template_name, paginate_by = None, 30

    def get(self,request,*args,**kwargs):
        if request.user.is_supermanager():
            self.user = User.objects.get(pk=self.kwargs["pk"])
            self.template_name = get_managers_template("managers/logs/user.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(UserLogs,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserLogs,self).get_context_data(**kwargs)
        context["user"] = self.user
        return context

    def get_queryset(self):
        from logs.model.manage_user_community import UserManageLog
        return UserManageLog.objects.filter(manager=self.user.pk)

class CommunityLogs(ListView):
    template_name, paginate_by = None, 30

    def get(self,request,*args,**kwargs):
        if request.user.is_supermanager():
            self.user = User.objects.get(pk=self.kwargs["pk"])
            self.template_name = get_managers_template("managers/logs/community.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(CommunityLogs,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityLogs,self).get_context_data(**kwargs)
        context["user"] = self.user
        return context

    def get_queryset(self):
        from logs.model.manage_user_community import CommunityManageLog
        return CommunityManageLog.objects.filter(manager=self.user.pk)


class BlogLogs(ListView):
    template_name, paginate_by = None, 30

    def get(self,request,*args,**kwargs):
        if request.user.is_supermanager():
            self.user = User.objects.get(pk=self.kwargs["pk"])
            self.template_name = get_managers_template("managers/logs/blog.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(BlogLogs,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(BlogLogs,self).get_context_data(**kwargs)
        context["user"] = self.user
        return context

    def get_queryset(self):
        from logs.model.manage_blog import BlogManageLog
        return BlogManageLog.objects.filter(manager=self.user.pk)


class PhotoLogs(ListView):
    template_name, paginate_by = None, 30

    def get(self,request,*args,**kwargs):
        if request.user.is_supermanager():
            self.user = User.objects.get(pk=self.kwargs["pk"])
            self.template_name = get_managers_template("managers/logs/photo.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(PhotoLogs,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PhotoLogs,self).get_context_data(**kwargs)
        context["user"] = self.user
        return context

    def get_queryset(self):
        from logs.model.manage_photo import PhotoManageLog
        return PhotoManageLog.objects.filter(manager=self.user.pk)


class AudioLogs(ListView):
    template_name, paginate_by = None, 30

    def get(self,request,*args,**kwargs):
        if request.user.is_supermanager():
            self.user = User.objects.get(pk=self.kwargs["pk"])
            self.template_name = get_managers_template("managers/logs/audio.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(AudioLogs,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AudioLogs,self).get_context_data(**kwargs)
        context["user"] = self.user
        return context

    def get_queryset(self):
        from logs.model.manage_audio import AudioManageLog
        return AudioManageLog.objects.filter(manager=self.user.pk)


class VideoLogs(ListView):
    template_name, paginate_by = None, 30

    def get(self,request,*args,**kwargs):
        if request.user.is_supermanager():
            self.user = User.objects.get(pk=self.kwargs["pk"])
            self.template_name = get_managers_template("managers/logs/video.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(VideoLogs,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(VideoLogs,self).get_context_data(**kwargs)
        context["user"] = self.user
        return context

    def get_queryset(self):
        from logs.model.manage_video import VideoManageLog
        return VideoManageLog.objects.filter(manager=self.user.pk)


class SurveyLogs(ListView):
    template_name, paginate_by = None, 30

    def get(self,request,*args,**kwargs):
        if request.user.is_supermanager():
            self.user = User.objects.get(pk=self.kwargs["pk"])
            self.template_name = get_managers_template("managers/logs/survey.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(SurveyLogs,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(SurveyLogs,self).get_context_data(**kwargs)
        context["user"] = self.user
        return context

    def get_queryset(self):
        from logs.model.manage_survey import SurveyManageLog
        return SurveyManageLog.objects.filter(manager=self.user.pk)


class DocLogs(ListView):
    template_name, paginate_by = None, 30

    def get(self,request,*args,**kwargs):
        if request.user.is_supermanager():
            self.user = User.objects.get(pk=self.kwargs["pk"])
            self.template_name = get_managers_template("managers/logs/doc.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(DocLogs,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(DocLogs,self).get_context_data(**kwargs)
        context["user"] = self.user
        return context

    def get_queryset(self):
        from logs.model.manage_doc import DocManageLog
        return DocManageLog.objects.filter(manager=self.user.pk)
