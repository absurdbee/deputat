from users.models import User
from django.views.generic import ListView
from django.http import Http404
from common.templates import get_detect_platform_template


class ModerationUser(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_user_manager() or self.user.is_superuser:
            self.template_name = get_detect_platform_template("managers/moderation_list/user.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationUser,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return self.user.get_moderation_users()

class ModerationCommunity(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_community_manager() or self.user.is_superuser:
            self.template_name = get_detect_platform_template("managers/moderation_list/community.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationCommunity,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return self.user.get_moderation_communities()

class ModerationElectNew(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_elect_new_manager() or self.user.is_superuser:
            self.template_name = get_detect_platform_template("managers/moderation_list/elect_new.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationElectNew,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return self.user.get_moderation_posts()

class ModerationElectNewComment(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_elect_new_manager() or self.user.is_superuser:
            self.template_name = get_detect_platform_template("managers/moderation_list/elect_new_comment.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationElectNewComment,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return self.user.get_moderation_posts()

class ModerationSurvey(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_survey_manager() or self.user.is_superuser:
            self.template_name = get_detect_platform_template("managers/moderation_list/survey.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationSurvey,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return self.user.get_moderation_post_comments()


class ModerationPhoto(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_photo_manager() or self.user.is_superuser:
            self.template_name = get_detect_platform_template("managers/moderation_list/photo.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationPhoto,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return self.user.get_moderation_photos()

class ModerationAudio(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_audio_manager() or self.user.is_superuser:
            self.template_name = get_detect_platform_template("managers/moderation_list/audio.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationAudio,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return self.user.get_moderation_audios()


class ModerationVideo(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_video_manager() or self.user.is_superuser:
            self.template_name = get_detect_platform_template("managers/moderation_list/video.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationVideo,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return self.user.get_moderation_videos()


class ModerationUserAdvertiser(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_user_advertiser() or self.user.is_superuser:
            self.template_name = get_detect_platform_template("managers/moderation_list/user_advertiser.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationUserAdvertiser,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return []

class ModerationCommunityAdvertiser(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_community_advertiser() or self.user.is_superuser:
            self.template_name = get_detect_platform_template("managers/moderation_list/community_advertiser.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationCommunityAdvertiser,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return []
