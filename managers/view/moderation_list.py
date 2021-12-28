from users.models import User
from django.views.generic import ListView
from django.http import Http404
from common.templates import get_detect_platform_template
from managers.models import Moderated
from generic.mixins import CategoryListMixin


class ModerationUser(ListView, CategoryListMixin):
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


class ModerationDoc(ListView, CategoryListMixin):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_doc_manager():
            self.template_name = get_detect_platform_template("managers/moderation_list/doc_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationDoc,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return Moderated.get_moderation_docs()


class ModerationCommunity(ListView, CategoryListMixin):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_community_manager():
            self.template_name = get_detect_platform_template("managers/moderation_list/community_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationCommunity,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return Moderated.get_moderation_communities()

class ModerationElectNew(ListView, CategoryListMixin):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_elect_new_manager():
            self.template_name = get_detect_platform_template("managers/moderation_list/elect_new_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationElectNew,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return Moderated.get_moderation_elect_news()

class ModerationElect(ListView, CategoryListMixin):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        if request.user.is_elect_new_manager():
            self.template_name = get_detect_platform_template("managers/moderation_list/elect_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationElect,self).get(request,*args,**kwargs)

    def get_queryset(self):
        from elect.models import Elect
        return Elect.objects.filter(type="SUG")


class ModerationBlog(ListView, CategoryListMixin):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_blog_manager():
            self.template_name = get_detect_platform_template("managers/moderation_list/blog_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationBlog,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return Moderated.get_moderation_blog()

class ModerationSurvey(ListView, CategoryListMixin):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_survey_manager():
            self.template_name = get_detect_platform_template("managers/moderation_list/survey_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationSurvey,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return Moderated.get_moderation_survey()


class ModerationPhoto(ListView, CategoryListMixin):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_photo_manager():
            self.template_name = get_detect_platform_template("managers/moderation_list/photo_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationPhoto,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return Moderated.get_moderation_photos()

class ModerationAudio(ListView, CategoryListMixin):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_audio_manager():
            self.template_name = get_detect_platform_template("managers/moderation_list/audio_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationAudio,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return Moderated.get_moderation_audios()


class ModerationVideo(ListView, CategoryListMixin):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_video_manager():
            self.template_name = get_detect_platform_template("managers/moderation_list/video_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationVideo,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return Moderated.get_moderation_videos()

class ModerationChat(ListView, CategoryListMixin):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_manager():
            self.template_name = get_detect_platform_template("managers/moderation_list/chat_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationChat,self).get(request,*args,**kwargs)

    def get_queryset(self):
        from chat.models import Chat
        query = []
        for chat in Chat.objects.filter(type='SUP'):
            if chat.members == 1:
                query.append(chat)
        return query
