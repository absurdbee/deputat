from quan.models import Support
from django import forms


class SupportForm(forms.ModelForm):

	class Meta:
		model = Support
		fields = ['description', 'type']
