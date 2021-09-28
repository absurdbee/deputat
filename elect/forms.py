from django import forms
from elect.models import Elect


class ElectForm(forms.ModelForm):
	class Meta:
		model = Elect
		fields = ['name', 'image', 'description', 'birthday', 'fraction', 'list', 'region', 'area', 'post_2','vk', 'fb', 'ig', 'tg', 'tw', 'mail', 'phone', 'address', 'site']
