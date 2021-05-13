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

        if not request.is_ajax():
            raise Http404
        new = ElectNew.objects.get(pk=self.kwargs["pk"])
        return new.send_like(request.user, None)

class ElectNewDislike(View):
    def get(self, request, **kwargs):
        from common.model.votes import ElectVotes

        if not request.is_ajax():
            raise Http404
        new = ElectNew.objects.get(pk=self.kwargs["pk"])
        return new.send_dislike(request.user, None)

class ElectNewInert(View):
    def get(self, request, **kwargs):
        from common.model.votes import ElectVotes

        if not request.is_ajax():
            raise Http404
        new = ElectNew.objects.get(pk=self.kwargs["pk"])
        return new.send_inert(request.user, None)


class ElectNewCommentLike(View):
    def get(self, request, **kwargs):
        from common.model.votes import ElectNewCommentVotes

        if not request.is_ajax():
            raise Http404
        comment = ElectNewComment.objects.get(pk=self.kwargs["pk"])
        return comment.send_like(request.user, None)


class BlogLike(View):
    def get(self, request, **kwargs):
        from common.model.votes import BlogVotes

        if not request.is_ajax():
            raise Http404
        blog = Blog.objects.get(pk=self.kwargs["pk"])
        return blog.send_like(request.user, None)

class BlogDislike(View):
    def get(self, request, **kwargs):
        from common.model.votes import BlogVotes

        if not request.is_ajax():
            raise Http404
        blog = Blog.objects.get(pk=self.kwargs["pk"])
        return blog.send_dislike(request.user, None)

class BlogInert(View):
    def get(self, request, **kwargs):
        from common.model.votes import BlogVotes

        if not request.is_ajax():
            raise Http404
        blog = Blog.objects.get(pk=self.kwargs["pk"])
        return blog.send_inert(request.user, None)


class BlogCommentLike(View):
    def get(self, request, **kwargs):
        from common.model.votes import BlogCommentVotes

        if not request.is_ajax():
            raise Http404
        comment = BlogComment.objects.get(pk=self.kwargs["pk"])
        return comment.send_like(request.user, None)
