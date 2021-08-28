from django import forms
from common.model.comments import ElectComment
from elect.models import Elect


class ElectCommentForm(forms.ModelForm):
	text = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': ''}))
	class Meta:
		model = ElectComment
		fields = ['text']


class ElectForm(forms.ModelForm):
	class Meta:
		model = Elect
		fields = ['name', 'image', 'description', 'list', 'region', 'city', 'birthday', 'fraction']
