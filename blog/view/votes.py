import json
from django.views import View
from django.http import HttpResponse
from blog.models import ElectNew, Blog
from common.model.comments import ElectNewComment, BlogComment
from django.http import Http404
from common.notify import user_wall, user_notify


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
            user_wall(request.user, type="ELN", object_id=new.pk, "new_wall", "LIK")
            user_notify(request.user, type="ELN", object_id=new.pk, "new_notify", "LIK")
        return HttpResponse(json.dumps({
                "like_count": str(new.likes_count()),
                "inert_count": str(new.inerts_count()),
                "dislike_count": str(new.dislikes_count())}),
                content_type="application/json")

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
            user_wall(request.user, type="ELN", object_id=new.pk, "new_wall", "DIS")
            user_notify(request.user, type="ELN", object_id=new.pk, "new_notify", "DIS")
        return HttpResponse(json.dumps({
                "like_count": str(new.likes_count()),
                "inert_count": str(new.inerts_count()),
                "dislike_count": str(new.dislikes_count())}),
                content_type="application/json")

class ElectNewInert(View):
    def get(self, request, **kwargs):
        from common.model.votes import ElectVotes

        new = ElectNew.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        try:
            likedislike = ElectVotes.objects.get(new=new, user=request.user)
            if likedislike.vote != ElectVotes.INERT:
                likedislike.vote = ElectVotes.INERT
                likedislike.save(update_fields=['vote'])
            else:
                likedislike.delete()
        except ElectVotes.DoesNotExist:
            ElectVotes.objects.create(new=new, user=request.user, vote=ElectVotes.INERT)
            user_wall(request.user, type="ELN", object_id=new.pk, "new_notify", "INE")
            user_notify(request.user, type="ELN", object_id=new.pk, "new_notify", "INE")
        return HttpResponse(json.dumps({
                    "like_count": str(new.likes_count()),
                    "inert_count": str(new.inerts_count()),
                    "dislike_count": str(new.dislikes_count())}),
                    content_type="application/json")


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
            user_wall(request.user, type="ELNC", object_id=comment.pk, "new_comment", "LCO")
            user_notify(request.user, type="ELNC", object_id=comment.pk, "new_comment", "LRE")
        likes = comment.likes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes)}),content_type="application/json")


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
            user_wall(request.user, type="BLO", object_id=blog.pk, "new_notify", "LIK")
            user_notify(request.user, type="BLO", object_id=blog.pk, "new_notify", "LIK")
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
            user_wall(request.user, type="BLO", object_id=blog.pk, "new_notify", "DIS")
            user_notify(request.user, type="BLO", object_id=blog.pk, "new_notify", "DIS")
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
            user_wall(request.user, type="BLO", object_id=blog.pk, "new_notify", "INE")
            user_notify(request.user, type="BLO", object_id=blog.pk, "new_notify", "INE")
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
            user_wall(request.user, type="BLOC", object_id=comment.pk, "blog_comment", "LCO")
            user_notify(request.user, type="BLOC", object_id=comment.pk, "blog_comment", "LRE")
        likes = comment.likes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes)}),content_type="application/json")
