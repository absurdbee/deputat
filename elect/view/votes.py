from django.views import View
from django.http import HttpResponse
from common.model.comments import BlogComment
from django.http import Http404
import json


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
