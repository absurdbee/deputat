from django.views import View
from django.http import HttpResponse
from blog.models import Blog
from common.model.comments import BlogComment
from django.http import Http404
import json


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
