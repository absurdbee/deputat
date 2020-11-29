from django.views.generic.base import TemplateView
from elect.models import Elect, SubscribeElect
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest
from blog.forms import ElectNewForm
from users.models import User
from blog.models import ElectNew, ElectVotes, BlogVotes, Blog
from django.http import Http404
from django.shortcuts import render
import json


class ElectLikeCreate(View):
    def get(self, request, **kwargs):
        new = ElectNew.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        try:
            likedislike = ElectVotes.objects.get(parent=new, user=request.user)
            if likedislike.vote is not ElectVotes.LIKE:
                likedislike.vote = ElectVotes.LIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except ElectVotes.DoesNotExist:
            ElectVotes.objects.create(parent=new, user=request.user, vote=ElectVotes.LIKE)
            result = True
        likes = new.likes_count()
        dislikes = new.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(disliks)}),content_type="application/json")

class ElectDislikeCreate(View):
    def get(self, request, **kwargs):
        new = ElectNew.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        try:
            likedislike = ElectVotes.objects.get(parent=new, user=request.user)
            if likedislike.vote is not ElectVotes.DISLIKE:
                likedislike.vote = ElectVotes.DISLIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except ElectVotes.DoesNotExist:
            ElectVotes.objects.create(parent=new, user=request.user, vote=ElectVotes.DISLIKE)
            result = True
        likes = item.likes_count()
        dislikes = video.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


class BlogLikeCreate(View):
    def get(self, request, **kwargs):
        new = Blog.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        try:
            likedislike = BlogVotes.objects.get(parent=new, user=request.user)
            if likedislike.vote is not BlogVotes.LIKE:
                likedislike.vote = BlogVotes.LIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except BlogVotes.DoesNotExist:
            BlogVotes.objects.create(parent=new, user=request.user, vote=BlogVotes.LIKE)
            result = True
        likes = new.likes_count()
        dislikes = new.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(disliks)}),content_type="application/json")

class BlogDislikeCreate(View):
    def get(self, request, **kwargs):
        new = Blog.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        try:
            likedislike = BlogVotes.objects.get(parent=new, user=request.user)
            if likedislike.vote is not BlogVotes.DISLIKE:
                likedislike.vote = BlogVotes.DISLIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except BlogVotes.DoesNotExist:
            BlogVotes.objects.create(parent=new, user=request.user, vote=BlogVotes.DISLIKE)
            result = True
        likes = item.likes_count()
        dislikes = video.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


class ElectSubscribe(View):
    def get(self,request,*args,**kwargs):
        elect = Elect.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and not SubscribeElect.is_elect_subscribe(elect.pk, request.user.pk):
            SubscribeElect.create_elect_subscribe(request.user.pk, elect.pk)
            return HttpResponse()
        else:
            raise Http404

class ElectUnSubscribe(View):
    def get(self,request,*args,**kwargs):
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
        self.elect = Elect.objects.get(pk=self.kwargs["pk"])
        return super(ElectNewCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ElectNewCreate,self).get_context_data(**kwargs)
        context["form"] = ElectNewForm()
        return context

    def post(self,request,*args,**kwargs):
        self.form_post = ElectNewForm(request.POST)
        self.elect = Elect.objects.get(pk=self.kwargs["pk"])

        if request.is_ajax() and self.form_post.is_valid() and request.user.is_authenticated:
            post = self.form_post.save(commit=False)
            post.creator = request.user
            post.save()
            return render(request, 'elect/elect_new.html', {'object': new_post})
        else:
            return HttpResponseBadRequest()
