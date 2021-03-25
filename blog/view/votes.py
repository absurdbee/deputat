import json
from django.views import View
from django.http import HttpResponse
from blog.models import ElectNew, Blog
from common.model.comments import ElectNewComment, BlogComment
from django.http import Http404
from common.notify import *


class ElectNewLike(View):
    def get(self, request, **kwargs):
        from common.model.votes import ElectVotes

        new = ElectNew.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        try:
            likedislike = ElectVotes.objects.get(new=new, user=request.user)
            if likedislike.vote != ElectVotes.LIKE:
                likedislike.vote = ElectVotes.LIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except ElectVotes.DoesNotExist:
            ElectVotes.objects.create(new=new, user=request.user, vote=ElectVotes.LIKE)
            result = True
            user_notify(request.user, new.creator.pk, "new"+str(new.pk), "new_notify", "LIK")
        likes = new.likes_count()
        dislikes = new.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")

class ElectNewDislike(View):
    def get(self, request, **kwargs):
        from common.model.votes import ElectVotes

        new = ElectNew.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        try:
            likedislike = ElectVotes.objects.get(new=new, user=request.user)
            if likedislike.vote != ElectVotes.DISLIKE:
                likedislike.vote = ElectVotes.DISLIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except ElectVotes.DoesNotExist:
            ElectVotes.objects.create(new=new, user=request.user, vote=ElectVotes.DISLIKE)
            result = True
            user_notify(request.user, new.creator.pk, "new"+str(new.pk), "new_notify", "DIS")
        likes = new.likes_count()
        dislikes = new.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


class ElectNewCommentLike(View):
    def get(self, request, **kwargs):
        from common.model.votes import ElectNewCommentVotes

        comment = ElectNewComment.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        try:
            likedislike = ElectNewCommentVotes.objects.get(comment=comment, user=request.user)
            if likedislike.vote != ElectNewCommentVotes.LIKE:
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
                user_notify(request.user, comment.commenter.pk, "com"+str(comment.pk)+", new"+str(comment.parent.new.pk), "new_comment", "LRE")
            else:
                user_notify(request.user, comment.commenter.pk, "com"+str(comment.pk)+", new"+str(comment.new.pk), "new_comment", "LCO")
        likes = comment.likes_count()
        dislikes = comment.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


class BlogLike(View):
    def get(self, request, **kwargs):
        from common.model.votes import BlogVotes

        blog = Blog.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        try:
            likedislike = BlogVotes.objects.get(blog=blog, user=request.user)
            if likedislike.vote == BlogVotes.LIKE:
                likedislike.delete()
            else:
                likedislike.vote = BlogVotes.LIKE
                likedislike.save(update_fields=['vote'])
        except BlogVotes.DoesNotExist:
            BlogVotes.objects.create(blog=blog, user=request.user, vote=BlogVotes.LIKE)
            user_notify(request.user, blog.creator.pk, "blo"+str(blog.pk), "blog_notify", "LIK")
        return HttpResponse(json.dumps({
                "like_count": str(blog.likes_count()),
                "inert_count": str(blog.inerts_count()),
                "dislike_count": str(blog.dislikes_count())}),
                content_type="application/json")

class BlogDislike(View):
    def get(self, request, **kwargs):
        from common.model.votes import BlogVotes

        blog = Blog.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        try:
            likedislike = BlogVotes.objects.get(blog=blog, user=request.user)
            if likedislike.vote != BlogVotes.DISLIKE:
                likedislike.vote = BlogVotes.DISLIKE
                likedislike.save(update_fields=['vote'])
            else:
                likedislike.delete()
        except BlogVotes.DoesNotExist:
            BlogVotes.objects.create(blog=blog, user=request.user, vote=BlogVotes.DISLIKE)
            user_notify(request.user, blog.creator.pk, "blo"+str(blog.pk), "blog_notify", "DIS")
        return HttpResponse(json.dumps({
                    "like_count": str(blog.likes_count()),
                    "inert_count": str(blog.inerts_count()),
                    "dislike_count": str(blog.dislikes_count())}),
                    content_type="application/json")

class BlogInert(View):
    def get(self, request, **kwargs):
        from common.model.votes import BlogVotes

        blog = Blog.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        try:
            likedislike = BlogVotes.objects.get(blog=blog, user=request.user)
            if likedislike.vote != BlogVotes.INERT:
                likedislike.vote = BlogVotes.INERT
                likedislike.save(update_fields=['vote'])
            else:
                likedislike.delete()
        except BlogVotes.DoesNotExist:
            BlogVotes.objects.create(blog=blog, user=request.user, vote=BlogVotes.INERT)
            user_notify(request.user, blog.creator.pk, "blo"+str(blog.pk), "blog_notify", "INS")
        return HttpResponse(json.dumps({
                    "like_count": str(blog.likes_count()),
                    "inert_count": str(blog.inerts_count()),
                    "dislike_count": str(blog.dislikes_count())}),
                    content_type="application/json")


class BlogCommentLike(View):
    def get(self, request, **kwargs):
        from common.model.votes import BlogCommentVotes

        comment = BlogComment.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        try:
            likedislike = BlogCommentVotes.objects.get(comment=comment, user=request.user)
            if likedislike.vote != BlogCommentVotes.LIKE:
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
                user_notify(request.user, comment.commenter.pk, "com"+str(comment.pk)+", blo"+str(comment.parent.blog.pk), "blog_comment", "LRE")
            else:
                user_notify(request.user, comment.commenter.pk, "com"+str(comment.pk)+", blo"+str(comment.blog.pk), "blog_comment", "LCO")
        likes = comment.likes_count()
        dislikes = comment.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")
