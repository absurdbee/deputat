from users.models import User
from django.views.generic import ListView
from django.http import Http404
from common.templates import get_detect_platform_template
from managers.models import Moderated


class ModerationUser(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_user_manager():
            self.template_name = get_detect_platform_template("managers/moderation_list/user_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationUser,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return Moderated.get_moderation_users()


class ModerationDoc(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_doc_manager():
            self.template_name = get_detect_platform_template("managers/moderation_list/doc_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationDoc,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return self.user.get_moderation_docs()


class ModerationCommunity(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_community_manager():
            self.template_name = get_detect_platform_template("managers/moderation_list/community_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationCommunity,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return self.user.get_moderation_communities()

class ModerationElectNew(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_elect_new_manager():
            self.template_name = get_detect_platform_template("managers/moderation_list/elect_new_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationElectNew,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return self.user.get_moderation_posts()

class ModerationSurvey(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_survey_manager():
            self.template_name = get_detect_platform_template("managers/moderation_list/survey_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationSurvey,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return self.user.get_moderation_post_comments()


class ModerationPhoto(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_photo_manager():
            self.template_name = get_detect_platform_template("managers/moderation_list/photo_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationPhoto,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return self.user.get_moderation_photos()

class ModerationAudio(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_audio_manager():
            self.template_name = get_detect_platform_template("managers/moderation_list/audio_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationAudio,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return self.user.get_moderation_audios()


class ModerationVideo(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_video_manager():
            self.template_name = get_detect_platform_template("managers/moderation_list/video_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationVideo,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return self.user.get_moderation_videos()
