from django.views.generic.base import TemplateView
from django.views import View
from django.http import HttpResponse
from blog.models import ElectNew, Blog
from common.model.comments import ElectNewComment, BlogComment, ElectComment
from django.http import Http404
import json


class ElectNewLikeCreate(View):
    def get(self, request, **kwargs):
        from common.model.votes import ElectVotes

        new = ElectNew.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        try:
            likedislike = ElectVotes.objects.get(new=new, user=request.user)
            if likedislike.vote is not ElectVotes.LIKE:
                likedislike.vote = ElectVotes.LIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except ElectVotes.DoesNotExist:
            ElectVotes.objects.create(new=new, user=request.user, vote=ElectVotes.LIKE)
            result = True
        likes = new.likes_count()
        dislikes = new.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")

class ElectNewDislikeCreate(View):
    def get(self, request, **kwargs):
        from common.model.votes import ElectVotes

        new = ElectNew.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        try:
            likedislike = ElectVotes.objects.get(new=new, user=request.user)
            if likedislike.vote is not ElectVotes.DISLIKE:
                likedislike.vote = ElectVotes.DISLIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except ElectVotes.DoesNotExist:
            ElectVotes.objects.create(new=new, user=request.user, vote=ElectVotes.DISLIKE)
            result = True
        likes = new.likes_count()
        dislikes = new.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


class ElectNewCommentLikeCreate(View):
    def get(self, request, **kwargs):
        from common.model.votes import ElectNewCommentVotes

        comment = ElectNewComment.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        try:
            likedislike = ElectNewCommentVotes.objects.get(comment=comment, user=request.user)
            if likedislike.vote is not ElectNewCommentVotes.LIKE:
                likedislike.vote = ElectNewCommentVotes.LIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except ElectNewCommentVotes.DoesNotExist:
            ElectNewCommentVotes.objects.create(comment=comment, user=request.user, vote=ElectNewCommentVotes.LIKE)
            result = True
        likes = comment.likes_count()
        dislikes = comment.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")

class ElectNewCommentDislikeCreate(View):
    def get(self, request, **kwargs):
        from common.model.votes import ElectNewCommentVotes

        comment = ElectNewComment.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        try:
            likedislike = ElectNewCommentVotes.objects.get(comment=comment, user=request.user)
            if likedislike.vote is not ElectNewCommentVotes.DISLIKE:
                likedislike.vote = ElectNewCommentVotes.DISLIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except ElectNewCommentVotes.DoesNotExist:
            ElectNewCommentVotes.objects.create(comment=comment, user=request.user, vote=ElectNewCommentVotes.DISLIKE)
            result = True
        likes = comment.likes_count()
        dislikes = comment.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


class ElectCommentLikeCreate(View):
    def get(self, request, **kwargs):
        from common.model.votes import ElectCommentVotes

        comment = ElectComment.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        try:
            likedislike = ElectCommentVotes.objects.get(comment=comment, user=request.user)
            if likedislike.vote is not ElectCommentVotes.LIKE:
                likedislike.vote = ElectCommentVotes.LIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except ElectCommentVotes.DoesNotExist:
            ElectCommentVotes.objects.create(comment=comment, user=request.user, vote=ElectCommentVotes.LIKE)
            result = True
        likes = comment.likes_count()
        dislikes = comment.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")

class ElectCommentDislikeCreate(View):
    def get(self, request, **kwargs):
        from common.model.votes import ElectCommentVotes

        comment = ElectComment.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        try:
            likedislike = ElectCommentVotes.objects.get(comment=comment, user=request.user)
            if likedislike.vote is not ElectCommentVotes.DISLIKE:
                likedislike.vote = ElectCommentVotes.DISLIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except ElectCommentVotes.DoesNotExist:
            ElectCommentVotes.objects.create(comment=comment, user=request.user, vote=ElectCommentVotes.DISLIKE)
            result = True
        likes = comment.likes_count()
        dislikes = comment.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


class BlogLikeCreate(View):
    def get(self, request, **kwargs):
        from common.model.votes import BlogVotes

        comment = Blog.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        try:
            likedislike = BlogVotes.objects.get(comment=comment, user=request.user)
            if likedislike.vote is not BlogVotes.LIKE:
                likedislike.vote = BlogVotes.LIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except BlogVotes.DoesNotExist:
            BlogVotes.objects.create(comment=comment, user=request.user, vote=BlogVotes.LIKE)
            result = True
        likes = comment.likes_count()
        dislikes = comment.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")

class BlogDislikeCreate(View):
    def get(self, request, **kwargs):
        from common.model.votes import BlogVotes

        comment = Blog.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        try:
            likedislike = BlogVotes.objects.get(comment=comment, user=request.user)
            if likedislike.vote is not BlogVotes.DISLIKE:
                likedislike.vote = BlogVotes.DISLIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except BlogVotes.DoesNotExist:
            BlogVotes.objects.create(comment=comment, user=request.user, vote=BlogVotes.DISLIKE)
            result = True
        likes = comment.likes_count()
        dislikes = comment.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


class BlogCommentLikeCreate(View):
    def get(self, request, **kwargs):
        from common.model.votes import BlogCommentVotes

        comment = BlogComment.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        try:
            likedislike = BlogCommentVotes.objects.get(comment=comment, user=request.user)
            if likedislike.vote is not BlogCommentVotes.LIKE:
                likedislike.vote = BlogCommentVotes.LIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except BlogCommentVotes.DoesNotExist:
            BlogCommentVotes.objects.create(comment=comment, user=request.user, vote=BlogCommentVotes.LIKE)
            result = True
        likes = comment.likes_count()
        dislikes = comment.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")

class BlogCommentDislikeCreate(View):
    def get(self, request, **kwargs):
        from common.model.votes import BlogCommentVotes

        comment = BlogComment.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        try:
            likedislike = BlogCommentVotes.objects.get(comment=comment, user=request.user)
            if likedislike.vote is not BlogCommentVotes.DISLIKE:
                likedislike.vote = BlogCommentVotes.DISLIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except BlogCommentVotes.DoesNotExist:
            BlogCommentVotes.objects.create(comment=comment, user=request.user, vote=BlogCommentVotes.DISLIKE)
            result = True
        likes = comment.likes_count()
        dislikes = comment.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


class ElectSubscribe(View):
    def get(self,request,*args,**kwargs):
        from elect.models import SubscribeElect
        from elect.models import Elect

        elect = Elect.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and not SubscribeElect.is_elect_subscribe(elect.pk, request.user.pk):
            SubscribeElect.create_elect_subscribe(request.user.pk, elect.pk)
            return HttpResponse()
        else:
            raise Http404

class ElectUnSubscribe(View):
    def get(self,request,*args,**kwargs):
        from elect.models import SubscribeElect
        from elect.models import Elect

        elect = Elect.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and SubscribeElect.is_elect_subscribe(elect.pk, request.user.pk):
            subscribe = SubscribeElect.objects.filter(user_id=request.user.pk, elect_id=elect.pk)[0]
            subscribe.delete()
            return HttpResponse()
        else:
            raise Http404


class ElectNewCreate(View):
    template_name = "elect/add_new.html"

    def get(self,request,*args,**kwargs):
        from elect.models import Elect

        self.elect = Elect.objects.get(pk=self.kwargs["pk"])
        return super(ElectNewCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from blog.forms import ElectNewForm

        context=super(ElectNewCreate,self).get_context_data(**kwargs)
        context["form"] = ElectNewForm()
        return context

    def post(self,request,*args,**kwargs):
        from blog.forms import ElectNewForm
        from django.shortcuts import render
        from elect.models import Elect

        self.form_post = ElectNewForm(request.POST)
        self.elect = Elect.objects.get(pk=self.kwargs["pk"])

        if request.is_ajax() and self.form_post.is_valid() and request.user.is_authenticated:
            post = self.form_post.save(commit=False)
            post.creator = request.user
            post.save()
            return render(request, 'elect/elect_new.html', {'object': new_post})
        else:
            from django.http import HttpResponseBadRequest
            return HttpResponseBadRequest()
