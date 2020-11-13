from elect.models import ElectNew
from django import forms


class ElectNewForm(forms.ModelForm):

	class Meta:
		model = ElectNew
		fields = ['title', 'description', ]
