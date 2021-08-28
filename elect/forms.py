from django import forms
from elect.models import Elect


class ElectForm(forms.ModelForm):
	class Meta:
		model = Elect
		fields = ['name', 'image', 'description', 'list', 'region', 'city', 'birthday', 'fraction']
