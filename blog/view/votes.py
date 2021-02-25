from django.views import View
from django.http import HttpResponse
from blog.models import ElectNew
from common.model.comments import ElectNewComment, ElectComment
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
