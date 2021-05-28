from users.models import User
from django.views.generic import ListView
from django.http import Http404
from common.templates import get_detect_platform_template
from managers.models import ModerationPenalty


class PenaltyUser(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_user_manager():
            self.template_name = get_detect_platform_template("managers/penalty_list/user_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(PenaltyUser,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return ModerationPenalty.get_penalty_users(self.request.user.pk)

class PenaltyDoc(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_doc_manager():
            self.template_name = get_detect_platform_template("managers/penalty_list/doc_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(PenaltyDoc,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return ModerationPenalty.get_penalty_docs(self.request.user.pk)

class PenaltyCommunity(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_community_manager():
            self.template_name = get_detect_platform_template("managers/penalty_list/community_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(PenaltyCommunity,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return ModerationPenalty.get_penalty_communities(self.request.user.pk)

class PenaltyElectNew(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_elect_new_manager():
            self.template_name = get_detect_platform_template("managers/penalty_list/elect_new_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(PenaltyElectNew,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return ModerationPenalty.get_penalty_elect_news(self.request.user.pk)

class PenaltySurvey(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_survey_manager():
            self.template_name = get_detect_platform_template("managers/penalty_list/survey_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(PenaltySurvey,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return ModerationPenalty.get_penalty_surveys(self.request.user.pk)


class PenaltyPhoto(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_photo_administrator():
            self.template_name = get_detect_platform_template("managers/penalty_list/photo_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(PenaltyPhoto,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return ModerationPenalty.get_penalty_photos(self.request.user.pk)

class PenaltyAudio(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_audio_manager():
            self.template_name = get_detect_platform_template("managers/penalty_list/audio_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(PenaltyAudio,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return ModerationPenalty.get_penalty_audios(self.request.user.pk)


class PenaltyVideo(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_video_manager():
            self.template_name = get_detect_platform_template("managers/penalty_list/video_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(PenaltyVideo,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return ModerationPenalty.get_penalty_videos(self.request.user.pk)
