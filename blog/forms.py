from blog.models import BlogComment, ElectNew
from django import forms


class BlogCommentForm(forms.ModelForm):
	text = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': ''}))
	class Meta:
		model = BlogComment
		fields = ['text']


class ElectNewForm(forms.ModelForm):
	class Meta:
		model = ElectNew
		fields = ['title', 'description', ]
