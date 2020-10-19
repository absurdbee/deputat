from elect.models import ElectComment
from django import forms


class ElectForm(forms.ModelForm):
	text = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': ''}))

	class Meta:
		model = ElectComment
		fields = ['text']
