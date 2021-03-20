import json
from django.views import View
from django.http import HttpResponse
from blog.models import ElectNew, Blog
from common.model.comments import ElectNewComment, BlogComment
from django.http import Http404
from common.notify import *


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
            user_notify(request.user, new.creator.pk, None, "new"+str(new.pk), "new_notify", "LIK")
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
            user_notify(request.user, new.creator.pk, None, "new"+str(new.pk), "new_notify", "DIS")
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
            if comment.parent:
                user_notify(request.user, comment.commenter.pk, None, "com"+str(comment.pk)+", new"+str(comment.parent.new.pk), "new_comment", "LRE")
            else:
                user_notify(request.user, comment.commenter.pk, None, "com"+str(comment.pk)+", new"+str(comment.new.pk), "new_comment", "LCO")
        likes = comment.likes_count()
        dislikes = comment.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


class BlogLikeCreate(View):
    def get(self, request, **kwargs):
        from common.model.votes import BlogVotes

        blog = Blog.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        try:
            likedislike = BlogVotes.objects.get(blog=blog, user=request.user)
            if likedislike.vote is not BlogVotes.LIKE:
                likedislike.vote = BlogVotes.LIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except BlogVotes.DoesNotExist:
            BlogVotes.objects.create(blog=blog, user=request.user, vote=BlogVotes.LIKE)
            result = True
            user_notify(request.user, blog.creator.pk, None, "blo"+str(blog.pk), "blog_notify", "DIS")
        likes = blog.likes_count()
        dislikes = blog.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")

class BlogDislikeCreate(View):
    def get(self, request, **kwargs):
        from common.model.votes import BlogVotes

        blog = Blog.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        try:
            likedislike = BlogVotes.objects.get(blog=blog, user=request.user)
            if likedislike.vote is not BlogVotes.DISLIKE:
                likedislike.vote = BlogVotes.DISLIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except BlogVotes.DoesNotExist:
            BlogVotes.objects.create(blog=blog, user=request.user, vote=BlogVotes.DISLIKE)
            result = True
            user_notify(request.user, blog.creator.pk, None, "blo"+str(blog.pk), "blog_notify", "LIK")
        likes = blog.likes_count()
        dislikes = blog.dislikes_count()
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
            if comment.parent:
                user_notify(request.user, comment.commenter.pk, None, "com"+str(comment.pk)+", blo"+str(comment.parent.blog.pk), "blog_comment", "LRE")
            else:
                user_notify(request.user, comment.commenter.pk, None, "com"+str(comment.pk)+", blo"+str(comment.blog.pk), "blog_comment", "LCO")
        likes = comment.likes_count()
        dislikes = comment.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")
