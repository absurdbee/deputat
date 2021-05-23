from blog.models import ElectNew
from common.model.comments import BlogComment, ElectNewComment
from django import forms


class ElectNewForm(forms.ModelForm):
	class Meta:
		model = ElectNew
		fields = ['title', 'description', 'category', ]


class BlogCommentForm(forms.ModelForm):
	text = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': ''}))
	class Meta:
		model = BlogComment
		fields = ['text']

class ElectNewCommentForm(forms.ModelForm):
	text = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': ''}))
	class Meta:
		model = ElectNewComment
		fields = ['text']
