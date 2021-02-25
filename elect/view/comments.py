from elect.models import Elect
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from django.http import Http404


class ElectCommentCreate(View):
	def post(self,request,*args,**kwargs):
		from elect.forms import ElectCommentForm
		from django.shortcuts import render

		form_post = ElectCommentForm(request.POST)
		elect = Elect.objects.get(pk=request.POST.get('pk'))
		if request.is_ajax() and form_post.is_valid() and elect.comments_enabled:
			comment = form_post.save(commit=False)
			new_comment = comment.create_comment(commenter=request.user, parent=None, elect=elect, text=comment.text)
			return render(request, 'elect_comment/elect_parent.html',{'comment': new_comment})
		else:
			return HttpResponseBadRequest()


class ElectReplyCreate(View):
	def post(self,request,*args,**kwargs):
		from elect.forms import ElectCommentForm
		from django.shortcuts import render
		from common.model.comments import ElectComment

		form_post = ElectCommentForm(request.POST)
		parent = ElectComment.objects.get(pk=request.POST.get('post_comment'))
		if request.is_ajax() and form_post.is_valid():
			comment = form_post.save(commit=False)
			new_comment = comment.create_comment(commenter=request.user, parent=parent, elect=None, text=comment.text)
			return render(request, 'elect_comment/elect_reply.html',{'reply': new_comment, 'comment': parent,})
		else:
			return HttpResponseBadRequest()

class ElectCommentDelete(View):
	def get(self,request,*args,**kwargs):
		from common.model.comments import ElectComment

		comment = ElectComment.objects.get(pk=self.kwargs["pk"])
		if request.is_ajax() and request.user.pk == comment.commenter.pk:
			comment.is_deleted = True
			comment.save(update_fields=['is_deleted'])
			return HttpResponse()
		else:
			raise Http404

class ElectCommentAbortDelete(View):
	from common.model.comments import ElectComment

	def get(self,request,*args,**kwargs):
		comment = ElectComment.objects.get(pk=self.kwargs["pk"])
		if request.is_ajax() and request.user.pk == comment.commenter.pk:
			comment.is_deleted = False
			comment.save(update_fields=['is_deleted'])
			return HttpResponse()
		else:
			raise Http404
