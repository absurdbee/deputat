from blog.models import ElectNew, Blog
from common.model.comments import BlogComment, ElectNewComment
from django import forms


class SuggestElectNewForm(forms.ModelForm):
	class Meta:
		model = ElectNew
		fields = ['title', 'description', 'category', ]
class PublishElectNewForm(forms.ModelForm):
	class Meta:
		model = ElectNew
		fields = ['title', 'description', 'category', 'comments_enabled', 'votes_on', ]

class BlogForm(forms.ModelForm):
	class Meta:
		model = Blog
		fields = ['title', 'description', 'image', 'comments_enabled', 'votes_on', ]


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
