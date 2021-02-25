from django import forms
from common.model.comments import ElectComment


class ElectCommentForm(forms.ModelForm):
	text = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': ''}))
	class Meta:
		model = ElectComment
		fields = ['text']
