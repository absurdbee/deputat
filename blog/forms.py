from blog.models import BlogComment
from django import forms


class BlogCommentForm(forms.ModelForm):
	text = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': ''}))

	class Meta:
		model = BlogComment
		fields = ['text']
